from logging import DEBUG
from datetime import datetime

class Settings:

    ######################################################################
    # System
    ######################################################################

    logging = {
        "level": DEBUG,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "filename": datetime.now().strftime("log/log_%Y_%m_%d_%H_%M_%S.log"),
    }