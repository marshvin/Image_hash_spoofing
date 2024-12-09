from PIL import Image
import io
import sys
import hashlib
from typing import Optional
from .png_modifier import modify_png_get_hash
import time
import random

def find_matching_hash(image_path, target_prefix, output_path):
    """Find a modified version of the image with desired hash prefix"""
    # Read original image and convert to PNG in memory
    with Image.open(image_path) as img:
        # Convert to PNG format in memory
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        original_bytes = img_byte_arr.getvalue()
    
    # Remove '0x' prefix if present
    target_prefix = target_prefix.lower().replace('0x', '')
    
    # Validate prefix length
    prefix_bits = len(target_prefix) * 4
    if prefix_bits > 32:
        raise ValueError(f"Target prefix length ({prefix_bits} bits) is too long. "
                        "Keep it under 32 bits (8 hex characters) for reasonable performance.")
    
    # Add a progress counter and time tracking
    start_time = time.time()
    attempt = 0
    tried_values = set()
    
    while True:
        attempt += 1
        # Use random values instead of sequential
        current_try = random.randint(1, 1000000)
        while current_try in tried_values:
            current_try = random.randint(1, 1000000)
        tried_values.add(current_try)
        
        modified_bytes, hash_result = modify_png_get_hash(original_bytes, current_try)
        
        # Print progress every 1000 attempts with estimated speed
        if attempt % 1000 == 0:
            elapsed_time = time.time() - start_time
            speed = attempt / elapsed_time
            print(f"Tried {attempt} combinations... ({speed:.1f} attempts/sec)")
        
        # Check if we found a match
        if hash_result.startswith(target_prefix):
            print(f"\nFound match after {attempt} attempts!")
            with open(output_path, 'wb') as f:
                f.write(modified_bytes)
            return hash_result
        
        # Optional: Add a timeout condition
        if attempt >= 1000000:  # Limit to 1 million attempts
            raise TimeoutError("Could not find matching hash after 1 million attempts")

def verify_hash(filepath):
    """Verify the hash of the output file"""
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha512(f.read()).hexdigest()
    print(f"SHA-512: {file_hash}")
    return file_hash
