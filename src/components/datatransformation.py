import sys
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
import os
from dataclasses import dataclass
from src.utils import save_object
@dataclass
class DataTransformConfig:
    preprocess_obj = os.path.join("artifacts","preproc.pkl")

class DataTransform:
    def __init__(self):
        self.datatransformobj = DataTransformConfig()

    def getdatatransformer(self):
        try:
           numcol = ["writing_score","reading_score"]
           catcol = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

           numpipe = Pipeline(
               steps =[
               ("impute",SimpleImputer(strategy="median")),
               ("scaler",StandardScaler(with_mean=False))
           ])

           logging.info("Numerical column scaling done")
           catpipe = Pipeline(
               steps=[
                   ("imputer",SimpleImputer(strategy="most_frequent")),
                   ("encoder",OneHotEncoder()),
                   ("scaler",StandardScaler(with_mean=False))
               ])

           logging.info("Categorical column encoding done")

           preprocessor = ColumnTransformer(
               [
                   ("numpre",numpipe,numcol),
                   ("catpre",catpipe,catcol)
               ]
           )

           return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def init_data_transform(self,train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and Test data read")

            logging.info("Obtaining preprocessed data")
            predataobj = self.getdatatransformer()

            target_column = "math_score"
            numcol = ["writing_score", "reading_score"]

            inputtrain = train_df.drop(columns=[target_column],axis=1)
            targettrain = train_df[target_column]
            inputtest = test_df.drop(columns=[target_column],axis=1)
            targettest = test_df[target_column]

            logging.info("Applying preprocessed object into train and test dataframe")

            inputtrainarr = predataobj.fit_transform(inputtrain)
            inputtestarr = predataobj.transform(inputtest)

            train_arr = np.c_[inputtrainarr,np.array(targettrain)]
            test_arr = np.c_[inputtestarr,np.array(targettest)]

            logging.info("saved preprocessing object")

            save_object(
                file_path = self.datatransformobj.preprocess_obj,
                obj = predataobj
            )

            return(
               train_arr,
               test_arr,
               self.datatransformobj.preprocess_obj,
            )


        except Exception as e:
             raise CustomException(e,sys)
