"""Pipeline Class Definition"""

# On TOP of all of this, the user shall define FLOW.py which should
# give him the desired trajectory operation output
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from .utilFunctions import tokenize_trajectory, detokenize_trajectory
from .constraintsClass import SpatialConstraints
from .partioningClass import PartitioningModule

import logging
import warnings

warnings.filterwarnings(
    "ignore", category=FutureWarning, module="transformers.deepspeed"
)

# warnings.simplefilter("always", UserWarning)
import pickle
import random
import datetime
import string
import pandas as pd
from typing import Tuple, List
from KAFY.modelsLoader import (
    train_wordpiece_tokenizer,
    load_training_args,
    Trainer,
    DataCollatorForLanguageModeling,
    prepare_and_save_datasets,
)
import json

# Configure the logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TrajectoryPipeline:
    """
    A configurable pipeline that orchestrates various processes such as
    tokenization, spatial constraints,
    trajectory plugins, and de-tokenization. This class is designed to be
    flexible and extensible, allowing
    the user to customize and modify different components according to their needs.
    """

    def __init__(
        self,
        mode: str = "",
        operation_type: str = "",
        use_tokenization: bool = False,
        use_spatial_constraints: bool = True,
        use_trajectory_plugin=False,
        use_detokenization: bool = True,
        modify_transformers_plugin: bool = False,
        modify_trajectory_plugin: bool = False,
        modify_spatial_constraints: bool = False,
        use_predefined_spatial_constraints: bool = False,
        project_path: str = "/KafyProject/",
    ):
        """
        Initializes the pipeline with needed params.

        Args:
            mode (str): Either 'addingModel','addingPretrainingData','addingFinetuningData', 'finetuning', or 'testing'.
            operation_type (str): User sets the operationt type
            use_tokenization (bool): Whether to use tokenization.
            use_spatial_constraints (bool): Whether to use spatial constraints.
            use_trajectory_plugin (bool): Whether to use trajectory plugin.
            use_detokenization (bool): Whether to use de-tokenization.
            modify_transformers_plugin (bool): Whether to modify transformers plugin.
            modify_trajectory_plugin (bool): Whether to modify trajectory plugin.
            modify_spatial_constraints (bool): Whether to modify spatial constraints.
            use_predefined_spatial_constraints (bool): Whether to user predefined
                                                        spatial constraints or not.
            project_path (str): where to save modelsRepo and trajectoryStore
        """
        # Case Scenarios 
        self.mode_options = ['startNewProject','addPretrainModel','addPretrainData','addFinetunData', 'finetuning', 'testing']
        # Those are the only required arguments
        if not mode:
            raise TypeError("Missing required argument: 'mode'")
        if mode not in self.mode_options:
            raise TypeError("wrong mode initialization. \n'mode' should be one of the following ",self.mode_options)
        if not project_path:
            raise TypeError("Missing required argument: 'project_path'")
        self.mode = mode
        self.use_tokenization = use_tokenization
        self.use_spatial_constraints = use_spatial_constraints
        self.use_trajectory_plugin = use_trajectory_plugin
        self.use_detokenization = use_detokenization
        self.modify_transformers_plugin = modify_transformers_plugin
        self.modify_trajectory_plugin = modify_trajectory_plugin
        self.modify_spatial_constraints = modify_spatial_constraints
        self.use_predefined_spatial_constraints = use_predefined_spatial_constraints
        self.operation_type = operation_type
        # Create ModelsRepo and trajectoryStore at specified projectPath if they don't exist already
        self.models_repository_path = os.path.join(project_path, "modelsRepo")
        self.trajecotry_store_path = os.path.join(project_path, "trajectoryStore")
        self.transformers_plugin_path = os.path.join(project_path, "transformersPlugin")
        self.trajectory_plugin_path = os.path.join(project_path, "trajectoryPlugin")
        pyramid_data = {"H": 5, "L": 3, "build_pyramid_from_scratch": True}
        if self.mode == "startNewProject":
            try:
                project_dir_name = os.path.basename(os.path.normpath(project_path))
                # Check if the project path is the default and issue a warning
                if project_dir_name == "KafyProject":
                    warnings.warn(
                        "No alternative project path provided. Will default to {project_path} directory",
                        UserWarning,
                    )

                # Create the project directories if they do not exist
                if not os.path.exists(project_path):
                    os.makedirs(project_path)
                    os.makedirs(self.models_repository_path)
                    os.makedirs()
                    os.makedirs(self.trajecotry_store_path)
                    os.makedirs(self.transformers_plugin_path)
                    os.makedirs(self.trajectory_plugin_path)
                    # JSON data to write
                    # Logging messages to indicate successful creation
                    logging.info(
                        "First time creating the project directory. All directories will be empty."
                    )
                    logging.info(
                        "First time creating modelsRepo, trajectoryStore, trajectoryPlugin, transformersPlugin."
                    )
                    # Define the file path for pyramidConfigs.json
                    pyramid_config_file = os.path.join(
                        self.models_repository_path, "pyramidConfigs.json"
                    )
                    # Initialize the empty modelsRepo.json file
                    self.modelsRepoJson = os.path.join(self.models_repository_path,'modelsRepo.json')
                    if not self.modelsRepoJson.exists():
                        self.modelsRepoJson.touch()
                    # Write the JSON data to the file
                    with open(pyramid_config_file, "w") as json_file:
                        json.dump(pyramid_data, json_file, indent=4)

                    logging.info(
                        "Created the pyramid configurations for the first time."
                    )
                    logging.info(
                        "Created the modelsRepo.json file for the first time.
                        "
                    )
                else:
                    logging.info(
                        f"Project path '{project_path}' already exists.   No directories were created."
                    )
                   

            except OSError as e:
                raise ValueError(f"Error creating project directories: {e}")

        elif self.mode=="addPretrainData":
            self.add_training_data()
        elif self.mode=="addPretrainModel":
            self.pretrain_model_on_all_datasets()
        # Initialize any other attributes or perform setup based on the parameters
        (
            self.model,
            self.tokenizer,
            self.spatial_constraints,
            self.trajectory_plugin,
            self.tokenized_trajectories,
            self.input_attributes,
            self.trajectories_list,
            self.spatial_constraints,
        ) = (None,) * 8
        (
            self.resolution_set_by_user,
            self.user_did_define_spatial_constraints,
            self.trajectories_got_tokenized,
            self.data_saved_to_trajectory_store,
        ) = (False,) * 4
        self.resolution = 10
        self.data_path_trajectory_store, self.metadata_path_trajectory_store = "", ""
        logging.info("Pipeline Initialized with mode: %s", self.mode)

    def add_training_data(self):
        """
        Tokenizes training data if needed and adds it to trajectoryStore/pretraining/
        """
        logging.info("Initializing for pretraining mode.")
        # Implementation for initializing pretraining mode

        if self.use_tokenization and self.trajectories_list is not None:
            logging.info(
                "Tokenizing the provided trajectories and adding to TrajectoryStore."
            )
            self.tokenized_trajectories = self.__tokenization_module(
                self.trajectories_list
            )
            self.trajectories_got_tokenized = True
            self.data_path_trajectory_store, self.metadata_path_trajectory_store = (
                self.__save_trajectories_to_store(
                    self.tokenized_trajectories, "pretraining"
                )
            )
        elif not self.use_tokenization and self.trajectories_list is not None:
            logging.info("Adding the provided trajectories to TrajectoryStore.")

            self.trajectories_got_tokenized = False
            self.data_path_trajectory_store, self.metadata_path_trajectory_store = (
                self.__save_trajectories_to_store(self.trajectories_list, "pretraining")
            )

        # @Youssef DO: I need to call the partioning module, need to think about this
        # in the case he is not using tokenization, i.e. passing traj,summary
        return self.__partioning_module_interface()

    def pretrain_model_on_all_datasets(self, model):
        """
        This function is responsible on taking the model that is added by
        the user and uses the tokenizer in models_loader to train the tokenizer
        on each dataset in the TrajectoryStore/pretraining.

        Output should be a model pretrained and tokenizer trained on the dataset
        and saved using the Partitioning in the modelsRepo
        """
        self.mode = "pretraining"
        self.operation = "pretraining"

        for file_name in os.listdir(
            os.path.join(self.trajecotry_store_path, "pretraining")
        ):
            if file_name.endswith("_vocab.txt"):

                vocab_file_path = os.path.join(
                    os.path.join(self.trajecotry_store_path, "pretraining"), file_name
                )
                metadata_file_path = vocab_file_path.replace(
                    "_vocab.txt", "_metadata.json"
                )

                if os.path.isfile(metadata_file_path):
                    with open(metadata_file_path, "r") as metadata_file:
                        metadata = json.load(metadata_file)
                    if "tokenized" not in metadata or not metadata["tokenized"]:
                        raise ValueError(
                            "Metadata indicates that the dataset is not tokenized, cannot proceed with pretraining."
                        )
                    module = PartitioningModule(
                        models_repo_path=self.models_repository_path,
                        operation=self.mode,
                    )
                    # Train the tokenizer

                    dataset_file_path = vocab_file_path.replace("_vocab.txt", ".txt")
                    if os.path.isfile(dataset_file_path):
                        # call datacollator and do your train, val, and test splits etc
                        # call train here

                        model_path = module.update_pretraining_repository(
                            dataset_file_path, metadata_file_path
                        )
                        logging.info(
                            "Updating pretraining pyramid in modelsRepo with the new model"
                        )
                        model_location = os.path.join(
                            model_path, model.config.given_name
                        )
                        # # Set mlm in args to False if using a causal language model like GPT

                        training_args = load_training_args(
                            model.config.training_args_path, model_location
                        )
                        # mlm_param = getattr(training_args, "mlm", True)
                        # mlm_prop = getattr(training_args, "mlm_probability", 0.15)
                        if not os.path.exists(model_location):
                            os.makedirs(model_location)
                        tokenizer = train_wordpiece_tokenizer(
                            vocab_file_path, metadata_file_path, model_location
                        )
                        tokenizer.save_pretrained(model_location)

                        # Create a data collator, for MLM or CLM depending on the model
                        data_collator = DataCollatorForLanguageModeling(
                            tokenizer=tokenizer,
                            mlm=True,  # Set to False if using a causal language model like GPT
                            mlm_probability=0.15,  # Only used for MLM (Masked Language Modeling)
                        )
                        train_dataset, eval_dataset, test_dataset = (
                            prepare_and_save_datasets(
                                txt_file_path=dataset_file_path,
                                output_dir=model_location,
                                tokenizer=tokenizer,
                            )
                        )
                        trainer = Trainer(
                            model=model,
                            args=training_args,
                            data_collator=data_collator,
                            train_dataset=train_dataset,
                            eval_dataset=eval_dataset,
                        )
                        trainer.train()
                        model.save_pretrained(model_location)
                        logging.info(f"Trained model saved to: {model_location}")

                        # paritoning should give me the path here

                        # Now handle the corresponding dataset file
                        logging.info(
                            f"Trained tokenizer with vocab file saved to: {model_location}"
                        )

    def __run_testing(self):
        """
        Set up components and configurations specific to testing mode.
        """
        logging.info("Initializing for testing mode.")
        # Implementation for initializing testing mode
        if self.use_tokenization and self.trajectories_list is not None:
            logging.info("Tokenizing the provided trajectories.")
            self.tokenized_trajectories = self.__tokenization_module(
                self.trajectories_list
            )
        else:
            pass
            # @Youssef DO: I need to get the attributes here
        return

    def __save_trajectories_to_store(self, dataset, operation):
        if dataset is not None:
            self.data_saved_to_trajectory_store = False
            # Generate a random dataset name
            dataset_name = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
            dataset_filename = os.path.join(
                self.trajecotry_store_path, operation, f"{dataset_name}.txt"
            )
            # Ensure the directory exists
            os.makedirs(os.path.dirname(dataset_filename), exist_ok=True)
            vocab_file_path = os.path.join(
                self.trajecotry_store_path, operation, f"{dataset_name}_vocab.txt"
            )
            # Save the tokenized trajectories to a .pkl file
            with open(dataset_filename, "w") as f:
                for trajectory in dataset:
                    for token in trajectory:
                        f.write(token)
                        f.write("[PAD]")
                    f.write("\n")
            # generate the vocab file which will be used by the tokenizer
            unique_tokens = set(token for sublist in dataset for token in sublist)
            # Write the unique tokens to the vocabulary file
            with open(vocab_file_path, "w") as vocab_file:
                vocab_file.write(f"[UNK]\n")
                vocab_file.write(f"[PAD]\n")
                vocab_file.write(f"[MASK]\n")
                for token in sorted(unique_tokens):  # Sort for consistency
                    vocab_file.write(f"{token}\n")

            # Create metadata
            # Create metadata
            metadata = {
                "total_number_of_trajectories": len(dataset),
                "total_number_of_tokens": sum(len(traj) for traj in dataset),
                "date_of_data_storage": datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "type_of_data": operation,
                "tokenized": self.trajectories_got_tokenized,
            }

            # Save metadata to a .txt file
            metadata_filename = os.path.join(
                self.trajecotry_store_path,
                operation,
                f"{dataset_name}_metadata.json",
            )
            # Ensure the directory exists
            os.makedirs(os.path.dirname(metadata_filename), exist_ok=True)
            with open(metadata_filename, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)

            logging.info("Trajectories saved to %s with metadata.", dataset_filename)
            self.data_saved_to_trajectory_store = True
            return dataset_filename, metadata_filename

    def set_tokenization_resolution(self, resolution: int = 10):
        """
        Sets the resolution to be used if tokenization is enabled.

        Args:
            resolution (int):resolution for the tokenization.

        Returns:
            None
        """
        if not self.use_tokenization:
            raise ValueError("Tokenization is not used. No need to set resolution.")
        self.resolution = resolution
        self.resolution_set_by_user = True

    def get_trajectories_from_csv(
        self, file_path: str = ""
    ) -> List[List[Tuple[float, float]]]:
        """
        Reads a CSV file containing trajectories and returns the trajectories as a list of lists of tuples.

        Each trajectory is represented as a list of (latitude, longitude) tuples.

        Args:
            file_path (str): A CSV file path containing the trajectories.

        Returns:
            List[List[Tuple[float, float]]]: List of trajectories, where each trajectory is a list of (latitude, longitude) tuples.
        """
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Initialize a list to hold the trajectories
        trajectories = []

        # Process each row in the DataFrame
        for _, row in df.iterrows():
            # Extract the trajectory string
            trajectory_str = row["trajectory"]

            # Split the trajectory string into individual points
            points_str = trajectory_str.split(",")

            # Convert the points to (latitude, longitude) tuples
            trajectory = [
                (float(point.split()[0]), float(point.split()[1]))
                for point in points_str
            ]

            # Append the trajectory to the list
            trajectories.append(trajectory)

        return trajectories

    def set_trajectories(self, trajectories: list[list[tuple[float, float]]]):
        """
        Sets the list of trajectories to be used if tokenization is enabled.

        Args:
            trajectories (list of list of tuples): List of trajectories, where each
                                trajectory is a list of (latitude, longitude) tuples.

        Returns:
            None
        """
        self.trajectories_list = trajectories
        logging.info("Trajectories set")

    def __setup_detokenization(self):
        """
        Set up de-tokenization components and configurations.
        """
        # logging.info("Setting up de-tokenization.")
        # Implementation for setting up de-tokenization

    def __setup_spatial_constraints(self):
        """
        Set up spatial constraints components and configurations.
        """
        logging.info("Setting up spatial constraints, reverting to default constraints")
        # Implementation for setting up spatial constraints
        # from constra

        self.spatial_constraints = SpatialConstraints(
            rules=None, usepredefined_rules=True
        )
        self.user_did_define_spatial_constraints = True
        # Example usage
        token = "8f2830831ffffff"  # --> This should come from the model
        previous_tokens = [
            "8f2830830ffffff",
            "8f2830831ffffff",
        ]  # --> This should be previously stored in the class
        result, rule = self.spatial_constraints.check_token(token, previous_tokens)
        if result is False:
            logging.info("Token didn't pass the following constraint: ", rule)
        else:
            logging.info("Token meets all conditions")

    def define_spatial_constraints(self, rules=None):
        """
        Modify spatial constraints based on passed rules.
        Args:
            rules (list of callables, optional): A list of functions that take a token
            and previous tokens as input and return True if the condition is met, otherwise False.
        """
        logging.info("Adding user defined spatial constraints..")

        self.spatial_constraints = SpatialConstraints(
            rules, usepredefined_rules=self.use_predefined_spatial_constraints
        )
        self.user_did_define_spatial_constraints = True
        # Example usage
        token = "8f2830831ffffff"  # --> This should come from the model
        previous_tokens = [
            "8f2830830ffffff",
            "8f2830831ffffff",
        ]  # --> This should be previously stored in the class
        result, rule = self.spatial_constraints.check_token(
            token, previous_tokens
        )  # --> This should be applied after each model output
        if result is False:
            logging.info("Token didn't pass the following constraint: ", rule)
        else:
            logging.info("Token meets all conditions")
            # Then continue your operation

    def __setup_trajectory_plugin(self):
        """
        Set up trajectory plugin components and configurations.
        """
        logging.info("Setting up trajectory plugin.")
        logging.info(self)
        # Implementation for setting up trajectory plugin

    def __modify_transformers_plugin(self):
        """
        Modify transformers plugin based on configurations.
        """
        logging.info("Modifying transformers plugin.")
        logging.info(self)
        # Implementation for modifying transformers plugin

    def define_trajectory_plugin(self):
        """
        Modify trajectory plugin based on configurations.
        """
        logging.info("Modifying trajectory plugin.")
        logging.info(self)
        # Implementation for modifying trajectory plugin

    def __tokenization_module(
        self, trajectories: list[list[tuple[float, float]]]
    ) -> list[list[str]]:
        """
        Tokenizes a list of trajectories.

        Args:
            trajectories (list of list of tuple[float, float]]): A list of trajectories,
                                                    where each trajectory is a list of
            (latitude, longitude) tuples.

        Returns:
            list of list of str: A list of tokenized trajectories, where
                                    each trajectory is a list of tokens.
        """

        if not self.resolution_set_by_user:
            info = "Tokenization Resolution Set By Default to: " + self.resolution
            logging.info(info)
        tokenized_trajectories = [
            tokenize_trajectory(trajectory, self.resolution)
            for trajectory in trajectories
        ]
        return tokenized_trajectories

    def __detokenization_module(
        self, tokenized_trajectories: list[list[str]]
    ) -> list[list[tuple[float, float]]]:
        """
        Detokenizes a list of tokenized trajectories.

        Args:
            tokenized_trajectories (list of list of str): A list of tokenized
                        trajectories, where each trajectory is a list of tokens.

        Returns:
            list of list of tuple[float, float]]: A list of detokenized trajectories,
                            where each trajectory is a list of
            (latitude, longitude) tuples.
        """

        detokenized_trajectories = [
            detokenize_trajectory(tokenized_trajectory)
            for tokenized_trajectory in tokenized_trajectories
        ]
        return detokenized_trajectories

    def __partioning_module_interface(self):
        """
        Provides an interface to the paritioning Module.
        The user doesn't have access to this function
        """
        model_path, dataset_path = None, None
        if (
            self.mode == "pretraining"
            and self.trajectories_got_tokenized
            and self.data_saved_to_trajectory_store
        ):
            # Only in the case of pretraining add to pretraining pyramids
            module = PartitioningModule(
                models_repo_path=self.models_repository_path, operation=self.mode
            )
            logging.info("Updating pyramid modelsRepo with the new dataset")
            model_path = module.update_pretraining_repository(
                self.data_path_trajectory_store, self.metadata_path_trajectory_store
            )
            # logging.info(model_path)
            dataset_path = self.data_path_trajectory_store
        elif self.mode == "finetuning":
            # @Youssef DO: Need to think about handling this here
            # print("TODO")
            pass
        elif self.mode == "testing" and self.trajectories_got_tokenized:
            module = PartitioningModule(
                models_repo_path=self.models_repository_path, operation=self.mode
            )
            logging.info("Fetching proper model from the models repo")
            model_path = module.find_proper_model(
                self.tokenized_trajectories, self.operation_type
            )
            # @Youssef DO: I need a way to load the model after getting its path, TensorFlow
            logging.info("Found proper model in the repo")
            dataset_path = None
        else:  # i.e. user entered other attributes
            # @Youssef DO: I need to think about this case
            pass
        return model_path, dataset_path

    def run(self):
        """
        Where the user is ale to run the pipeline
        """
        if (
            self.modify_spatial_constraints
            and not self.user_did_define_spatial_constraints
            and not self.use_predefined_spatial_constraints
        ):
            raise ValueError(
                "User requested to create spatial constraints from scratch without defining any constraints."
            )
        if (
            self.modify_spatial_constraints
            and not self.user_did_define_spatial_constraints
        ):
            warnings.warn(
                "User requested to modify spatial constraints without defining any constraints."
            )
        if self.mode == "pretraining":
            return self.__run_pretraining()
        elif self.mode == "testing":
            return self.__run_testing()

        logging.info("Pipeline Started Running Successfully")
