# Prior Art Update

**Question**: What changed in the literature after the 2018 paper, and what upgrade path remains open?

## What Changed

### 1. 3D learning moved beyond the old volumetric-versus-projection framing

By 2021, point-based self-attention models such as **Point Transformer** shifted the discussion away from ``can 2D proxies replace 3D CNNs?'' and toward stronger native 3D architectures.  
Source: [Point Transformer, ICCV 2021](https://openaccess.thecvf.com/content/ICCV2021/html/Zhao_Point_Transformer_ICCV_2021_paper.html)

### 2. Serialization became an explicit efficiency strategy

Later work began to say the quiet part out loud: point and voxel data can be serialized to improve compute and memory behavior.

- **Point Transformer V3** explicitly uses efficient serialized neighbor mapping to scale 3D models.  
  Source: [Point Transformer V3, CVPR 2024](https://openaccess.thecvf.com/content/CVPR2024/html/Wu_Point_Transformer_V3_Simpler_Faster_Stronger_CVPR_2024_paper)

- **PointMamba** uses space-filling curves for point tokenization in a linear-complexity state-space backbone.  
  Source: [PointMamba, NeurIPS 2024](https://openreview.net/forum?id=Kc37srXvan)

- **Voxel Mamba** states directly that serialization-based voxel methods are already effective in 3D detection, while trying to recover locality more efficiently.  
  Source: [Voxel Mamba, NeurIPS 2024](https://openreview.net/forum?id=gHYhVSCtDH)

- **NoKSR** uses point cloud serialization as a core ingredient in efficient neural surface reconstruction.  
  Source: [NoKSR, 3DV 2025](https://openreview.net/forum?id=Z8bwCg6tJH)

### 3. Structural biology also moved forward

The structural-biology side is now stronger too. Voxel-based protein representation learning has resurfaced in more modern self-supervised form.

- **AtoMAE** learns protein structure representations from atomic voxel grids with masked autoencoding, showing that voxelized structural learning is still a live idea when tied to modern architectures.  
  Source: [AtoMAE, GenBio 2025](https://openreview.net/forum?id=PrzgZvPwVT)

## What This Means For The Source Paper

The original empirical claim is saturated:

- it is no longer enough to compare mapped 2D/1D CNNs against 3D CNNs
- the strongest modern work already treats serialization as a serious computational tool
- a direct refresh would need new experiments the repo does not have

## Remaining Novelty Gap

A gap still exists, but it is a different one:

> There is still room for a unifying paper that explains serialization as a general representation interface across voxel, point, and biomolecular 3D learning, and that positions early Hilbert-style mappings as part of that broader lineage.

That gap is especially credible if the new paper contributes:

1. a cross-era taxonomy of serialization strategies
2. a design framework for locality, token efficiency, and channel semantics
3. a biomolecular agenda where serialization is framed as a way to bridge irregular structures and sequence-native foundation models

## Best Defensible Upgrade Path

**Pivot to a perspective paper.**

This path is stronger than a cosmetic revision because it changes:

- the target audience
- the central claim
- the evidence base
- the paper type

It uses the source paper as a precursor and anchor, not merely as text to polish.
