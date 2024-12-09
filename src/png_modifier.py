import zlib
from typing import Tuple
import hashlib

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