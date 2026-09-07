# This python program breaks a single FEN encoded chess board image into 64 square images.
# For each type of square (13 in total: P,R,B,N,Q,K,p,r,b,n,q,k, empty), it creates a subfolder
# and stores the cropped image in that folder.

import os
import argparse
from PIL import Image

# Map characters to meaningful folder names (optional, but keeps things organized)
PIECE_NAMES = {
    'r': 'black_rook', 'n': 'black_knight', 'b': 'black_bishop', 'q': 'black_queen', 'k': 'black_king', 'p': 'black_pawn',
    'R': 'white_rook', 'N': 'white_knight', 'B': 'white_bishop', 'Q': 'white_queen', 'K': 'white_king', 'P': 'white_pawn',
    '_': 'empty'
}

def expand_fen_string(fen_filename):
    """
    Converts a FEN filename into a flat list of 64 characters.
    Example: '8-8-8...' becomes ['_', '_', '_', ...]
    """
    # Remove the file extension
    fen_str = os.path.splitext(fen_filename)[0]
    
    board_squares = []
    # Kaggle dataset I'm using has '-' to separate rows in filenames
    rows = fen_str.split('-') 
    
    for row in rows:
        for char in row:
            if char.isdigit():
                # If it's a number, it represents that many empty squares
                board_squares.extend(['_'] * int(char))
            else:
                # Otherwise, it's a piece
                board_squares.append(char)
                
    return board_squares

def process_boards(input_dir, output_dir):
    image_count = 0
    square_count = 0

    # Use os.walk to recursively search all subdirectories
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            img_path = os.path.join(root, filename)
            
            # Calculate the relative path (e.g., 'train' or 'test') to maintain structure
            rel_path = os.path.relpath(root, input_dir)
            
            try:
                # 1. Extract the 64 labels from the filename
                labels = expand_fen_string(filename)
                
                if len(labels) != 64:
                    print(f"Skipping {filename}: FEN did not expand to exactly 64 squares.")
                    continue
                    
                # 2. Open and prep the image
                img = Image.open(img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                width, height = img.size
                sq_width = width // 8
                sq_height = height // 8
                
                # 3. Crop the image into an 8x8 grid
                square_idx = 0
                for row in range(8):
                    for col in range(8):
                        # Define the bounding box for the current square (left, upper, right, lower)
                        left = col * sq_width
                        upper = row * sq_height
                        right = (col + 1) * sq_width
                        lower = (row + 1) * sq_height
                        
                        square_img = img.crop((left, upper, right, lower))
                        
                        # 4. Determine the label and save path
                        piece_char = labels[square_idx]
                        class_name = PIECE_NAMES[piece_char]
                        
                        # Dynamically create the target directory preserving train/test split
                        target_dir = os.path.join(output_dir, rel_path, class_name)
                        os.makedirs(target_dir, exist_ok=True)
                        
                        # Create a unique filename for the square 
                        # (e.g., rnbqkbnr-pppppppp-8-8-8-8-PPPPPPPP-RNBQKBNR_sq05_white_pawn.jpg)
                        # The initial FEN chars also preserve the orig file from which this 
                        # cropped image was created - for cross-reference just in case.
                        base_name = os.path.splitext(filename)[0]
                        sq_filename = f"{base_name}_sq{square_idx:02d}_{class_name}.jpg"
                        sq_save_path = os.path.join(target_dir, sq_filename)
                        
                        square_img.save(sq_save_path)
                        
                        square_idx += 1
                        square_count += 1
                        
                image_count += 1
                if image_count % 100 == 0:
                    print(f"Processed {image_count} boards ({square_count} squares)...")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"\nDone! Processed {image_count} boards into {square_count} individual squares.")

def main():
    parser = argparse.ArgumentParser(description="Crop chessboard images into 64 labeled squares.")
    parser.add_argument("--dir", required=True, help="Path to your resized boards (e.g., ../Compressed-Dataset)")
    parser.add_argument("--out", required=True, help="Path to save the cropped squares (e.g., ../Grid-Dataset)")
    
    args = parser.parse_args()
    process_boards(args.dir, args.out)

if __name__ == "__main__":
    main()
