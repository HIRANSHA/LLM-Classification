import os
import sys
import faiss
from src.exception import CustomException
from src.logger import logging
from langchain.prompts import ChatPromptTemplate
import pickle

def Promp_temp(relevant_chunks:list,query:str):
    PROMPT_TEMPLATE = """
        Query Data: {query_content}
        Retrieved Data: {context}
        Task: classify the query into any of following sections such as Biochemistry, Cytology, Haematology, Histopathology, Immunology, Microbiology  based on the Retrieved Data provided.
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=relevant_chunks, query_content=query)

    return prompt

def save_reference_data(ref_documents)->list:
    path = './artifacts/reference_data_list.pkl'
    # Saving the list to a file
    with open(path, 'wb') as file:
        pickle.dump(ref_documents, file)
    return(path)


def load_reference_data(path):
    # Loading the list back
    with open(path, 'rb') as file:
        loaded_list = pickle.load(file)

    return loaded_list


def add_vectorDB(ref_embeddings,folder_path):
    try:
        logging.info("Adding data to Vector DB")
        os.makedirs(folder_path, exist_ok=True)
        #  Store embeddings in FAISS
        dimension = ref_embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(ref_embeddings)

        logging.info("Vector DB Data Adding completed ")

        # Save the index to the specified folder
        index_file_path = os.path.join(folder_path, "vector_database.faiss")
        faiss.write_index(index, index_file_path)

        logging.info(f"Db written to {index_file_path}")

        return index_file_path

    except Exception as e:
        raise CustomException(e, sys)
    

    
def load_vectorDB(index_file_path):
    try:
        # Load the index from the folder
        loaded_index = faiss.read_index(index_file_path)
        return loaded_index

    except Exception as e:
        raise CustomException(e, sys)
    


