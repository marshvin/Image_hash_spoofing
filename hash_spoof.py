import sys
import hashlib
from PIL import Image
import io
import random
import zlib

def modify_png_get_hash(image_bytes, current_attempt):
    """Modify PNG metadata and return new bytes and hash"""
    # Create a copy of the image bytes
    new_bytes = bytearray(image_bytes)
    
    # Find the IEND chunk (last chunk in PNG)
    iend_index = new_bytes.rfind(b'IEND')
    if iend_index == -1:
        raise ValueError("Invalid PNG: No IEND chunk found")
    
    # Insert custom metadata chunk before IEND
    # Using 'prVt' as custom chunk type (private ancillary chunk)
    chunk_type = b'prVt'
    chunk_data = str(current_attempt).encode('utf-8')
    chunk_length = len(chunk_data)
    
    # Calculate CRC for the chunk
    crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
    
    # Construct the complete chunk
    new_chunk = (
        chunk_length.to_bytes(4, 'big') +
        chunk_type +
        chunk_data +
        crc.to_bytes(4, 'big')
    )
    
    # Insert the new chunk before IEND
    new_bytes[iend_index:iend_index] = new_chunk
    
    # Calculate SHA-512 hash of modified image
    return bytes(new_bytes), hashlib.sha512(new_bytes).hexdigest()

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
    
    attempt = 0
    while True:
        modified_bytes, hash_result = modify_png_get_hash(original_bytes, attempt)
        
        if hash_result.startswith(target_prefix):
            # Found a match! Save the modified image
            with open(output_path, 'wb') as f:
                f.write(modified_bytes)
            return hash_result
        
        attempt += 1
        if attempt % 1000 == 0:
            print(f"Tried {attempt} combinations...", file=sys.stderr)

def verify_hash(filepath):
    """Verify the hash of the output file"""
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha512(f.read()).hexdigest()
    print(f"SHA-512: {file_hash}")
    return file_hash

def main():
    if len(sys.argv) != 4:
        print("Usage: python hash_spoof.py <target_prefix> <input_image> <output_image>")
        sys.exit(1)
    
    target_prefix = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]
    
    try:
        final_hash = find_matching_hash(input_path, target_prefix, output_path)
        print(f"Success! Modified image saved to {output_path}")
        print(f"SHA-512: {final_hash}")
        verify_hash(output_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()