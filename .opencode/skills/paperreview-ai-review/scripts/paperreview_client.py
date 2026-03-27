#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

BASE_URL = "https://paperreview.ai"
MAX_FILE_SIZE = 10 * 1024 * 1024


def fail(message):
    print(message, file=sys.stderr)
    raise SystemExit(1)


def request(method, url, *, data=None, headers=None, timeout=120):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


def request_json(method, url, payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    status, _, body = request(method, url, data=data, headers=headers)
    try:
        parsed = json.loads(body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        parsed = {"raw_body": body.decode("utf-8", errors="replace")}
    return status, parsed


def encode_multipart(fields, files):
    boundary = f"----paperreview-{uuid.uuid4().hex}"
    body = bytearray()

    def add_text(name, value):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(str(value).encode("utf-8"))
        body.extend(b"\r\n")

    def add_file(name, filename, content, content_type):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode("utf-8")
        )
        body.extend(f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"))
        body.extend(content)
        body.extend(b"\r\n")

    for key, value in fields.items():
        add_text(key, value)
    for key, file_info in files.items():
        add_file(key, file_info["filename"], file_info["content"], file_info["content_type"])

    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    content_type = f"multipart/form-data; boundary={boundary}"
    return content_type, bytes(body)


def request_multipart(method, url, fields, files=None):
    files = files or {}
    content_type, body = encode_multipart(fields, files)
    return request(method, url, data=body, headers={"Content-Type": content_type})


def derive_verdict(score, assessment_text):
    if score is not None:
        if score >= 8.5:
            return "Strong Accept"
        if score >= 7.5:
            return "Accept"
        if score >= 6.5:
            return "Weak Accept"
        if score >= 5.5:
            return "Borderline"
        if score >= 4.5:
            return "Weak Reject"
        return "Reject"

    lowered = (assessment_text or "").lower()
    for label in ["strong accept", "weak accept", "borderline", "weak reject", "reject", "accept"]:
        if label in lowered:
            return label.title()
    return "No calibrated score returned"


def ensure_parent(path):
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)


def write_json(path, payload):
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_text(path, text):
    ensure_parent(path)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def render_markdown(data, round_label, artifact_path):
    sections = data.get("sections", {}) or {}
    score = data.get("numerical_score")
    verdict = derive_verdict(score, sections.get("assessment", ""))
    score_text = f"{score} / 10" if score is not None else "not returned by paperreview.ai"
    lines = [
        f"# {round_label} Review",
        "",
        f"Reviewed artifact: `{artifact_path}`",
        "",
        "Backend: `paperreview.ai`",
        "",
        f"Score: `{score_text}`",
        "",
        f"Verdict: `{verdict}`",
        "",
    ]

    ordered_sections = [
        ("summary", "Summary"),
        ("strengths", "Strengths"),
        ("weaknesses", "Weaknesses"),
        ("detailed_comments", "Detailed Comments"),
        ("questions", "Questions"),
        ("assessment", "Overall Assessment"),
        ("full_review", "Full Review"),
    ]
    for key, heading in ordered_sections:
        text = sections.get(key)
        if text:
            lines.extend([f"## {heading}", "", text.strip(), ""])
    return "\n".join(lines).rstrip() + "\n"


def render_scorecard(data, artifact_path, round_label):
    sections = data.get("sections", {}) or {}
    score = data.get("numerical_score")
    verdict = derive_verdict(score, sections.get("assessment", ""))
    return {
        "backend": "paperreview.ai",
        "paper_path": artifact_path,
        "round_label": round_label,
        "title": data.get("title"),
        "venue": data.get("venue"),
        "submission_date": data.get("submission_date"),
        "final_score": score,
        "verdict": verdict,
        "score_note": "paperreview.ai calibrated score is currently exposed for ICLR submissions only",
        "available_sections": sorted(list(sections.keys())),
    }


def submit(pdf_path, email, venue):
    if not os.path.exists(pdf_path):
        fail(f"PDF not found: {pdf_path}")
    if os.path.getsize(pdf_path) > MAX_FILE_SIZE:
        fail(f"PDF exceeds 10MB limit: {pdf_path}")

    filename = os.path.basename(pdf_path)
    status, url_data = request_json(
        "POST",
        f"{BASE_URL}/api/get-upload-url",
        {"filename": filename, "venue": venue or ""},
    )
    if status != 200:
        fail(url_data.get("detail") or f"get-upload-url failed with status {status}")

    with open(pdf_path, "rb") as handle:
        content = handle.read()

    content_type = mimetypes.guess_type(filename)[0] or "application/pdf"
    s3_status, _, _ = request_multipart(
        "POST",
        url_data["presigned_url"],
        url_data["presigned_fields"],
        {"file": {"filename": filename, "content": content, "content_type": content_type}},
    )
    if s3_status not in (200, 201, 204):
        fail(f"S3 upload failed with status {s3_status}")

    confirm_status, _, confirm_body = request_multipart(
        "POST",
        f"{BASE_URL}/api/confirm-upload",
        {"s3_key": url_data["s3_key"], "venue": venue or "", "email": email},
    )
    try:
        confirm_data = json.loads(confirm_body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        fail("confirm-upload returned non-JSON output")
    if confirm_status != 200 or not confirm_data.get("success"):
        fail(confirm_data.get("detail") or confirm_data.get("message") or "confirm-upload failed")

    token = confirm_data.get("token")
    if not token:
        fail("confirm-upload succeeded but returned no token")

    return {
        "backend": "paperreview.ai",
        "pdf_path": pdf_path,
        "filename": filename,
        "venue": venue or "",
        "email_redacted": True,
        "email_domain": email.split("@", 1)[1] if "@" in email else None,
        "token": token,
        "message": confirm_data.get("message", ""),
        "s3_key": url_data.get("s3_key"),
    }


def wait_for_review(token, timeout_seconds, interval_seconds):
    deadline = time.time() + timeout_seconds
    last_detail = None
    while time.time() < deadline:
        status, data = request_json("GET", f"{BASE_URL}/api/review/{urllib.parse.quote(token)}")
        if status == 200:
            return data
        if status == 202:
            last_detail = data.get("detail", "Review still processing")
            time.sleep(interval_seconds)
            continue
        fail(data.get("detail") or f"review lookup failed with status {status}")
    fail(f"Timed out waiting for review. Last status: {last_detail or 'processing'}")


def main():
    parser = argparse.ArgumentParser(description="paperreview.ai submission and retrieval client")
    subparsers = parser.add_subparsers(dest="command", required=True)

    submit_wait = subparsers.add_parser("submit-and-wait", help="submit a PDF and wait for the review")
    submit_wait.add_argument("--pdf", required=True)
    submit_wait.add_argument("--email", required=True)
    submit_wait.add_argument("--venue", default="")
    submit_wait.add_argument("--round-label", required=True)
    submit_wait.add_argument("--artifact", required=True)
    submit_wait.add_argument("--submission-json", required=True)
    submit_wait.add_argument("--review-json", required=True)
    submit_wait.add_argument("--review-md", required=True)
    submit_wait.add_argument("--scorecard-json", required=True)
    submit_wait.add_argument("--timeout-seconds", type=int, default=21600)
    submit_wait.add_argument("--interval-seconds", type=int, default=60)

    render = subparsers.add_parser("render", help="render markdown and scorecard from an existing review JSON")
    render.add_argument("--review-json", required=True)
    render.add_argument("--round-label", required=True)
    render.add_argument("--artifact", required=True)
    render.add_argument("--review-md", required=True)
    render.add_argument("--scorecard-json", required=True)

    args = parser.parse_args()

    if args.command == "submit-and-wait":
        submission = submit(args.pdf, args.email, args.venue)
        write_json(args.submission_json, submission)
        print(f"paperreview.ai token: {submission['token']}")

        review = wait_for_review(submission["token"], args.timeout_seconds, args.interval_seconds)
        write_json(args.review_json, review)
        write_text(args.review_md, render_markdown(review, args.round_label, args.artifact))
        write_json(args.scorecard_json, render_scorecard(review, args.artifact, args.round_label))
        print(f"saved review to {args.review_md}")
        return

    if args.command == "render":
        with open(args.review_json, "r", encoding="utf-8") as handle:
            review = json.load(handle)
        write_text(args.review_md, render_markdown(review, args.round_label, args.artifact))
        write_json(args.scorecard_json, render_scorecard(review, args.artifact, args.round_label))
        print(f"rendered review to {args.review_md}")


if __name__ == "__main__":
    main()
