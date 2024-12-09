import sys
from .hash_utils import find_matching_hash, verify_hash

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

