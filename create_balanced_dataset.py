#This python code balances the images to reflect equal proportion.
#In the case of a chess board, even in a fully loaded board,
# there are only 16 out 64 squares occupied - rest are all empty.
# so if you left it as it is, there would be a heavy bias of the
# empty square images in the training data. 
# This code fixes that imbalance by picking equal amount of all
# pieces and empty squares for better traning quality dataset.

import os
import random
import shutil
import argparse

def create_balanced_dataset(input_dir, output_dir, train_samples, test_samples):
    # Find the top-level splits (e.g., 'train', 'test')
    splits = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d))]
    
    total_copied = 0
    
    for split in splits:
        split_in_path = os.path.join(input_dir, split)
        split_out_path = os.path.join(output_dir, split)
        
        # Find the class folders inside this specific split (e.g., white_pawn, empty)
        classes = [d for d in os.listdir(split_in_path) if os.path.isdir(os.path.join(split_in_path, d))]
        
        if not classes:
            continue
            
        print(f"\nProcessing '{split}' split...")
        
        # Apply the correct sample limit depending on the directory being processed
        samples_per_class = train_samples if split == 'train' else test_samples
        
        for cls in classes:
            class_in_path = os.path.join(split_in_path, cls)
            class_out_path = os.path.join(split_out_path, cls)
            
            os.makedirs(class_out_path, exist_ok=True)
            
            # Get all images in this class folder
            images = [f for f in os.listdir(class_in_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            if not images:
                continue
                
            # If a class has fewer images than requested, take what is available
            num_to_sample = min(samples_per_class, len(images))
            
            # Randomly select the images
            sampled_images = random.sample(images, num_to_sample)
            
            # Copy them to the new balanced directory
            for img_name in sampled_images:
                src = os.path.join(class_in_path, img_name)
                dst = os.path.join(class_out_path, img_name)
                shutil.copy2(src, dst)
                total_copied += 1
                
            print(f"  Copied {num_to_sample} images for class: {cls}")
            
    print(f"\nDone! Created balanced dataset with {total_copied} total images in '{output_dir}'.")

def main():
    parser = argparse.ArgumentParser(description="Create a balanced subset of images, preserving train/test splits.")
    parser.add_argument("--dir", required=True, help="Input directory (e.g., ../Grid-Dataset)")
    parser.add_argument("--out", required=True, help="Output directory (e.g., ../Balanced-Dataset)")
    parser.add_argument("--train-samples", type=int, default=1000, help="Images per class for training")
    parser.add_argument("--test-samples", type=int, default=200, help="Images per class for testing")
    
    args = parser.parse_args()
    create_balanced_dataset(args.dir, args.out, args.train_samples, args.test_samples)

if __name__ == "__main__":
    main()
