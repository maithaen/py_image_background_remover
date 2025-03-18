# Python CLI Tool for AI Image Background Removal

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Remove background from a single image:
```bash
python main.py -i input_image.jpg -o output_image.jpg
```

Process all images in a folder:
```bash
python main.py -i input/folder/path
```

## GPU Acceleration (CUDA)

To enable GPU acceleration, first remove existing PyTorch installation:
```bash
pip uninstall torch torchvision -y
```

Then install CUDA-enabled PyTorch:
```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
```
