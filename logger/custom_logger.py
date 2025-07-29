import logging
from datetime import datetime
import os

class CustomLogging:
    def __init__(self , log_dir = "logs"):
        self.logs_dir = os.path.join(os.getcwd() , log_dir)
        os.makedirs(self.logs_dir , exist_ok= True)

        self.log_file = f"LOG_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.LOG_FILE_PATH = os.path.join(self.logs_dir , self.log_file)
        logging.basicConfig(filename= self.LOG_FILE_PATH,level= logging.INFO,format= "[ %(asctime)s ] %(levelname)s  [%(name)s] - (line-Num:%(lineno)d) -  %(message)s",force= True)

    def get_logger(self,name =__file__):
        return logging.getLogger(name = os.path.basename(name))

if __name__ == "__main__":
    logger = CustomLogging()
    logger = logger.get_logger(__file__)
    logger.info("Testing")