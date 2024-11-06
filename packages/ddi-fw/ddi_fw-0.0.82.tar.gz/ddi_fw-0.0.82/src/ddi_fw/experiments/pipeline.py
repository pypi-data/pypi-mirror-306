import sqlite3
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
from keras.models import Model, Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout, Input, Activation, BatchNormalization
from tensorflow import keras
from ddi_fw.experiments import TFSingleModal, TFMultiModal
from ddi_fw.experiments import evaluate
from sklearn.preprocessing import LabelBinarizer
import numpy as np
import pandas as pd
from ddi_fw.utils import ZipHelper, Py7ZipHelper
import os
import chromadb
from collections import defaultdict
from langchain_community.vectorstores import Chroma
from ddi_fw.ner.ner import CTakesNER
from ddi_fw.langchain.embeddings import PoolingStrategy

from ddi_fw.datasets import BaseDataset, DDIMDLDataset

from ddi_fw.langchain.embeddings import SumPoolingStrategy
from keras import metrics
from ddi_fw.experiments.evaluation_helper import evaluate

import mlflow


class Experiment:
    def __init__(self, 
                 experiment_name=None, 
                 experiment_description=None, 
                 experiment_tags=None, 
                 tracking_uri=None, 
                 dataset_type:BaseDataset=None, 
                 columns=None,
                 embedding_dict = None, 
                 vector_db_persist_directory=None, 
                 vector_db_collection_name=None, 
                 embedding_pooling_strategy_type:PoolingStrategy=None, 
                 ner_data_file=None, 
                 ner_threshold=None, 
                 combinations=None, 
                 model=None):
        
        self.experiment_name = experiment_name
        self.experiment_description = experiment_description
        self.experiment_tags = experiment_tags
        self.tracking_uri = tracking_uri
        self.dataset_type = dataset_type
        self.columns = columns
        self.embedding_dict = embedding_dict
        self.vector_db_persist_directory = vector_db_persist_directory
        self.vector_db_collection_name = vector_db_collection_name
        self.embedding_pooling_strategy_type = embedding_pooling_strategy_type
        self.ner_data_file = ner_data_file
        self.ner_threshold = ner_threshold
        self.combinations = combinations
        self.model = model

    def build(self):
        # 'enzyme','target','pathway','smile','all_text','indication', 'description','mechanism_of_action','pharmacodynamics', 'tui', 'cui', 'entities'
        kwargs = {"columns": self.columns}
        for k, v in self.ner_threshold.items():
            kwargs[k] = v
        if self.embedding_dict == None:
            if self.vector_db_persist_directory:
                self.vector_db = chromadb.PersistentClient(
                    path=self.vector_db_persist_directory)
                self.collection = self.vector_db.get_collection(
                    self.vector_db_collection_name)
                dictionary = self.collection.get(include=['embeddings', 'metadatas'])

                embedding_dict = defaultdict(lambda: defaultdict(list))

                for metadata, embedding in zip(dictionary['metadatas'], dictionary['embeddings']):
                    embedding_dict[metadata["type"]][metadata["id"]].append(embedding)

                embedding_size = dictionary['embeddings'].shape[1]
        else:
            embedding_dict = self.embedding_dict
            embedding_size = list(embedding_dict['all_text'].values())[0][0].shape

        pooling_strategy = self.embedding_pooling_strategy_type()

        self.ner_df = CTakesNER().load(filename=self.ner_data_file)  if self.ner_data_file else None

        self.dataset = self.dataset_type(
            embedding_dict=embedding_dict,
            embedding_size=embedding_size,
            embeddings_pooling_strategy=pooling_strategy,
            ner_df=self.ner_df, **kwargs)

        X_train, X_test, y_train, y_test, X_train.index, X_test.index, train_idx_arr, val_idx_arr = self.dataset.load()

        self.dataframe = self.dataset.dataframe
        # dataframe.dropna()
        self.X_train = self.dataset.X_train
        self.X_test = self.dataset.X_test
        self.y_train = self.dataset.y_train
        self.y_test = self.dataset.y_test
        self.train_idx_arr = self.dataset.train_idx_arr
        self.val_idx_arr = self.dataset.val_idx_arr
        # Logic to set up the experiment
        self.items = self.dataset.produce_inputs()

        unique_classes = pd.unique(self.dataframe['event_category'])
        event_num = len(unique_classes)
        # droprate = 0.3
        vector_size = self.dataset.drugs_df.shape[0]

        print("Building the experiment with the following settings:")
        print(
            f"Name: {self.experiment_name}, Dataset: {self.dataset}, Model: {self.model}")
        # Implement additional build logic as needed
        return self

    def run(self, model_func, batch_size=128, epochs=100):
        mlflow.set_tracking_uri(self.tracking_uri)

        if mlflow.get_experiment_by_name(self.experiment_name) == None:
            mlflow.create_experiment(self.experiment_name)
            mlflow.set_experiment_tags(self.experiment_tags)
        mlflow.set_experiment(self.experiment_name)

        y_test_label = self.items[0][4]
        multi_modal = TFMultiModal(
            model_func=model_func, batch_size=batch_size,  epochs=epochs)  # 100
        multi_modal.set_data(
            self.items, self.train_idx_arr, self.val_idx_arr, y_test_label)
        result = multi_modal.predict(self.combinations)
        return result