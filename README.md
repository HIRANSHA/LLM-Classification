# Document Classification using LLM and RAG

## Overview

This project is designed to classify documents (PDF and DOCX formats) into predefined classes using a combination of a FAISS vector database for similarity matching and the LLAMA2 model for classification. The system leverages advanced language models to accurately classify documents into their respective categories.

## Features

- **Document Classification:** Classifies documents into predefined categories using LLAMA2 and FAISS.
- **Page-wise Classification:** Provides the ability to classify each page and images within a document individually.
- **Supports Multiple Formats:** Works with both PDF and DOCX file formats.

## Installation

### 1. Download and Install OLLAMA

- Visit the [Ollama official website](https://ollama.com) or their GitHub page.
- Download the Windows installer or binary for the latest version.
- If you downloaded an installer (usually an `.exe` file), double-click it to start the installation process.
- Follow the on-screen instructions to complete the installation.

### 2. Verify Installation

- Open a new Command Prompt.
- Type `ollama --version` and press Enter to check if Ollama is installed correctly and to see the installed version.

### 3. Download LLAMA2 7B Model File

- Open a new Command Prompt.
- Run the following command to download the LLAMA2 7B model:
  ```bash
  ollama run llama2:7b

- Once the model is downloaded, you can close the Command Prompt.


### 4. Set Up Local Environment using Conda

- **Download the Anaconda Installer:**
  - Go to the [Anaconda Distribution page](https://www.anaconda.com/products/distribution).
  - Download the Windows installer for Python 3.x (64-bit or 32-bit depending on your system).
  - Double-click the downloaded `.exe` file to start the installer.
  - Follow the on-screen instructions.

- **Create and set up a Conda environment:**
  - Open a new Command Prompt and navigate to the directory where you want to set up the git and conda environment.
  - Execute the following steps to fetch the data from GitHub and set up the Conda environment:
    ```bash
    git clone https://github.com/HIRANSHA/LLM-Classification.git
    cd LLM-Classification
    conda create -p venv python==3.10 -y
    pip install -r requirements.txt
    ```

### 5. Copy Sample Data

- Copy sample data into two folders named `pre-defined-data2` and `query_data`.
  - `pre-defined-data2`: Contains reference data (data from different clinical sections).
  - `query_data`: Contains data to classify.

- Folder paths:
  ```bash
  ./artifacts/pre-defined-data2
  ./artifacts/query_data
  ```



