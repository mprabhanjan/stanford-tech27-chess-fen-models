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

## 1. Running the Basic ML Models
The traditional ML models (`tech27_project_chess_basic_models.ipynb`) are fully self-contained. 

You **do not** need to set up a local Python virtual environment to run these. You can upload the notebook directly to Google Colab (or any cloud Jupyter environment), point it to your dataset paths, and execute the cells. 

---

## 2. Running the Deep Learning Models
The Neural Network models (`chess_fen_neural_networks.ipynb`) process large spatial images and require significant GPU memory. It is highly recommended to run this notebook using a local runtime (e.g., Apple M-series GPU via Metal) to prevent memory crashes.

### Local Setup
Open your terminal, navigate to the `src` directory, and run the following command to create a virtual environment (`venv`) and install all required dependencies from `requirements.txt`:

```bash
make setup

### Run the Jupyter Notebook on your local Mac:
jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --port=8888 --NotebookApp.port_retries=0

### Launch Google Colab and connect to the local Jupyter server.
