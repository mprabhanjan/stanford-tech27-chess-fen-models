import os
import argparse
from PIL import Image

def process_images(input_dir, output_dir, size):
    # Ensure the base output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Walk through the directory tree
    for root, _, files in os.walk(input_dir):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(root, filename)
                
                # Maintain the original subdirectory structure in the output folder
                rel_path = os.path.relpath(root, input_dir)
                target_dir = os.path.join(output_dir, rel_path)
                os.makedirs(target_dir, exist_ok=True)
                
                try:
                    img = Image.open(img_path)
                    
                    # Convert to RGB to prevent errors if saving RGBA (PNG) as JPEG
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Resize the image
                    img_resized = img.resize((size, size), Image.Resampling.LANCZOS)
                    
                    # Save to the new destination
                    output_path = os.path.join(target_dir, filename)
                    img_resized.save(output_path)
                    
                except Exception as e:
                    print(f"Error processing {img_path}: {e}")

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Batch resize image datasets.")
    parser.add_argument("--dir", required=True, help="Path to the original images directory")
    parser.add_argument("--out", required=True, help="Path where resized images will be saved")
    parser.add_argument("--size", type=int, required=True, help="Target size for width and height (e.g., 200)")
    
    args = parser.parse_args()
    
    print(f"Starting batch resize to {args.size}x{args.size}...")
    process_images(args.dir, args.out, args.size)
    print(f"Done! Resized images are saved in '{args.out}'.")

if __name__ == "__main__":
    main()
