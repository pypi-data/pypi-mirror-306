import os
import shutil
from sklearn.model_selection import train_test_split
from typing import List, Tuple

class YOLODatasetFormatter:
    def __init__(self, parent_dir: str, output_dir: str = "Data", train_ratio: float = 0.8, val_ratio: float = 0.1, test_ratio: float = 0.1):
        self.parent_dir = parent_dir
        self.output_dir = output_dir
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.image_exts = {".jpg", ".jpeg", ".png"}
        self.create_output_structure()
    
    def create_output_structure(self):
        """Create the YOLO output structure in a new 'Data' folder outside the parent directory."""
        os.makedirs(os.path.join(self.output_dir, 'train', 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'train', 'labels'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'val', 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'val', 'labels'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'test', 'images'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'test', 'labels'), exist_ok=True)
    
    def gather_images_and_labels(self) -> List[Tuple[str, str]]:
        """Collects all images and their corresponding label files if they exist."""
        image_label_pairs = []
        for root, _, files in os.walk(self.parent_dir):
            for file in files:
                if os.path.splitext(file)[1].lower() in self.image_exts:
                    image_path = os.path.join(root, file)
                    label_path = os.path.splitext(image_path)[0] + ".txt"
                    if os.path.exists(label_path):  # Ensure label file exists
                        image_label_pairs.append((image_path, label_path))
        return image_label_pairs
    
    def split_data(self, image_label_pairs: List[Tuple[str, str]]) -> Tuple[List, List, List]:
        """Split data into train, val, and test sets."""
        train_val, test = train_test_split(image_label_pairs, test_size=self.test_ratio, random_state=42)
        train, val = train_test_split(train_val, test_size=self.val_ratio / (self.train_ratio + self.val_ratio), random_state=42)
        return train, val, test

    def copy_files(self, dataset: List[Tuple[str, str]], subset: str):
        """Copy images and labels to the designated train/val/test folders."""
        for image_path, label_path in dataset:
            subset_image_dir = os.path.join(self.output_dir, subset, "images")
            subset_label_dir = os.path.join(self.output_dir, subset, "labels")
            shutil.copy(image_path, subset_image_dir)
            shutil.copy(label_path, subset_label_dir)
    
    def format_dataset(self):
        """Organize the dataset in YOLO format."""
        image_label_pairs = self.gather_images_and_labels()
        
        # Split into train, val, and test sets
        train, val, test = self.split_data(image_label_pairs)
        
        # Copy files to the appropriate folders
        self.copy_files(train, "train")
        self.copy_files(val, "val")
        self.copy_files(test, "test")
        
        print(f"Dataset has been organized in '{self.output_dir}' with the following structure:")
        print(f" - {len(train)} images in 'train'")
        print(f" - {len(val)} images in 'val'")
        print(f" - {len(test)} images in 'test'")
    
    def execute(self):
        """Run all necessary steps to organize the dataset for YOLO."""
        self.format_dataset()
