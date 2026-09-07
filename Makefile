# Define variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

.PHONY: setup clean downsize grid balance filter run_jupyter

# Default target
all: setup

# Create the virtual environment and install requirements
setup:
	python3.11 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Step 1: Downsize the original images
downsize: setup
	$(PYTHON) image_downsize.py --dir ../Orig-Dataset --out ../Compressed-Dataset --size 200

# Step 2: Crop the resized images into 64 labeled squares
grid: setup
	$(PYTHON) create_grid_dataset.py --dir ../Compressed-Dataset --out ../Grid-Dataset

# Step 3: Create a balanced subset for training
balance: setup
	$(PYTHON) create_balanced_dataset.py --dir ../Grid-Dataset --out ../Balanced-Dataset --train-samples 5000 --test-samples 1000

# Step 4: Extract unused full boards to prevent data leakage
filter: setup
	$(PYTHON) filter_unused_boards.py --grid_dir ../Grid-Dataset/test --orig_dir ../Compressed-Dataset/test --target_dir ../Unused-Full-Boards/test --size 1000

# Enable the extension for Colab local backend and start the Jupyter server
run_jupyter: setup
	$(PYTHON) -m jupyter serverextension enable --py jupyter_http_over_ws
	$(PYTHON) -m jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0

# Remove the virtual environment
clean:
	rm -rf $(VENV)
