import json
import cv2
import numpy as np
import os
from random import choice, shuffle, choices

class AnnotationProcessor:
    def __init__(self, cvat_root, cvat_dataset_names,split,output_path):
        self.cvat_root = cvat_root
        self.cvat_dataset_names = cvat_dataset_names
        self.split=split
        self.cvat_train = []
        self.cvat_valid = []
        self.output_path=output_path

    def load_frames(self, name):
        """Load frames from annotation file and divide into training and validation sets."""
        print("Adding", name)
        frames = self.read_annotation_frames(f"{self.cvat_root}/{name}/annotations/default.json", f"{self.cvat_root}/{name}/images/default/")
        n = round(len(frames) * self.split)
        self.cvat_train += frames[:n]
        self.cvat_valid += frames[n:]

    def save_frames_to_coco_dataset(self, frames, coco_result_path):
        """Save frames in COCO format."""
        annotations = []
        images = []

        for frame in frames:
            nice_annots = frame.get_nice_keypoints()
            for annot in nice_annots:
                annotations.append({
                    "id": len(annotations),
                    "category_id": 1,
                    "num_keypoints": 7,
                    "score": 1.0,
                    "area": annot['bbox'][2] * annot['bbox'][3],
                    "image_id": len(images),
                    "bbox": annot['bbox'],
                    "keypoints": annot['keypoints']
                })
            images.append({
                "id": len(images),
                "file_name": frame.image_info['path'],
                "height": frame.image_info['size'][0],
                "width": frame.image_info['size'][1],
            })

        categories = [{
            "id": 1,
            "name": "mouse",
            "supercategory": "mouse",
            "keypoints": [
                "nose_tip", "right_ear", "left_ear", "neck", "right_side_body", "left_side_body", "tail_base"
            ],
            "skeleton": [
                [0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [3, 5], [4, 6], [5, 6]
            ]
        }]

        shuffle(annotations)
        coco_res = {
            "info": {"description": "mouse pose estimation dataset"},
            "licenses": [],
            "images": images,
            "annotations": annotations,
            "categories": categories,
        }

        with open(f'{coco_result_path}_annotation.json', 'w') as f:
            json.dump(annotations, f)
        with open(f'{coco_result_path}.json', 'w') as f:
            json.dump(coco_res, f)

    @staticmethod
    def read_annotation_frames(json_path, img_root):
        """Read frames from annotation file."""
        with open(json_path) as f:
            datum = json.load(f)
        dtframes = []
        for item in datum['items']:
            dtframes.append(DataumFrame(
                img_info=item['image'],
                img_root_path=img_root,
                dataum_annotations=item['annotations'],
            ))
        return dtframes

    @staticmethod
    def read_coco_as_frames(json_path, img_root=None):
        """Read COCO dataset as frames."""
        with open(json_path) as f:
            coco = json.load(f)

        frames = {}
        for img in coco['images']:
            frames[img['id']] = {
                "image": {
                    "size": (img['height'], img['width']),
                    "path": img['file_name'],
                },
                "nice_keypoints": []
            }

        for annot in coco['annotations']:
            image_id = annot['image_id']
            frames[image_id]['nice_keypoints'].append({
                'keypoints': annot['keypoints'],
                'bbox': annot['bbox'],
            })

        dtframes = []
        for frame in frames.values():
            dtframes.append(DataumFrame(
                img_info=frame['image'],
                img_root_path=img_root,
                nice_keypoints=frame['nice_keypoints'],
            ))
        return dtframes

    def generate_random_samples(self, frames, output_path, k=10):
        """Generate random samples with bounding boxes and keypoints and save images."""
        sampled_frames = choices(frames, k=k)
        for i, frame in enumerate(sampled_frames):
            img = cv2.imread(frame.image_info['path'])
            for obj in frame.nice_keypoints:
                x, y, w, h = obj['bbox']
                cv2.rectangle(img, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 1)
                kps = np.array(obj['keypoints']).reshape((-1, 3)).astype(np.int32)
                for point in kps[:, :2]:
                    img = cv2.circle(img, tuple(point), 2, (0, 0, 255), -1)
            cv2.imwrite(f"{output_path}/random_sample_{i:02d}.jpg", img)

    @staticmethod
    def trim_annotation(data):
        """Trim a dictionary to reduce long lists for preview purposes."""
        def trimmer(d):
            if isinstance(d, list):
                if len(d) > 20:
                    d = d[:2] + ["..."]
                for i in range(len(d)):
                    d[i] = trimmer(d[i])
            elif isinstance(d, dict):
                for k in d:
                    d[k] = trimmer(d[k])
            return d
        return trimmer(data)

    @staticmethod
    def plot_mouse(mouse, img, color):
        """Plot mouse keypoints and bounding box on an image."""
        xs = np.array(mouse['x']).astype(np.int32)
        ys = np.array(mouse['y']).astype(np.int32)
        ps = np.array(list(zip(xs, ys)))

        bbox = cv2.boundingRect(ps)
        pad = 0.10
        x, y, w, h = bbox
        pw, ph = int(w * pad), int(h * pad)
        x -= pw
        y -= ph
        w += pw * 2
        h += ph * 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        for point in ps:
            img = cv2.circle(img, tuple(point), 2, color, -1)
        return img

    def process_datasets(self):
        """Process all datasets for training and validation."""
        for name in self.cvat_dataset_names:
            self.load_frames(name)
        print("cvat_train", len(self.cvat_train))
        print("cvat_valid", len(self.cvat_valid))
        self.save_frames_to_coco_dataset(self.cvat_train, f"{self.output_path}/coco_train")
        self.save_frames_to_coco_dataset(self.cvat_valid, f"{self.output_path}/coco_valid")



