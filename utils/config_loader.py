import yaml
from logger.custom_logger import CustomLogging
from exception.custom_exception import DocumentPortalException
import sys


logging = CustomLogging()
logger = logging.get_logger(__file__)

def load_config(filepath:str = "config/config.yaml") -> dict:
    try:
        with open(filepath, "r") as file:
            config = yaml.safe_load(file)
        logger.info(f"Config loaded successfully" , filepath = filepath , config_keys = list(config.keys()))
        return config
    except Exception as e:
        cus_exc = DocumentPortalException(e , sys)
        logger.error(cus_exc)
        raise DocumentPortalException(e , sys)



# if __name__ == "__main__":
#     config = load_config()
#     print(config)