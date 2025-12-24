# Image Format Converter

A powerful and flexible Python script for batch converting images between different formats. Built on ImageMagick/Wand, it supports a wide range of image formats and provides options for resizing and quality control.

## Features

- **Batch Conversion**: Convert all images of a specific format in a folder at once
- **Format Support**: Works with any format ImageMagick supports (SVG, PNG, JPG, WEBP, GIF, BMP, TIFF, PDF, and more)
- **Non-Destructive**: Keeps original files intact and creates copies in the new format
- **Resizing**: Optional resizing during conversion (width, height, or both)
- **Quality Control**: Adjust compression quality for lossy formats (JPEG, WEBP)
- **Progress Tracking**: Clear feedback on conversion progress and success/failure status
- **Cross-Platform**: Works on macOS, Linux, and Windows

## Prerequisites

### 1. Python 3
The script requires Python 3.6 or later.

### 2. ImageMagick
Install ImageMagick using your system's package manager:

**macOS (Homebrew):**
```bash
brew install imagemagick
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install imagemagick libmagickwand-dev
```

**Linux (Fedora):**
```bash
sudo dnf install ImageMagick ImageMagick-devel
```

**Windows:**
Download and install from [ImageMagick's official website](https://imagemagick.org/script/download.php)

### 3. Wand Python Library
Install the Wand library:
```bash
pip3 install wand
```

## Installation

1. Download the script:
```bash
curl -O https://raw.githubusercontent.com/your-repo/convert_images.py
```

2. Make it executable (macOS/Linux):
```bash
chmod +x convert_images.py
```

3. Optionally, move it to your PATH for global access:
```bash
sudo mv convert_images.py /usr/local/bin/convert_images
```

## Usage

### Basic Syntax
```bash
python3 convert_images.py [folder] --from INPUT_FORMAT --to OUTPUT_FORMAT [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `folder` | No | Path to folder containing images (default: current directory) |
| `--from` | Yes | Input format (e.g., svg, png, jpg, webp) |
| `--to` | Yes | Output format (e.g., png, jpg, webp, svg) |
| `--width` | No | Output width in pixels |
| `--height` | No | Output height in pixels |
| `--quality` | No | Output quality for lossy formats (1-100) |

### Examples

#### Convert SVG to PNG
```bash
python3 convert_images.py --from svg --to png
```

#### Convert JPG to WEBP with Quality Control
```bash
python3 convert_images.py --from jpg --to webp --quality 85
```

#### Convert PNG to JPG in Specific Folder
```bash
python3 convert_images.py /path/to/images --from png --to jpg
```

#### Convert and Resize
```bash
python3 convert_images.py --from svg --to png --width 1024
```

#### Convert with Both Dimensions
```bash
python3 convert_images.py --from png --to jpg --width 1920 --height 1080
```

#### Convert with Aspect Ratio Preservation
Specify only width OR height to maintain aspect ratio:
```bash
python3 convert_images.py --from jpg --to webp --width 800 --quality 90
```

## Supported Formats

The script supports any format that ImageMagick supports, including:

### Common Formats
- **Raster**: PNG, JPG/JPEG, WEBP, GIF, BMP, TIFF, ICO
- **Vector**: SVG, EPS, PDF
- **RAW**: CR2, NEF, ARW, DNG (camera raw formats)
- **Other**: PSD (Photoshop), XCF (GIMP), and many more

### Format-Specific Notes

**SVG to Raster (PNG/JPG/WEBP):**
- Vector graphics are rasterized at a default resolution
- Use `--width` and `--height` to control output size
- Higher dimensions = better quality but larger file size

**Raster to SVG:**
- Creates traced/bitmap-embedded SVG
- Not recommended for photos (use vector sources when possible)

**WEBP:**
- Modern format with excellent compression
- Use `--quality 80-90` for good balance between size and quality

**JPEG:**
- Lossy format, best for photos
- Use `--quality 85-95` for high quality
- Not suitable for images requiring transparency

**PNG:**
- Lossless format with transparency support
- Best for graphics, logos, screenshots
- Larger file sizes than JPEG/WEBP

## How It Works

1. **Discovery**: Scans the specified folder for files matching the input format
2. **Validation**: Checks if the folder exists and contains matching files
3. **Conversion**: Processes each image using ImageMagick via the Wand library
4. **Output**: Creates new files with the target format extension
5. **Reporting**: Shows success/failure status for each file

### Auto-Detection on macOS
The script automatically detects ImageMagick installed via Homebrew and sets the necessary environment variables (`MAGICK_HOME` and `DYLD_LIBRARY_PATH`).

## Troubleshooting

### "Could not import Wand library"
**Solution:**
1. Install Wand: `pip3 install wand`
2. Install ImageMagick: `brew install imagemagick` (macOS) or equivalent for your OS

### "MAGICK_HOME not set" errors
**Solution (macOS):**
```bash
export MAGICK_HOME=$(brew --prefix imagemagick)
export DYLD_LIBRARY_PATH="$MAGICK_HOME/lib:$DYLD_LIBRARY_PATH"
```

**Solution (Linux):**
```bash
export MAGICK_HOME=/usr
```

### No files found
**Common causes:**
- Wrong folder path
- Incorrect input format (case-sensitive on some systems)
- Files have different extensions than specified

### Conversion failures
**Common causes:**
- Corrupted input files
- Unsupported format combinations
- Insufficient permissions
- Disk space issues

## Performance Considerations

- **Large batches**: Processing hundreds of images may take time
- **High resolution**: SVG to raster conversions with large dimensions are slower
- **Quality settings**: Higher quality = slower conversion and larger files
- **Format complexity**: Vector to raster is faster than raster to vector

## Use Cases

### Web Development
```bash
# Optimize images for web
python3 convert_images.py images/ --from png --to webp --quality 85
```

### Icon Generation
```bash
# Create PNGs from SVG icons
python3 convert_images.py icons/ --from svg --to png --width 512
```

### Photo Optimization
```bash
# Convert and compress photos
python3 convert_images.py photos/ --from jpg --to webp --quality 90 --width 1920
```

### Archive Conversion
```bash
# Convert old formats to modern ones
python3 convert_images.py archive/ --from bmp --to png
```

## Advanced Usage

### Integration with Shell Scripts
```bash
#!/bin/bash
for dir in images/*; do
    python3 convert_images.py "$dir" --from jpg --to webp --quality 85
done
```

### Automation with Cron
```bash
# Add to crontab to convert images daily
0 2 * * * /usr/bin/python3 /path/to/convert_images.py /path/to/images --from svg --to png
```

## Safety Features

- **Non-destructive**: Original files are never modified or deleted
- **Error handling**: Individual file failures don't stop the batch process
- **Validation**: Checks folder existence and file availability before processing
- **Clear reporting**: Shows exactly which files succeeded and which failed

## Contributing

Issues, improvements, and pull requests are welcome. Some ideas for enhancements:
- Recursive folder processing
- Output to a different directory
- Preserve/modify EXIF data
- Batch rename functionality
- GUI interface

## License

This script is provided as-is for personal and commercial use.

## Credits

Built by [Nerdy South Inc](https://www.nerdysouthinc.com/)

Powered by:
- [ImageMagick](https://imagemagick.org/) - Image processing engine
- [Wand](https://docs.wand-py.org/) - Python bindings for ImageMagick

## Version

Current version: 1.0.0

Last updated: 2025-12-23
