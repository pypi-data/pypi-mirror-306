"""Pipeline Class Definition"""

# On TOP of all of this, the user shall define FLOW.py which should
# give him the desired trajectory operation output
from os import path as os_path
from os import makedirs as os_makedirs

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from .utilFunctions import tokenize_trajectory, detokenize_trajectory
from .constraintsClass import SpatialConstraints
from .partioningClass import PartitioningModule
from pathlib import Path as pathlib_Path

import logging
from  warnings import filterwarnings,warn

filterwarnings(
    "ignore", category=FutureWarning, module="transformers.deepspeed"
)

from pandas import read_csv
from typing import Tuple, List
from KAFY.modelsLoader import *
from json import dump as json_dump

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
        use_detokenization: bool = True,
        modify_transformers_plugin: bool = False,
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
        self.mode,self.use_tokenization,self.use_spatial_constraints = mode,use_tokenization,use_spatial_constraints
        self.use_detokenization,self.modify_transformers_plugin = use_detokenization,modify_transformers_plugin
        self.modify_spatial_constraints,self.use_predefined_spatial_constraints,self.operation_type = modify_spatial_constraints,use_predefined_spatial_constraints,operation_type
        # Create ModelsRepo and trajectoryStore at specified projectPath if they don't exist already
        self.project_path = project_path
        self.models_repository_path = os_path.join(self.project_path, "modelsRepo")
        self.trajecotry_store_path = os_path.join(self.project_path, "trajectoryStore")
        self.transformers_plugin_path = os_path.join(self.project_path, "transformersPlugin")
        
        
        if self.mode == "startNewProject":
            self.start_new_project()
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
    def is_valid_input(self,H, L):
        if not (3 <= H <= 20):
            print("H should be between 3 and 20.")
            return False
        if not (3 <= L <= 20):
            print("L should be between 3 and 20.")
            return False
        if L >= H:
            print("L should be less than H.")
            return False
        return True

    def get_pyramid_values(self):
        pyramid_data = { "H": 5,  "L": 3,  "build_pyramid_from_scratch": True}
        # Ask the user if they want to use default values or enter custom values
        use_default = input("Do you want to use default values for Pyramid parameters (H and L)? (yes/no): ").strip().lower()
        if use_default == "no":
            try:
                # Prompt the user for input for H and L
                H = int(input("Enter the value for H (height of the pyramid, between 5 and 20): "))
                L = int(input("Enter the value for L (levels of the pyramid, between 3 and 18, must be less than H): "))

                # Validate user input
                if self.is_valid_input(H, L):
                    # Update the dictionary with the user's input if valid
                    pyramid_data["H"] = H
                    pyramid_data["L"] = L
                else:
                    logging.info("Invalid input, reverting to default values.")
            
            except ValueError:
                print("Invalid input. Please enter valid integers. Reverting to default values.")

        else:
            print("Using default pyramid data:", pyramid_data)
        return pyramid_data
# Function to validate the user input
    
    def start_new_project(self):
        try:
            project_dir_name = os_path.basename(os_path.normpath(self.project_path))
            # Check if the project path is the default and issue a warning
            if project_dir_name == "KafyProject":
                warn(
                    "No alternative project path provided. Will default to {self.project_path} directory",
                    UserWarning,
                )

            # Create the project directories if they do not exist
            if not os_path.exists(self.project_path):
                logging.info(
                    "First time creating projectDirectory, modelsRepo, trajectoryStore, transformersPlugin."
                )
                os_makedirs(self.project_path)
                os_makedirs(self.models_repository_path)
                os_makedirs(os_path.join(self.models_repository_path,"pretrainedModels"))
                os_makedirs(os_path.join(self.models_repository_path,"finetunedModels"))
                os_makedirs(self.trajecotry_store_path)
                os_makedirs(os_path.join(self.trajecotry_store_path,"pretrainedDatasets"))
                os_makedirs(os_path.join(self.trajecotry_store_path,"finetunedDatasets"))
                os_makedirs(self.transformers_plugin_path)
                logging.info("Creating necessary files in modelsRepo...")
                pyramid_data = self.get_pyramid_values()
                # Define the file path for pyramidConfigs.json
                pyramid_config_file = os_path.join(
                    self.models_repository_path, "pyramidConfigs.json"
                )
                # Write the JSON data to the file
                with open(pyramid_config_file, "w") as json_file:
                    json_dump(pyramid_data, json_file, indent=4)

                logging.info(
                    "Created the pyramid configurations for the first time."
                )
                module = PartitioningModule(
                        models_repo_path=self.models_repository_path,
                        operation=self.mode,
                    )
                # Define the paths using pathlib.Path
                self.modelsRepoJsonPretrained = pathlib_Path(self.models_repository_path) / "pretrainedModels" / 'storedModelsConfigs.json'
                self.modelsRepoJsonFinetuned = pathlib_Path(self.models_repository_path) / "finetunedModels" / 'storedModelsConfigs.json'
                self.storedDatasetsTablePretrained = pathlib_Path(self.trajecotry_store_path) / "pretrainedDatasets" / 'storedDatasetsMetadata.json'
                self.storedDatasetsTableFinetuned = pathlib_Path(self.trajecotry_store_path) / "finetunedDatasets" / 'storedDatasetsMetadata.json'

                if not self.modelsRepoJsonPretrained.exists():
                    self.modelsRepoJsonPretrained.touch()
                if not self.modelsRepoJsonFinetuned.exists():
                    self.modelsRepoJsonFinetuned.touch()
                logging.info(
                    "Created the storedModelsConfigs.json file(s) for the first time."
                )
                if not self.storedDatasetsTablePretrained.exists():
                    self.storedDatasetsTablePretrained.touch()
                if not self.storedDatasetsTableFinetuned.exists():
                    self.storedDatasetsTableFinetuned.touch()
                logging.info(
                    "Created the storedDatasetsMetadata.json file(s) for the first time."
                )
            else:
                logging.info(
                    f"Project path '{self.project_path}' already exists.   No directories were created."
                )
                

        except OSError as e:
            raise ValueError(f"Error creating project directories: {e}")

    def get_trajectories_from_csv(
        self, column_name,file_path: str = ""
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
        df = read_csv(file_path)

        # Initialize a list to hold the trajectories
        trajectories = []

        # Process each row in the DataFrame
        for _, row in df.iterrows():
            # Extract the trajectory string
            trajectory_str = row[column_name]

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
    
    def add_pretraining_data(self,trajectories_list:List[List[Tuple[float, float]]]):
        """
        Tokenizes training data if needed and adds it to trajectoryStore/pretraining/
        """
        logging.info("Case Scenario #1: Adding a pretraining dataset")
        # Implementation for initializing pretraining mode
        # This logic needs to be changed

        self.trajectories_list = trajectories_list
        

        if self.use_tokenization and self.trajectories_list is not None:
            logging.info(
                "Tokenizing the provided trajectories and adding to TrajectoryStore."
            )
            self.tokenized_trajectories = self.__tokenization_module(
                self.trajectories_list
            )
            self.trajectories_got_tokenized = True
            #need to draw MBR and see if there are models already pretrained on this dataset
            
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
