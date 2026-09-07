# This python code finds and copies the original chess-board images 
# that were not used for the model traning or model-testing.
# The create_balanced_dataset.py took the original downsized images
# and decomposed it into a grid of 64 chess-square images.
# During that step, we retained the name of the orignal image
# from which the grid was generated. 
# Now we want to get a list of original images (i.e. non decomposed) 
# that were not used in the training or testing.


import os
import shutil
import argparse

def main():
    parser = argparse.ArgumentParser(description="Filter and copy unused full-board FEN images to prevent data leakage.")
    parser.add_argument('--grid_dir', required=True, help="Directory containing grid images (e.g., ./Downsized-Grid-Images-200/test)")
    parser.add_argument('--orig_dir', required=True, help="Directory containing original full downsized files")
    parser.add_argument('--target_dir', required=True, help="Destination directory for the unused files")
    parser.add_argument('--size', type=int, default=None, help="Maximum number of files to copy (optional)")
    
    args = parser.parse_args()

    # Define acceptable image extensions
    valid_exts = ('.jpg', '.jpeg', '.png')

    # Step 1: Build the "Do Not Use" set from the grid directory
    print(f"Scanning grid directory: {args.grid_dir}...")
    used_fens = set()
    
    for root, _, files in os.walk(args.grid_dir):
        for file in files:
            if file.lower().endswith(valid_exts):
                # The filename looks like: 1b1B1Qr1-7p-6r1..._sq01_black_bishop.jpg
                # We split at '_sq' to isolate the original FEN string
                if '_sq' in file:
                    fen_prefix = file.split('_sq')[0]
                    used_fens.add(fen_prefix)

    print(f"Found {len(used_fens)} unique FENs already used in the grid dataset.")

    # Step 2: Prepare the target directory
    os.makedirs(args.target_dir, exist_ok=True)

    # Step 3: Scan original directory and copy the safe files
    print(f"Scanning original directory: {args.orig_dir}...")
    copied_count = 0
    
    # Sort the files to ensure deterministic behavior across runs
    for file in sorted(os.listdir(args.orig_dir)):
        if file.lower().endswith(valid_exts):
            # The original filename looks like: 1b1B1Qr1-7p-6r1...jpeg
            # We separate the name from the extension to match against our set
            fen_prefix, _ = os.path.splitext(file)
            
            if fen_prefix not in used_fens:
                src_path = os.path.join(args.orig_dir, file)
                dest_path = os.path.join(args.target_dir, file)
                
                # copy2 preserves the original file metadata (timestamps, etc.)
                shutil.copy2(src_path, dest_path)
                copied_count += 1
                
                # Check if we hit the optional size limit
                if args.size and copied_count >= args.size:
                    print(f"\nReached the requested size limit of {args.size}.")
                    break
                    
    print(f"Success! Copied {copied_count} unused full-board images to {args.target_dir}.")

if __name__ == "__main__":
    main()
