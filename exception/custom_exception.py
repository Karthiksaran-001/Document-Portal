import sys
import traceback
from logger.custom_logger import CustomLogging
logger = CustomLogging().get_logger(__file__)
class DocumentPortalException(Exception):
    def __init__(self , error_msg , error_detail:sys):
        self.error_message = str(error_msg)
        _ , _ ,exc_tb = error_detail.exc_info()
        self.filename = exc_tb.tb_frame.f_code.co_filename
        self.lineno = exc_tb.tb_frame.f_lineno
        self.traceback_str = "".join(traceback.format_exception(*error_detail.exc_info()))

    def __str__(self):
        return f"""
            Error in {self.filename} at line [{self.lineno}]
            Message : {self.error_message}
            Traceback :{self.traceback_str}
            """
    

if __name__ == "__main__":
    try:
        a = 10/0
        print(a)
    except Exception as e:
        cus_exc = DocumentPortalException(e , sys)
        logger.error(cus_exc)
        raise cus_exc

