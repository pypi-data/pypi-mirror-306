# YOLO Formatter

YOLO Formatter is a Python library that helps you organize your dataset in a YOLO-compatible structure. This package is designed to simplify the process of converting a disorganized dataset into a structure that YOLO models can easily understand. This tool is particularly useful for users who have images and labels scattered in different directories and need an easy way to create a clean dataset structure.

## Features
- Automatically collects images and corresponding label files from a parent directory.
- Organizes images and labels into `train`, `val`, and `test` splits.
- Creates a clean output directory (`Data`) for easy integration with YOLO models.
- Ensures that the dataset is formatted correctly, reducing user error and speeding up model training preparation.

## Installation

Install YOLO Formatter via pip:

```sh
pip install yolo_formatter
```

## Requirements
- Python 3.6+
- scikit-learn (for splitting datasets)

You can install the required dependencies with:

```sh
pip install scikit-learn
```

## Usage

### Quick Start

Here's a simple example to get started:

```python
from yolo_formatter import YOLODatasetFormatter

# Initialize the formatter with the path to your dataset's parent directory
formatter = YOLODatasetFormatter(parent_dir='path/to/your/dataset')

# Execute the formatting process
formatter.execute()
```

This script will:
1. Find all images and corresponding labels in the `parent_dir` you specify.
2. Split the data into `train`, `val`, and `test` subsets.
3. Create a structured dataset in the `Data` directory, containing folders for images and labels under each split.

### Parameters
- `parent_dir` (str): Path to the directory containing your dataset (images and labels).
- `output_dir` (str, optional): Path to the output directory where the structured dataset will be saved. Default is "Data".
- `train_ratio` (float, optional): Proportion of the dataset to be used for training. Default is `0.8`.
- `val_ratio` (float, optional): Proportion of the dataset to be used for validation. Default is `0.1`.
- `test_ratio` (float, optional): Proportion of the dataset to be used for testing. Default is `0.1`.

### Example

To use a different output directory and data split ratio:

```python
formatter = YOLODatasetFormatter(parent_dir='path/to/your/dataset', output_dir='FormattedData', train_ratio=0.7, val_ratio=0.2, test_ratio=0.1)
formatter.execute()
```

## Output Structure
After running the formatter, your output directory (`Data` by default) will have the following structure:

```
Data/
  train/
    images/
    labels/
  val/
    images/
    labels/
  test/
    images/
    labels/
```

- `images/`: Contains the images for training, validation, or testing.
- `labels/`: Contains the corresponding YOLO format `.txt` files for each image.

## Contributing

Contributions are welcome! If you have any ideas, bug reports, or suggestions, feel free to open an issue or create a pull request on the [GitHub repository](https://github.com/yourusername/yolo_formatter).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for simpler, automated dataset structuring for YOLO and other deep learning models.
- Built with love for the computer vision community.

## Contact

For any questions or feedback, feel free to reach out to the [author](mailto:your_email@example.com).

