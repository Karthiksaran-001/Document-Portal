import logging
from datetime import datetime
import os
import structlog

class CustomLogging:
    def __init__(self , log_dir = "logs"):
        self.logs_dir = os.path.join(os.getcwd() , log_dir)
        os.makedirs(self.logs_dir , exist_ok= True)

        self.log_file = f"LOG_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.LOG_FILE_PATH = os.path.join(self.logs_dir , self.log_file)
        logging.basicConfig(filename= self.LOG_FILE_PATH,level= logging.INFO,format= "[ %(asctime)s ] %(levelname)s  [%(name)s] - (line-Num:%(lineno)d) -  %(message)s",force= True)

    def get_logger(self, name =__file__):
        logger_name = os.path.basename(name)
        #logger = logging.getLogger(logger_name)

        # Configure logging for console + file (both JSON)
        #print(f"File : {self.LOG_FILE_PATH}")
        file_handler = logging.FileHandler(self.LOG_FILE_PATH)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))  # Raw JSON lines

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",  # Structlog will handle JSON rendering
            handlers=[console_handler, file_handler]
        )

        # Configure structlog for JSON structured logging
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
        # if not logger.handlers:
        #     logger.addHandler(file_handler)
        #     logger.addHandler(console_handler)
        return structlog.get_logger(logger_name)
        #return logger

# if __name__ == "__main__":
#     logger = CustomLogging()
#     logger = logger.get_logger(__file__)
#     #logger.info("Stream Handler is Working")
#     logger.error("Failed to process PDF", error="File not found", user_id=123)