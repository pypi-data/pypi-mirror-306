import json
from ddi_fw.pipeline import Pipeline
import importlib


def load_config(file_path):
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def get_import(full_path_of_import):
    """Dynamically imports an object from a module given its full path.

    Args:
        full_path_of_import (str): The full path of the import (e.g., 'module.submodule.ClassName').

    Returns:
        object: The imported object.

    Raises:
        ImportError: If the module cannot be imported.
        AttributeError: If the attribute does not exist in the module.
    """
    if not full_path_of_import:
        raise ValueError("The import path cannot be empty.")

    parts = full_path_of_import.split('.')
    import_name = parts[-1]
    module_name = ".".join(parts[:-1]) if len(parts) > 1 else ""

    try:
        module = importlib.import_module(module_name)
        return getattr(module, import_name)
    except ModuleNotFoundError as e:
        raise ImportError(f"Module '{module_name}' could not be found.") from e
    except AttributeError as e:
        raise AttributeError(
            f"'{module_name}' has no attribute '{import_name}'") from e


class MultiPipeline():
    def __init__(self, experiments_config_file):
        self.experiments_config = load_config(experiments_config_file)
        self.items = []
        self.pipeline_resuts = dict()

    def __create_pipeline(self, config):
        library = config["library"]
        batch_size = config["batch_size"]
        epochs = config["epochs"]

        # dataset_module = config["dataset_module"]
        # dataset_name = config["dataset_name"]

        experiment_name = config["experiment_name"]
        experiment_description = config["experiment_description"]
        experiment_tags = config["experiment_tags"]
        tracking_uri = config["tracking_uri"]
        artifact_location = config["artifact_location"]
        columns = config["columns"]
        ner_data_file = config["ner_data_file"]
        ner_threshold = config["ner_threshold"]
        vector_db_persist_directory = config["vector_db_persist_directory"]
        vector_db_collection_name = config["vector_db_collection_name"]
        embedding_pooling_strategy = get_import(
            config["embedding_pooling_strategy_type"])
        # Dynamically import the model and dataset classes
        model_type = get_import(config["model_type"])
        dataset_type = get_import(config["dataset_type"])
        combination_type = get_import(config["combination_strategy"]["type"])
        kwargs_combination_params = config["combination_strategy"]["params"]

        # # Instantiate the classes
        # model_instance = model_class()
        # dataset_instance = dataset_class()
        return {
            "name": experiment_name,
            "library": library,
            "batch_size": batch_size,
            "epochs": epochs,
            "model_type": model_type,
            "pipeline": Pipeline(
                library=library,
                experiment_name=experiment_name,
                experiment_description=experiment_description,
                experiment_tags=experiment_tags,
                artifact_location=artifact_location,
                tracking_uri=tracking_uri,
                dataset_type=dataset_type,
                columns=columns,
                vector_db_persist_directory=vector_db_persist_directory,
                vector_db_collection_name=vector_db_collection_name,
                embedding_pooling_strategy_type=embedding_pooling_strategy,
                ner_data_file=ner_data_file,
                ner_threshold=ner_threshold,
                combinations=combination_type(**kwargs_combination_params).generate())}

    def build(self):
        for config in self.experiments_config['experiments']:
            item = self.__create_pipeline(config)
            self.items.append(item)

    def run(self):
        for item in self.items:
            print(f"{item['name']} is running")
            pipeline = item['pipeline']
            model_type = item['model_type']
            batch_size = item['batch_size']
            epochs = item['epochs']
            pipeline.build()
            result = pipeline.run(model_type, epochs=epochs, batch_size=batch_size)
            self.pipeline_resuts[item['name']] = result

    def results(self):
        return self.pipeline_resuts