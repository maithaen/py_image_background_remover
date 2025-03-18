import os
import torch
import requests
from PIL import Image
from io import BytesIO
from torchvision import transforms
import glob
from tqdm import tqdm
from colorama import Fore, Style, init  # Import colorama
from utils.model import load_model, initialize_model

# Initialize colorama
init()


def process_image(input_image, model, device):
    """
    Process an image to remove its background.

    Args:
        input_image (PIL.Image): Input image.
        model: Pretrained model.
        device: Computing device.
    Returns:
        PIL.Image: Image with transparent background, or None if processing fails.
    """
    if input_image is None:
        return None

    # Image preprocessing
    transform = transforms.Compose([
        transforms.Resize((1024, 1024)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    # Convert to tensor and move to device
    img_tensor = transform(input_image).unsqueeze(0).to(device)

    # Predict segmentation mask
    with torch.no_grad():
        pred = model(img_tensor)[-1].sigmoid().cpu()

    # Convert mask to PIL Image
    mask = transforms.ToPILImage()(pred[0].squeeze())
    mask = mask.resize(input_image.size)

    # Create new image with transparent background
    result = Image.new('RGBA', input_image.size, (0, 0, 0, 0))
    input_image = input_image.convert('RGBA')
    result.paste(input_image, (0, 0), mask=mask)

    return result


def load_image(input_path, is_url, verbose):
    if is_url:
        if verbose:
            print(f"{Fore.BLUE}Downloading image from URL: {input_path}{Style.RESET_ALL}")
        try:
            response = requests.get(input_path)
            return Image.open(BytesIO(response.content)).convert('RGB')
        except Exception as e:
            if verbose:
                print(f"{Fore.RED}Error downloading image: {e}{Style.RESET_ALL}")
            return None
    else:
        if verbose:
            print(f"{Fore.BLUE}Processing image: {input_path}{Style.RESET_ALL}")
        try:
            return Image.open(input_path).convert('RGB')
        except Exception as e:
            if verbose:
                print(f"{Fore.RED}Error opening image: {e}{Style.RESET_ALL}")
            return None


def save_image(output_path, result, verbose):
    try:
        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        result.save(output_path, format='PNG')
        if verbose:
            print(f"{Fore.GREEN}Saved to: {output_path}{Style.RESET_ALL}")
        return True
    except Exception as e:
        if verbose:
            print(f"{Fore.RED}Error saving output image: {e}{Style.RESET_ALL}")
        return False


def remove_bg_single(input_path, output_path, is_url=False, model=None, device=None, verbose=True):
    input_image = load_image(input_path, is_url, verbose)
    if input_image is None:
        return False

    model, device = initialize_model(model, device, verbose)

    result = process_image(input_image, model, device)

    if result:
        return save_image(output_path, result, verbose)
    else:
        if verbose:
            print(f"{Fore.RED}Failed to process image{Style.RESET_ALL}")
        return False


def process_directory(input_dir, output_dir):
    """
    Process all images in a directory with a progress bar.

    Args:
        input_dir (str): Directory containing input images.
        output_dir (str): Directory to save output images.
    Returns:
        bool: True if any images were processed successfully, False otherwise.
    """
    # Get all image files in the directory
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_dir, ext)))
        image_files.extend(glob.glob(os.path.join(input_dir, ext.upper())))

    if not image_files:
        print(f"{Fore.YELLOW}No image files found in {input_dir}{Style.RESET_ALL}")
        return False

    # Create output directory only if there are images to process
    os.makedirs(output_dir, exist_ok=True)

    print(f"{Fore.BLUE}Found {len(image_files)} images to process{Style.RESET_ALL}")

    # Load model once for all images
    model, device = load_model(verbose=True)

    # Process each image with progress bar
    success_count = 0
    for img_path in tqdm(image_files, desc="Processing images"):
        filename = os.path.basename(img_path)
        output_filename = os.path.splitext(filename)[0] + '.png'
        output_path = os.path.join(output_dir, output_filename)

        success = remove_bg_single(img_path, output_path, model=model, device=device, verbose=False)
        if success:
            success_count += 1
        else:
            tqdm.write(f"{Fore.RED}Failed to process {img_path}{Style.RESET_ALL}")

    print(f"{Fore.GREEN}Successfully processed {success_count} out of {len(image_files)} images{Style.RESET_ALL}")
    return success_count > 0
