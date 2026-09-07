# From Pixels to Positions: Chess FEN Generation via Machine Learning
**Author:** Mahidas Prabhanjan  
**Course:** TECH 27, Summer 2026, Stanford University  

This repository contains the data engineering pipeline and machine learning notebooks used to accurately translate a raw 2D image of a chessboard into its standardized Forsyth-Edwards Notation (FEN) string. 

## Project Structure
The project is divided into two distinct modeling phases, backed by a robust image preprocessing pipeline.

* **Basic Models Notebook:** Evaluates Traditional ML classifiers (Logistic Regression, k-NN, Random Forest, SVM, Boosting) on localized piece squares. 
* **Deep Learning Notebook:** Evaluates spatial architectures (MLP, CNN, Advanced CNN) on full 200x200 board inputs.
* **Data Engineering Scripts:** A suite of Python utilities that resize, slice, label, and balance the raw datasets.

---

## 0. Synthetic Chessboard Image Dataset from Kaggle

**Dataset Link:** [Chess Positions (Kaggle)](https://www.kaggle.com/datasets/koryakinp/chess-positions)

Follow these exact steps to set up the dataset, run the preprocessing pipeline, and prepare the files for model training:

1. Download the image dataset (`archive.zip`) from Kaggle via your browser.
2. Open your terminal and run the following commands to set up the original images:
   ```bash
   mkdir proj_root/Orig-Dataset
   cd proj_root/Orig-Dataset
   mv ~/Downloads/archive.zip .
   unzip archive.zip
   ```
3. Initialize the environment and downsize the images to 200x200:
   ```bash
   cd proj_root/
   mkdir ./Downsized-Dataset-200 
   cd src/
   make setup
   source venv/bin/activate
   python image_downsize.py --dir ../Orig-Dataset --out ../Downsized-Dataset-200 --size 200
   ```
4. Slice the downsized boards into individual square grids:
   ```bash
   mkdir ../Downsized-Grid-Images-200
   python ./create_grid_dataset.py --dir ../Downsized-Dataset-200 --out ../Downsized-Grid-Images-200
   ```
5. Balance the dataset to prevent majority-class bias (empty squares):
   ```bash
   mkdir ../Downsized-Grid-200-Images-Balanced-10K-2K
   python ./create_balanced_dataset.py --dir ../Downsized-Grid-Images-200 --out ../Downsized-Grid-200-Images-Balanced-10K-2K --train-samples 10000 --test-samples 2000
   ```
6. Archive and upload the training dataset to Google Drive:
   ```bash
   cd proj_root/
   zip -r Downsized-Grid-200-Images-Balanced-Dataset-10K-2K.zip Downsized-Grid-200-Images-Balanced-10K-2K
   ```
   *Upload the `.zip` file to your Google Drive.*

7. Extract the unused full boards to create an uncontaminated testing vault:
   ```bash
   mkdir -p Unused-Downsized-Dataset-200/test
   mkdir -p Unused-Downsized-Dataset-200/training
   cd src/
   python ./filter_unused_boards.py --grid_dir ../Downsized-Grid-200-Images-Balanced-10K-2K/test --orig_dir ../Downsized-Dataset-200/test --target_dir ../Unused-Downsized-Dataset-200/test --size 5000
   ```
8. Archive and upload the unused dataset to Google Drive:
   ```bash
   cd ..
   zip -r Unused-Downsized-Dataset-200-From-10K-2K.zip Unused-Downsized-Dataset-200
   ```
   *Upload the `Unused-Downsized-Dataset-200-From-10K-2K.zip` file to your Google Drive.*

---

## 1. Running the Basic ML Models
The traditional ML models (`tech27_project_chess_basic_models.ipynb`) are fully self-contained. 

You **do not** need to set up a local Python virtual environment to run these. You can upload the notebook directly to Google Colab (or any cloud Jupyter environment), point it to the datasets in your Google Drive, and execute the cells. 

---

## 2. Running the Deep Learning Models
The Neural Network models (`chess_fen_neural_networks.ipynb`) process large spatial images and require significant GPU memory. It is highly recommended to run this notebook using a local runtime (e.g., Apple M-series GPU via Metal) to prevent memory crashes.

### Local Setup
Open your terminal, navigate to the `src` directory, and run the following command to create the virtual environment (`venv`) and install all required dependencies:
```bash
make setup
```

### Run the Jupyter Notebook on your local Mac
Start the local Jupyter server with the necessary CORS flags to allow Google Colab to connect to it:
```bash
jupyter notebook --NotebookApp.allow_origin='[https://colab.research.google.com](https://colab.research.google.com)' --port=8888 --NotebookApp.port_retries=0
```

### Launch Google Colab and Connect to Local Server
1. Once the server starts in your terminal, look for the URL containing the access token (e.g., `http://localhost:8888/?token=...`).
2. Copy this URL.
3. Launch Google Colab in your browser.
4. Click the dropdown arrow next to the **Connect** button in the top right corner.
5. Select **Connect to a local runtime** and paste the URL.
