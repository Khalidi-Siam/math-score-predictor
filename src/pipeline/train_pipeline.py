import sys
import time
from dataclasses import dataclass

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import logging


@dataclass
class TrainPipelineArtifact:
    train_data_path: str
    test_data_path: str
    preprocessor_path: str
    best_model_name: str
    r2_square: float


class TrainPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()


    def run_pipeline(self):
        '''
            This function is responsible for running the entire training pipeline
            data ingestion, data transformation and model training
            and returns the artifact of the training pipeline
            which contains the path of the train and test data, preprocessor object,
            best model name and r2 square score
        '''

        try:
            start_time = time.time()

            logging.info("Training pipeline started")

            logging.info("Starting data ingestion")

            train_data_path, test_data_path = \
                self.data_ingestion.initiate_data_ingestion()

            logging.info("Data ingestion completed")

            logging.info("Starting data transformation")

            train_arr, test_arr, preprocessor_path = \
                self.data_transformation.initiate_data_transformation(
                    train_data_path,
                    test_data_path
                )

            logging.info("Data transformation completed")

            logging.info("Starting model training")

            best_model_name, r2_square = \
                self.model_trainer.initiate_model_trainer(
                    train_arr,
                    test_arr
                )

            logging.info(
                f"Model training completed. "
                f"Best model: {best_model_name}, "
                f"R2 Score: {r2_square}"
            )


            total_time = round(time.time() - start_time, 2)

            logging.info(f"Training pipeline finished in {total_time} seconds")

            return TrainPipelineArtifact(
                train_data_path=train_data_path,
                test_data_path=test_data_path,
                preprocessor_path=preprocessor_path,
                best_model_name=best_model_name,
                r2_square=r2_square
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    print("Training Started...")
    artifact = TrainPipeline().run_pipeline()

    print(
        f"""
        Training Completed Successfully

        Best Model: {artifact.best_model_name}
        R2 Score: {artifact.r2_square}
        """
    )
