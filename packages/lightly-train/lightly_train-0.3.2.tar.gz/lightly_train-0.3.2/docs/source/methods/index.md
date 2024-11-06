(methods)=

# Methods

Lightly**Train** supports the following self-supervised learning methods:

- `dino` (recommended)

  [DINO](https://arxiv.org/abs/2104.14294) is a popular self-supervised learning
  method that works well across various datasets, model architectures, and tasks.

- `densecl` (experimental)

  [DenseCL](https://arxiv.org/abs/2011.09157) was developed for learning strong local
  image representations, particularly for detection and segmentation tasks.

- `densecldino` (experimental)

  DenseCLDINO is a variant of DenseCL that combines DINO and DenseCL for more
  efficient learning of local image representations.

- `simclr`

  [SimCLR](https://arxiv.org/abs/2002.05709) is a classic self-supervised learning
  method widely used as a baseline for model pre-training.
