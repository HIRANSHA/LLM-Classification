import argparse
import os,glob
import faiss
import pandas as pd
from langchain_community.llms.ollama import Ollama   
from src.data_ingestion import DataIngestion
from src.data_transformation import Data_Transformation
from src.utils import add_vectorDB,load_vectorDB,load_reference_data,Promp_temp

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class Document_classifier:
    def __init__(self,index_file_path:str,ref_data_path:str,ref_data_infopath:str):
        self.loaded_index = faiss.read_index(index_file_path)
        self.ref_datainfo = pd.read_csv(ref_data_infopath)
        self.reference_data = load_reference_data(ref_data_path)
 

    def classify(self,query_documents:list,df_query,page_mode,img_pageno=None):
        img_count=0
        k = 4  # Number of nearest neighbors to retrieve
        # iterate through each input emebdding
        for i,qer_doc in enumerate(query_documents):
            # Search for the most relevant document chunks
            # Step 2: Create embeddings for input document
            # generating embedding of reference documents
            query_embeddings = obj_trans.get_embeddings(qer_doc)
            query_embeddings = query_embeddings.numpy()  # Convert to numpy array


            _, indices = self.loaded_index.search(query_embeddings, k)

            if not page_mode:
                print("name of the document is {} and similar document from vector db are \n{}".format(df_query['doc_name'][i],[self.ref_datainfo['doc_name'][j] for j in list(indices)]))
                print('\n')
            else:
                img_count = img_pageno.count(i+1)
                print("page {}  and similar document from vector db are \n{}".format(i+1,[self.ref_datainfo['doc_name'][j] for j in list(indices)]))
                print('\n')
       

            relevant_chunks = [self.reference_data[i] for i in indices[0]]
            relevant_text = "\n\n".join(relevant_chunks)

            prompt = Promp_temp(relevant_chunks,qer_doc)
            
            model = Ollama(model="llama2")
            response_text = model.invoke(prompt)
            if img_count ==0:
                formatted_response = f"LLM Response: {response_text}"
            else:
                formatted_response = f"LLM Response for the  Classification of Text and {img_count} Image contents in the Page {i+1} is : {response_text}"
            print(formatted_response)
            print('\n')
            print("######################")
            print('\n')



if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--pagewise", action='store_true',help='Enable page-wise processing')
    args = parser.parse_args()

    # Vector DB path
    db_path = './artifacts/vector_db/vector_database.faiss'

    # predifined data path
    prefined_data_saved_path = './artifacts/reference_data_list.pkl'

    # predefined data information path
    prefined_data_infopath = './artifacts/data_info/refr_data.csv'

    obj_doc_classifier = Document_classifier(db_path,prefined_data_saved_path,prefined_data_infopath)

    # Data ingestion object
    obj_inge=DataIngestion()

    # Data transformation object
    obj_trans=Data_Transformation()

    #query pdf path
   
    query_folder_path :str="D:\\Code\\generative_AI\\medbrief_final\\artifacts\\query_data"

    # Find both PDF and DOCX files
    query_pdf_docx_paths = [
        file for ext in ['*.pdf', '*.docx']
        for file in glob.glob(os.path.join(query_folder_path, '**', ext), recursive=True)
]
    if not args.pagewise:
        print("Entering Document mode to read each document")
        query_documents,df_query = obj_inge.read_query_document(query_pdf_docx_paths)
        page_mode=False
        obj_doc_classifier.classify(query_documents,df_query,page_mode)
    else:
        print("Entering pagewise mode to read each pages of document")
        query_documents,df_query,page_img,img_pageno = obj_inge.read_query_document_pages(query_pdf_docx_paths[0])
        page_mode=True
        obj_doc_classifier.classify(query_documents,df_query,page_mode,img_pageno)

    