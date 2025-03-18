import argparse
import os

# Set environment variable for MPS fallback to CPU
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

# Import utilities from our modules
from utils.environment import ensure_venv, BLUE, ENDC
from utils.image_processing import remove_bg_single, process_directory


def main():
    """Main function to handle command-line arguments and execute the program."""
    # Try to ensure we're running in the virtual environment
    ensure_venv()

    parser = argparse.ArgumentParser(description='RMBG-2.0 Background Removal CLI')
    parser.add_argument('--input', '-i', help='Input image path, URL, or directory (default: current directory)')
    parser.add_argument('--output', '-o', help='Output image path or directory (default: input_path/remove_bg/)')
    parser.add_argument('--url', action='store_true', help='Treat input as URL')

    args = parser.parse_args()

    # If no input is provided, use the current directory
    if not args.input:
        args.input = os.getcwd()
        print(f"{BLUE}No input specified, using current directory: {args.input}{ENDC}")

    # Set default output directory if not specified
    if not args.output:
        if os.path.isdir(args.input) and not args.url:
            args.output = os.path.join(args.input, 'remove_bg')
        else:
            input_dir = os.path.dirname(args.input) if os.path.dirname(args.input) else '.'
            filename = os.path.basename(args.input)
            output_filename = os.path.splitext(filename)[0] + '.png'
            args.output = os.path.join(input_dir, 'remove_bg', output_filename)

    # Process directory or single image
    if os.path.isdir(args.input) and not args.url:
        print(f"{BLUE}Processing directory: {args.input}{ENDC}")
        print(f"{BLUE}Output directory: {args.output}{ENDC}")
        process_directory(args.input, args.output)
    else:
        print(f"{BLUE}Output path: {args.output}{ENDC}")
        remove_bg_single(args.input, args.output, args.url)


if __name__ == "__main__":
    main()
