import os
import sys
import pandas
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.datatransformation import DataTransform
from src.components.datatransformation import DataTransformConfig


@dataclass
class DataIngestionConfig:
    train_data_path = os.path.join("artifacts","train.csv")
    test_data_path = os.path.join("artifacts", "test.csv")
    raw_data_path = os.path.join("artifacts", "data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initialise_data(self):
        logging.info("Entered the data initialisation function")
        try:
            df = pd.read_csv('notebook\stud.csv')
            logging.info("Read the data")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train Test Split initiated")
            train_data, test_data = train_test_split(df,test_size=0.2,random_state=42)

            train_data.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False,header=True)

            logging.info("Ingestion Completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initialise_data()

    data_trans = DataTransform()
    data_trans.init_data_transform(train_data,test_data)