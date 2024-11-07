# Annotation Processor

The `AnnotationProcessor` class is designed to manage and process annotation data for pose estimation tasks, specifically for datasets in the CVAT and COCO formats. The class can split datasets, save data in the COCO format, create visualizations, and manage annotations.

## Requirements

Make sure you have the following packages installed:

- `cv2` (OpenCV)
- `numpy`

## Class: `AnnotationProcessor`

### Attributes

- `cvat_root` : `str`  
  Root directory of the CVAT dataset.

- `cvat_dataset_names` : `list of str`  
  List of dataset names within the root directory.

- `split` : `float`  
  Proportion of frames to be allocated to the training set.

- `output_path` : `str`  
  Path where processed COCO files and random samples will be saved.

### Methods

#### `__init__(self, cvat_root, cvat_dataset_names, split, output_path)`
Constructor to initialize the processor with dataset paths, split ratio, and output paths.

#### `load_frames(self, name)`
Loads annotation frames for a given dataset name and splits them into training and validation sets based on the `split` ratio.

#### `save_frames_to_coco_dataset(self, frames, coco_result_path)`
Converts frames to COCO format and saves them as JSON files. Generates two JSON files:
  - `{coco_result_path}_annotation.json`: contains annotation details.
  - `{coco_result_path}.json`: main COCO file containing images, annotations, and categories.

#### `generate_random_samples(self, frames, output_path, k=10)`
Randomly samples frames and saves images with bounding boxes and keypoints. Useful for quickly checking the accuracy and quality of annotations.

#### `process_datasets(self)`
Processes each dataset in `cvat_dataset_names`, loading, splitting, and saving as COCO format. This is the main pipeline function that leverages `load_frames` and `save_frames_to_coco_dataset`.

#### `read_annotation_frames(json_path, img_root)`
Static method to load annotation frames from a specified JSON file path, using an optional root path for images.

#### `read_coco_as_frames(json_path, img_root=None)`
Static method to read COCO-formatted annotation frames from a JSON file and return a structured dataset for further processing.

#### `trim_annotation(data)`
Static method to trim long lists within annotation data for easy viewing. Trims any list longer than 20 items to show the first two items with an ellipsis (`...`).

#### `plot_mouse(mouse, img, color)`
Static method to plot keypoints and bounding boxes for a given mouse annotation on an image. Draws each keypoint and a bounding box around the mouse, using a specified color.
