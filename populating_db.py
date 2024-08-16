import os,glob
import pandas as pd 
from src.exception import CustomException
from src.logger import logging
from src.data_ingestion import DataIngestion
from src.data_transformation import Data_Transformation
from src.utils import add_vectorDB,save_reference_data



DB_path="./artifacts/vector_db"
os.makedirs(os.path.dirname(DB_path),exist_ok=True)
# Reference data info
folder_path = "D:\\Code\\generative_AI\\medbrief_final\\data\\pre-defined-data2"
reference_pdf_paths = glob.glob(os.path.join(folder_path, '**', '*.pdf'), recursive=True)

# Data ingestion object
obj_inge=DataIngestion()

# Data transformation object
obj_trans=Data_Transformation()

## reading Reference Document
ref_documents:list = obj_inge.read_reference_data(reference_pdf_paths)

## save reference data
ref_save_path = save_reference_data(ref_documents)

print("reference data saved path {}".format(ref_save_path))

# generating embedding of reference documents
embeddings=obj_trans.get_embeddings(ref_documents)

#Adding embeddings to vector db
index_file_path = add_vectorDB(embeddings,DB_path)

print("vector db path {}".format(index_file_path))
