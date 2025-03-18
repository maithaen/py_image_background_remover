import torch
from transformers import AutoModelForImageSegmentation
from colorama import Fore, Style, init  # Import colorama

# Initialize colorama
init()


def load_model(verbose=True):
    """
    Load the RMBG-2.0 model and set the device.

    Args:
        verbose (bool): Whether to print status messages.
    Returns:
        tuple: (model, device)
    """
    if verbose:
        print(f"{Fore.BLUE}Loading RMBG-2.0 model...{Style.RESET_ALL}")
    model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
    # Use CUDA if available, MPS if available (M1/M2 Mac), otherwise CPU
    device = torch.device('cuda' if torch.cuda.is_available() else
                          ('mps' if torch.backends.mps.is_available() else 'cpu'))

    # Print device information with color
    if torch.cuda.is_available():
        if verbose:
            print(f"{Fore.BLUE}Using CUDA device: {torch.cuda.get_device_name(0)}{Style.RESET_ALL}")
    elif torch.backends.mps.is_available():
        if verbose:
            print(f"{Fore.BLUE}Using MPS (Apple Silicon GPU){Style.RESET_ALL}")
    else:
        if verbose:
            print(f"{Fore.YELLOW}Using CPU for processing (this may be slow){Style.RESET_ALL}")

    model.to(device)
    model.eval()
    return model, device


def initialize_model(model, device, verbose):
    if model is None or device is None:
        return load_model(verbose=verbose)
    return model, device
