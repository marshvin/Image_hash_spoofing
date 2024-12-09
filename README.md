# Hash Spoofing Tool

## Overview

The Hash Spoofing Tool is a Python script that modifies PNG images to generate a specific SHA-512 hash prefix. This tool is useful for demonstrating how image metadata can be manipulated to achieve desired hash values.

## Features

- Modify PNG metadata by adding custom chunks.
- Generate a modified image with a specified SHA-512 hash prefix.
- Verify the hash of the modified image.

## Requirements

- Python 3.x
- Pillow library (for image processing)

You can install the required library using pip:

pip install Pillow

## Usage

To use the Hash Spoofing Tool, run the following command in your terminal:

python hash_spoof.py <target_prefix> <input_image> <output_image>

- `<target_prefix>`: The desired prefix for the SHA-512 hash.
- `<input_image>`: The path to the input PNG image.
- `<output_image>`: The path where the modified image will be saved.

### Example

spoof 0x1234abcd input.png output.png

## Functions

### `modify_png_get_hash(image_bytes, current_attempt)`

This function modifies the PNG metadata by adding a custom chunk and returns the modified image bytes along with its SHA-512 hash.

- **Parameters**:
  - `image_bytes`: The original image bytes.
  - `current_attempt`: The current attempt number used for generating the custom chunk.

- **Returns**: A tuple containing the modified image bytes and the SHA-512 hash.

### `find_matching_hash(image_path, target_prefix, output_path)`

This function attempts to find a modified version of the image that matches the desired hash prefix.

- **Parameters**:
  - `image_path`: The path to the original image.
  - `target_prefix`: The desired hash prefix.
  - `output_path`: The path where the modified image will be saved.

- **Returns**: The SHA-512 hash of the modified image if a match is found.

### `verify_hash(filepath)`

This function verifies the SHA-512 hash of the output file.

- **Parameters**:
  - `filepath`: The path to the modified image file.

- **Returns**: The SHA-512 hash of the file.

### `main()`

The main function that orchestrates the execution of the tool. It handles command-line arguments, calls the necessary functions, and manages error handling.

## Running the Tool

Invoke the tool on Unix-based systems using the following syntax:

```bash
spoof 0x1234abcd input.png output.png
```

By default, you'll need to run the tool with ./spoof. To make it available globally (run without ./), you have two options:

Option 1: Create a Symbolic Link

# Create a symbolic link to the spoof tool
```bash
sudo ln -s "$(pwd)/spoof" /usr/local/bin/spoof
```
# Make the tool executable
```bash
sudo chmod +x /usr/local/bin/spoof
```

Option 2: Copy the Script
# Copy the spoof tool to system-wide bin directory
```bash
sudo cp spoof /usr/local/bin/
```
# Make the tool executable
```bash
sudo chmod +x /usr/local/bin/spoof
```
## Acknowledgments

- [Pillow](https://python-pillow.org/) for image processing capabilities.
