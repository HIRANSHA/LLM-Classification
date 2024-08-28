import os, glob, sys
import pandas as pd 
from src.exception import CustomException
from src.logger import logging
from transformers import AutoTokenizer, AutoModel
from src.data_transformation import Data_Transformation



class DataIngestion:
    def __init__(self):
        self.data_trans_obj=Data_Transformation()
        self.refr_data_info_path: str=os.path.join('artifacts','data_info',"refr_data.csv")
        self.query_data_info_path: str=os.path.join('artifacts','data_info',"query_data.csv")

    def read_reference_data(self,reference_pdf_paths)->list:
        logging.info("Entered the data ingestion method to read reference data")
        try:
            os.makedirs(os.path.dirname(self.refr_data_info_path),exist_ok=True)
            
            
            ref_documents,ref_doc_info = self.data_trans_obj.read_pdf(reference_pdf_paths,'reference data')
            

            df_ref = pd.DataFrame(ref_doc_info)
            df_ref.to_csv(self.refr_data_info_path,index=False,header=True)

          

            return ref_documents
       
        except Exception as e:
            raise CustomException(e,sys)
        
    def read_query_document(self,query_pdf_paths)->list:
        logging.info("Entered the data ingestion method to read query document")
        try:
            
            os.makedirs(os.path.dirname(self.query_data_info_path),exist_ok=True)
            
            
            quer_documents,query_doc_info = self.data_trans_obj.read_pdf(query_pdf_paths,'query data')


            df_query = pd.DataFrame(query_doc_info)
            df_query.to_csv(self.query_data_info_path,index=False,header=True)

            return quer_documents,df_query
       
        except Exception as e:
            raise CustomException(e,sys)
        

    def read_query_document_pages(self,query_pdf_path)->str:
        logging.info("Entered the data ingestion method to read query document pagewise")
        try:
            
            os.makedirs(os.path.dirname(self.query_data_info_path),exist_ok=True)
            
            
            query_pages,query_page_info,page_img,img_pageno = self.data_trans_obj.read_pdf_page(query_pdf_path,'query data')


            df_query = pd.DataFrame(query_page_info)
            df_query.to_csv(self.query_data_info_path,index=False,header=True)

            return query_pages,df_query,page_img,img_pageno
       
        except Exception as e:
            raise CustomException(e,sys)


        



# if __name__=="__main__":
#     folder_path = "D:\\Code\\generative_AI\\medbrief_final\\data\\pre-defined-data2"
#     reference_pdf_paths = glob.glob(os.path.join(folder_path, '**', '*.pdf'), recursive=True)

#     ## Input Document
#     input_folder_path ="D:\\Code\\generative_AI\\medbrief_final\\data\\input"

#     input_pdf_paths = glob.glob(os.path.join(input_folder_path, '**', '*.pdf'), recursive=True)
#     obj=DataIngestion(reference_pdf_paths,input_pdf_paths)
#     ## Reference Document

#     ref_documents,quer_documents = obj.read_data()
  

