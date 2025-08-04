import os , sys 
from pathlib import Path 
import fitz
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException
from dotenv import load_dotenv


class DocumentIngestion:
    def __init__(self,base_dir:str = "data\document_compare"):
        self.log = CustomLogging().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)


    def delete_existing_files(self):
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("Delete existing file" , path = str(file))
                self.log.info("All existing files deleted" , dir = str(self.base_dir))
        except Exception as e:
            self.log.error(f"Error Occured while delete existing : {e}")
            raise DocumentPortalException("Error Occured while delete existing" , sys)
    def save_uploaded_files(self , ref_file , act_file):
        try:
            #self.delete_existing_files()
            #self.log.info("Delete Existing file Successfully")
            ref_path = Path(os.path.join(self.base_dir , ref_file.name))
            act_path = Path(os.path.join(self.base_dir , act_file.name))
            if not ref_file.name.lower().endswith(".pdf") or not act_file.name.lower().endswith(".pdf"):
                raise ValueError("Only PDF files are allowed.")
            #print(ref_path)
            with open(ref_path, "wb") as f:
                f.write(ref_file.get_buffer())

            with open(act_path, "wb") as f:
                f.write(act_file.get_buffer())

            self.log.info("Files saved", reference=str(ref_path), actual=str(act_path))
            return ref_path, act_path
            

        except Exception as e:
            self.log.error(f"Error Occured while upload file : {e}")
            raise DocumentPortalException("Error Occured while upload file" , sys) 
    def read_pdf(self , file_path:Path)->str:
        try:
            with fitz.open(file_path) as doc:
                if doc.is_encrypted:
                    raise ValueError("PDF is encrypted Cannot read from path :{file_path}")
                all_text = []
                for page in range(doc.page_count):
                    page = doc.load_page(page)
                    text = page.get_text()
                    if text.strip():
                        all_text.append(f"\n --- Page {page} --- \n {text}")
                self.log.info("Successfully read PDf from : {file_path}")
                all_text = "\n".join(all_text)
                return all_text 
        except Exception as e:
            self.log.error(f"Error Occured while Reading PDF : {e}")
            raise DocumentPortalException("Error Occured while reading file" , sys) 
        
    def combined_documents(self):
        try:
            concat_dict = {}
            doc_part = []
            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    concat_dict[filename.name] = self.read_pdf(filename)
            for filename , content in concat_dict.items():
                doc_part.append(f"Document: {filename}\n{content}")
            combined_doc = "\n\n".join(doc_part)
            self.log.info("Document Combined", count = len(doc_part))
            return combined_doc
            
        except Exception as e:
            self.log.error(f"Error Occured while combined_documents : {e}")
            raise DocumentPortalException("Error Occured while combined_documents" , sys)
        

