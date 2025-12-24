#!/usr/bin/env python3
"""
Convert all images in a folder from one format to another.
Keeps original files and creates copies in the new format.
Supports any format that ImageMagick supports (SVG, PNG, JPG, WEBP, GIF, etc.)
"""

import os
import sys
from pathlib import Path
import subprocess

# Set MAGICK_HOME to help wand find ImageMagick
if 'MAGICK_HOME' not in os.environ:
    # Try to find ImageMagick via brew
    try:
        result = subprocess.run(['brew', '--prefix', 'imagemagick'],
                              capture_output=True, text=True, check=True)
        magick_home = result.stdout.strip()
        os.environ['MAGICK_HOME'] = magick_home
        # Also set DYLD_LIBRARY_PATH for macOS
        lib_path = os.path.join(magick_home, 'lib')
        if 'DYLD_LIBRARY_PATH' in os.environ:
            os.environ['DYLD_LIBRARY_PATH'] = f"{lib_path}:{os.environ['DYLD_LIBRARY_PATH']}"
        else:
            os.environ['DYLD_LIBRARY_PATH'] = lib_path
    except:
        pass

try:
    from wand.image import Image as WandImage
except ImportError as e:
    print("Error: Could not import Wand library.")
    print(f"Details: {e}")
    print("\nTroubleshooting:")
    print("1. Install wand: pip3 install wand")
    print("2. Install ImageMagick: brew install imagemagick")
    print("\nIf both are installed, try setting MAGICK_HOME:")
    print("  export MAGICK_HOME=$(brew --prefix imagemagick)")
    sys.exit(1)


def convert_image(input_path, output_format, output_path=None, width=None, height=None, quality=None):
    """
    Convert a single image file to another format.

    Args:
        input_path: Path to the input image file
        output_format: Target format (e.g., 'png', 'jpg', 'webp', 'svg')
        output_path: Path for the output file (defaults to same name with new extension)
        width: Output width in pixels (optional)
        height: Output height in pixels (optional)
        quality: Output quality for lossy formats like JPEG/WEBP (1-100, optional)
    """
    if output_path is None:
        output_path = input_path.with_suffix(f'.{output_format.lower()}')

    try:
        with WandImage(filename=str(input_path)) as img:
            # Resize if dimensions specified
            if width or height:
                img.transform(resize=f'{width or ""}x{height or ""}')

            # Set quality for lossy formats
            if quality is not None:
                img.compression_quality = quality

            # Convert to target format
            img.format = output_format.lower()
            img.save(filename=str(output_path))
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def convert_all_images(folder_path, input_format, output_format, width=None, height=None, quality=None):
    """
    Convert all images of a specific format in a folder to another format.

    Args:
        folder_path: Path to the folder containing image files
        input_format: Source format (e.g., 'svg', 'png', 'jpg')
        output_format: Target format (e.g., 'png', 'jpg', 'webp')
        width: Output width in pixels (optional)
        height: Output height in pixels (optional)
        quality: Output quality for lossy formats (1-100, optional)
    """
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    if not folder.is_dir():
        print(f"Error: '{folder_path}' is not a directory.")
        return

    # Normalize format (remove leading dot if present)
    input_format = input_format.lower().lstrip('.')
    output_format = output_format.lower().lstrip('.')

    # Find all files with the input format
    pattern = f'*.{input_format}'
    image_files = list(folder.glob(pattern))

    if not image_files:
        print(f"No {input_format.upper()} files found in '{folder_path}'")
        return

    print(f"Found {len(image_files)} {input_format.upper()} file(s) in '{folder_path}'")
    print(f"Converting to {output_format.upper()}...")
    if width or height:
        print(f"Resizing to: {width or 'auto'}x{height or 'auto'}")
    if quality:
        print(f"Quality: {quality}")
    print()

    successful = 0
    failed = 0

    for image_file in image_files:
        print(f"  Converting: {image_file.name}... ", end='')
        if convert_image(image_file, output_format, width=width, height=height, quality=quality):
            print("✓")
            successful += 1
        else:
            print("✗")
            failed += 1

    print(f"\nConversion complete:")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert all images in a folder from one format to another",
        epilog="""
Examples:
  # Convert all SVG files to PNG
  python3 convert_images.py --from svg --to png

  # Convert all JPG files to WEBP with quality 85
  python3 convert_images.py --from jpg --to webp --quality 85

  # Convert all PNG files to JPG in a specific folder
  python3 convert_images.py /path/to/folder --from png --to jpg

  # Convert and resize all images
  python3 convert_images.py --from svg --to png --width 1024 --height 768

Supported formats include: svg, png, jpg, jpeg, webp, gif, bmp, tiff, pdf, and many more
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'folder',
        nargs='?',
        default='.',
        help='Folder containing image files (default: current directory)'
    )
    parser.add_argument(
        '--from',
        dest='input_format',
        required=True,
        help='Input format (e.g., svg, png, jpg, webp)'
    )
    parser.add_argument(
        '--to',
        dest='output_format',
        required=True,
        help='Output format (e.g., png, jpg, webp, svg)'
    )
    parser.add_argument(
        '--width',
        type=int,
        help='Output width in pixels (optional)'
    )
    parser.add_argument(
        '--height',
        type=int,
        help='Output height in pixels (optional)'
    )
    parser.add_argument(
        '--quality',
        type=int,
        help='Output quality for lossy formats like JPEG/WEBP (1-100, optional)'
    )

    args = parser.parse_args()

    convert_all_images(
        args.folder,
        args.input_format,
        args.output_format,
        width=args.width,
        height=args.height,
        quality=args.quality
    )
