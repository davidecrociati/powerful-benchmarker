import setuptools
import glob

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="powerful-benchmarker",
    version="0.9.33",
    author="Kevin Musgrave",
    description="A PyTorch library for benchmarking deep metric learning. It's powerful.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KevinMusgrave/powerful-benchmarker",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data = {'src/powerful_benchmarker': glob.glob("configs/**/*.yaml", recursive=True)},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=[
          'numpy == 1.19.2',
          'scikit-learn == 0.23.2',
          'torch == 1.6.0',
          'torchvision == 0.7.0',
          'easy-module-attribute-getter == 0.9.41',
          'record-keeper == 0.9.29',
          'tensorboard == 2.3.0',
          'matplotlib == 3.3.2',
          'pretrainedmodels ',
          'pytorch-metric-learning == 1.0.0',
          'pandas == 1.1.2',
          'ax-platform == 0.1.14',
          'faiss-gpu == 1.6.4',
          'gdown >= 3.12.0',
    ],
)
