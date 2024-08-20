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
