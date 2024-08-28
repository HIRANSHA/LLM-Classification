import fitz
import sys
from src.exception import CustomException
from src.logger import logging
import torch
from transformers import AutoTokenizer, AutoModel
from docx2pdf import convert

class Data_Transformation:
    def __init__(self):
        self.documents = []
        self.doc_id = 0
        self.page_id = 0
        self.chunk_info=[]
        self.page_text = []
        self.page_info=[]
        self.page_image=[]
        self.img_page_no=[]
        self.row={}
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


    # extract document data
    def exract_txt(self,path):
        name = path.split('\\')[-1].split('.')[0]
        # class_name = name.split('-')[-1]
        # temp_txt = "Category :{}".format(class_name) 
        doc = fitz.open(path)
        text = ""
        for page_num in range(len(doc)):
        
            page = doc.load_page(page_num)
            # text = "{} , {}".format(temp_txt,page.get_text())
            text += page.get_text()
            # text = remove_table_contents(text)
            new_row = self.row.copy()
            new_row = {
            'doc_id': self.doc_id+1,
            'doc_name':name,
                    } 
    
        return new_row,text
    
        # reading each documents to classify    
    def read_pdf(self,pdf_path,data_name):
        logging.info(f" Reading document of {data_name} Starting .... ")

        try:
            for path in pdf_path:
                if path.endswith('.pdf'):
                    new_row,text = self.exract_txt(path)

                elif path.endswith('.docx'):
                    print(path)
                    temp_pdf_path='temp.pdf'
                    convert(path, "temp.pdf")
                    new_row,text = self.exract_txt(temp_pdf_path)

                self.chunk_info.append(new_row) 
                self.documents.append(text)
                self.doc_id=self.doc_id+1
            logging.info(f"{data_name} reading  completed")
            # return (docu_,chunkinfo)
            return self.documents,self.chunk_info 
        except Exception as e:
            raise CustomException(e,sys)
        
    # extract pagewise data
    def exract_page_txt(self,path):
        name = path.split('\\')[-1].split('.')[0]
        # class_name = name.split('-')[-1]
        # temp_txt = "Category :{}".format(class_name) 
        doc = fitz.open(path)
   
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # text = "{} , {}".format(temp_txt,page.get_text())
            self.page_text.append(page.get_text())
            count = len(page.get_images(full=True))
            self.page_image.extend(page.get_images(full=True))
            self.img_page_no.extend([page_num+1]*count)
            # text = remove_table_contents(text)
            new_row = self.row.copy()
            new_row = {
            'page_id': self.page_id+1,
            'doc_name':name,
                    }
            self.page_info.append(new_row)
            self.page_id=self.page_id+1
        return self.page_info,self.page_text,self.page_image,self.img_page_no
    

    # reading each page of documents to classify 
    def read_pdf_page(self,pdf_path:str,data_name):
        logging.info(f" Reading each page of {data_name} Starting .... ")

        try:
            if pdf_path.endswith('.pdf'):
                page_info,page_text,page_img,img_pageno = self.exract_page_txt(pdf_path)

            elif pdf_path.endswith('.docx'):
                temp_pdf_path='temp.pdf'
                convert(pdf_path, "temp.pdf")
                page_info,page_text,page_img,img_pageno = self.exract_page_txt(temp_pdf_path)

            logging.info(f"Page wise reading of reading {data_name} completed")
            # return (docu_,chunkinfo)
            return page_text,page_info,page_img,img_pageno
        except Exception as e:
            raise CustomException(e,sys)
        



    def get_embeddings(self,text:list):
        logging.info(" Generating embedding  ")
        try:
            inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                embeddings = self.model(**inputs).last_hidden_state.mean(dim=1)
            logging.info("Embedding Generation completed ")
            return embeddings 
        except Exception as e:
            raise CustomException(e,sys)



