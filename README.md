# Quadtree Image Compression

This repository contains a Python implementation of a quadtree-based image compression algorithm. The implementation includes classes and functions to build a quadtree, compress colors, and reconstruct images from quadtree data.

## Files Overview

### 1. `main.py`

Contains the implementation of the quadtree data structure and related functions.

- **Data Structures:** `quadtree.py`
- **Classes:** `Node`, `Quadtree`
- **Functions:** 
  - `build_quadtree(qt)`
  - `quadtree_to_image(qt, draw_box=False)`
  - `compress_quadtree(qt, threshold)`
  - `count_nodes(node)`
  - `max_num_nodes(N)`

### 2. `testing.ipynb`

Contains examples and tests for the quadtree image compression algorithm. The notebook includes image resizing and compression demonstrations.

### 3. `figures` folder

Contains images used for testing and demonstration purposes in the `testing.ipynb` notebook.

## Usage

To use the quadtree image compression algorithm:

1. Ensure you have the necessary libraries installed, including `numpy`.
2. Import the necessary classes and functions from `main.py`.
3. Create a `Quadtree` object with an image array.
4. Build the quadtree using `build_quadtree(qt)`.
5. Compress colors using `compress_quadtree(qt, threshold)`.
6. Reconstruct the image using `quadtree_to_image(qt)`.

Refer to the `testing.ipynb` notebook for examples and demonstrations.

## Testing

The `testing.ipynb` notebook provides examples and tests for the quadtree image compression algorithm. It includes step-by-step demonstrations of building quadtrees, compressing colors, and reconstructing images.

