#! /usr/bin/env python3

import os
import tarfile
import zipfile
import shutil
import glob
import numpy as np
from PIL import Image
from torch.utils.data import Dataset
from ..utils import common_functions as c_f


class Oxford102(Dataset):

    def __init__(self, root, transform=None, download=False):
        self.root = os.path.join(root, "oxford102")
        if download:
            try:
                self.set_paths_and_labels()
            except Exception:
                self.download_dataset()
                self.set_paths_and_labels()
        else:
            self.set_paths_and_labels()
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        path = self.img_paths[idx]
        img = Image.open(path).convert('RGB')
        label = self.labels[idx]
        if self.transform is not None:
            img = self.transform(img)
        return {"data": img, "label": label}

    def set_paths_and_labels(self, assert_files_exist=False):
        candidates = [
            os.path.join(self.root, '102 flower', 'flowers'),
            os.path.join(self.root, '102 flower'),
            os.path.join(self.root, 'flowers'),
            self.root,
        ]
        dataset_folder = None
        for c in candidates:
            if os.path.isdir(c):
                dataset_folder = c
                break
        if dataset_folder is None:
            raise RuntimeError('Could not find extracted Oxford102 files in {}'.format(self.root))

        split_dirs = []
        for name in ['train', 'valid', 'test']:
            p = os.path.join(dataset_folder, name)
            if os.path.isdir(p):
                split_dirs.append(p)

        class_names = set()
        img_paths = []
        labels = []

        # Gather class names from all split dirs
        for sd in split_dirs:
            for class_dir in os.listdir(sd):
                class_path = os.path.join(sd, class_dir)
                if os.path.isdir(class_path):
                    class_names.add(class_dir)

        class_names = sorted(list(class_names))
        class_to_idx = {c: i for i, c in enumerate(class_names)}

        # Collect images and labels
        exts = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
        for sd in split_dirs:
            for class_dir in os.listdir(sd):
                class_path = os.path.join(sd, class_dir)
                if not os.path.isdir(class_path):
                    continue
                idx = class_to_idx[class_dir]
                for ext in exts:
                    for img in glob.glob(os.path.join(class_path, ext)):
                        img_paths.append(img)
                        labels.append(idx)

        if len(img_paths) == 0:
            for class_dir in os.listdir(dataset_folder):
                class_path = os.path.join(dataset_folder, class_dir)
                if os.path.isdir(class_path):
                    if class_dir not in class_to_idx:
                        class_to_idx[class_dir] = len(class_to_idx)
                    idx = class_to_idx[class_dir]
                    for ext in exts:
                        for img in glob.glob(os.path.join(class_path, ext)):
                            img_paths.append(img)
                            labels.append(idx)

        if len(img_paths) == 0:
            raise RuntimeError('No images found for Oxford102 in {}'.format(dataset_folder))

        self.img_paths = img_paths
        self.labels = np.array(labels)
        self.class_names = class_names

        assert len(np.unique(self.labels)) == 102, 'Expected 102 classes, found {}'.format(len(np.unique(self.labels)))
        assert self.__len__() == 8189, 'Expected 8189 images, found {}'.format(self.__len__())

        if assert_files_exist:
            for p in self.img_paths:
                assert os.path.isfile(p)

    def download_dataset(self):
        c_f.makedir_if_not_there(self.root)
        try:
            import kagglehub
        except Exception as e:
            raise RuntimeError('kagglehub is required to download Oxford102 via this class. Install it and try again.') from e

        archive_or_folder = kagglehub.dataset_download("yousefmohamed20/oxford-102-flower-dataset")

        if archive_or_folder is None:
            archive_or_folder = os.getcwd()

        if os.path.isfile(archive_or_folder):
            if archive_or_folder.endswith('.zip'):
                with zipfile.ZipFile(archive_or_folder, 'r') as z:
                    z.extractall(self.root)
            else:
                with tarfile.open(archive_or_folder, 'r:*') as tar:
                    tar.extractall(path=self.root, members=c_f.extract_progress(tar))
        elif os.path.isdir(archive_or_folder):
            for entry in os.listdir(archive_or_folder):
                src = os.path.join(archive_or_folder, entry)
                dst = os.path.join(self.root, entry)
                if os.path.exists(dst):
                    continue
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
        else:
            raise RuntimeError('kagglehub returned unexpected path: {}'.format(archive_or_folder))
