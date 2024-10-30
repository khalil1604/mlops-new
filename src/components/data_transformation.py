import sys
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessed_object_file_path = os.path.join("artifacts","preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        """function responsible for data transformation depending on the variable"""
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoding", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            logging.info("Categorical Variables Standard Scaling completed")
            logging.info("Numerical Variables encoding completed")

            preprocessor= ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor

            
        except Exception as e:
            raise CustomException(e,sys)
        

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df=pd.read_csv(train_path)

            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            logging.info("Read train and test data completed")
            logging.info(f"Train DataFrame columns: {train_df.columns.tolist()}")
            logging.info(f"Test DataFrame columns: {test_df.columns.tolist()}")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name= "math_score"
            numerical_columns=["writing_score", "reading_score"]

            input_features_train_df=train_df.drop(columns=[target_column_name], axis=1)
            target_features_train_df=train_df[target_column_name]

            input_features_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_features_test_df=test_df[target_column_name]

            logging.info("Applying preprocessing object on training dataframe and testing dataframe")

            input_features_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_features_test_arr=preprocessing_obj.transform(input_features_test_df)

            train_arr = np.c_[
                input_features_train_arr, np.array(target_features_train_df)
            ]

            test_arr = np.c_[input_features_test_arr, np.array(target_features_test_df)]

            logging.info("Saved preprocessing object")

            save_object(file_path=self.data_transformation_config.preprocessed_object_file_path, obj=preprocessing_obj)


            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessed_object_file_path,
            )
        
        except Exception as e:
            raise CustomException(e,sys)
            


