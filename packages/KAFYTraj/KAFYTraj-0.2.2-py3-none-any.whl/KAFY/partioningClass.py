"""Partioning Module Definition"""

from os import path as os_path
from os import makedirs as os_makedirs
from json import load as json_load
from json import dump as json_dump

from .utilFunctions import load_metadata, load_tokenized_trajectories
from h3 import h3_to_geo
import logging
# Configure the logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
from numpy import sqrt as np_sqrt


class PartitioningModule:
    """
    A class to manage a hierarchical pyramid structure for storing and updating models
    based on trajectory datasets. The pyramid structure is defined by levels and cells,
    with each cell potentially containing a model. The class handles the initialization
    of the pyramid structure, loading configuration parameters, and updating the model
    repository with new datasets.

    Attributes:
        config_file (str): The path to the JSON configuration file.
        H (int): The number of levels in the pyramid.
        L (int): The number of cells per level.
        pyramid (dict): The hierarchical pyramid structure where each level contains cells.
        model_repo_dir (str): The directory where model files are stored, structured as
        height_level_index.
    """

    def __init__(self, models_repo_path, operation):
        """
        Initializes the PartitioningModule with configurations read from a JSON file.
        """
        self.models_repo_path = models_repo_path

        self.config_file = os_path.join(models_repo_path, "pyramidConfigs.json")
        self.operation = operation
        self.pyramid_path_pretraining = os_path.join(
            models_repo_path, "pretrainedModels", "partioningPyramid.json"
        )
        self.pyramid_path_finetuning = os_path.join(
            models_repo_path, "finetunedModels", "partioningPyramid.json"
        )
        self.pyramid_height = 5
        self.pyramid_levels = 3
        self.build_pyramid_flag = False
        self.pyramid = {}
        self.model_repo_dir = models_repo_path
        self.tokens_threshold_per_cell = 100
        self.load_config()
        if self.operation=="startNewProject":
            self.build_pyramid(self.pyramid_path_pretraining)
            self.build_pyramid(self.pyramid_path_finetuning)
        elif not self.build_pyramid_flag:
            if self.operation=="addPretrainModel":
                self.pyramid = self.load_pyramid(self.pyramid_path_pretraining)
            else:
                self.pyramid = self.load_pyramid(self.pyramid_path_finetuning)
        else:
            raise ValueError("build_pyramid_from_scratch is set to True, although pipeline is not in mode startNewProject")
            
        # print(self.pyramid)

    def load_config(self):
        """
        Loads the configuration parameters H and L from the JSON file.
        """
        default_configs = {"H": 5, "L": 3, "build_pyramid_from_scratch": True}
        if not os_path.isfile(self.config_file):
            with open(self.config_file, "w", encoding="utf-8") as file:
                json_dump(default_configs, file, indent=4)
            raise Warning(
                "Pyramid Configurations File were not found\n Will assign default configurations."
            )
        with open(self.config_file, "r", encoding="utf-8") as file:
            config = json_load(file)
            self.pyramid_height = config.get("H", 5)  # Default to 5 if not specified
            self.pyramid_levels = config.get("L", 3)  # Default to 3 if not specified
            self.build_pyramid_flag = config.get("build_pyramid_from_scratch")
       
    def _calculate_bounds(self, h, index):
        """
        Calculates the bounds for a cell at a given height and index.
        """
        # Total number of cells at height h
        num_cells = 4**h
        # Determine the number of cells per side (sqrt(num_cells))
        cells_per_side = int(np_sqrt(num_cells))

        # Calculate the size of each cell
        lat_step = 180 / cells_per_side
        lon_step = 360 / cells_per_side

        # Calculate row and column of the cell
        row = index // cells_per_side
        col = index % cells_per_side

        # Calculate bounds
        min_lat = 90 - (row * lat_step)
        max_lat = min_lat - lat_step
        min_lon = -180 + (col * lon_step)
        max_lon = min_lon + lon_step

        return (min_lat, max_lat, min_lon, max_lon)


    def _generate_cells(self, h):
        """
        Generates cells for a given height h.
        """
        num_cells = 4**h
        cells = {}
        for i in range(num_cells):
            cells[i] = {
                "height": h,
                "index": i,
                "bounds": self._calculate_bounds(h, i),
                "occupied": False,
                "model_path": None,
                "num_tokens": 0,
            }
        return cells

    def build_pyramid(self,location):
        """
        Builds the pyramid data structure for the models repository.
        """
        self.pyramid = {}  # Reset the pyramid structure
        for l in range(self.pyramid_height + 1):
            self.pyramid[l] = self._generate_cells(l)
        # Save the pyramid to the JSON file
        # Ensure the directory exists
        os_makedirs(os_path.dirname(location), exist_ok=True)
        with open(location, "w", encoding="utf-8") as file:
            json_dump(self.pyramid, file, indent=4)
        logging.info("Successfully built the partitioning Pyramid from scratch based on configurations in pyramidConfigs.json")
    def load_pyramid(self, pyramid_path=None):
        """
        Loads the pyramid data structure from the JSON file given a path to the pyramid.
        If no path is provided it defaults to the self.pyramid_path which is basically
        a combination of the modelsRepoPath/operation , i.e. I use this by default
        but if I want specifically to load a pyramid I pass the argument
        """
        if pyramid_path is None:
            pyramid_path = self.pyramid_path
        if os_path.exists(pyramid_path):
            with open(pyramid_path, "r", encoding="utf-8") as file:
                pyramid = json_load(file)
        else:
            raise FileNotFoundError(f"Pyramid file not found at {self.pyramid_path}")

        return pyramid

    def save_pyramid(self):
        os_makedirs(os_path.dirname(self.pyramid_path), exist_ok=True)
        with open(self.pyramid_path, "w", encoding="utf-8") as file:
            json_dump(self.pyramid, file, indent=4)

    def _calculate_mbr(self, trajectories):
        """
        Calculates the minimum bounding rectangle (MBR) for a set of trajectories.
        It takes a list of tokenized trajectories, detokenize them and draw the MBR
        Args:
            trajectories (list of list of tuples): List of trajectories, where each trajectory is a list of (lat, lon) tuples.

        Returns:
            tuple: A tuple representing the MBR (min_lat, max_lat, min_lon, max_lon).
        """
        latlon_trajectories = []
        # Detokenization of the trajectories
        for trajectory in trajectories:
            latlon_trajectory = []
            for token in trajectory:
                if token != "":
                    latlon_trajectory.append(h3.h3_to_geo(token))
                latlon_trajectories.append(latlon_trajectory)
        min_lat = min_lon = float("inf")
        max_lat = max_lon = float("-inf")

        for trajectory in latlon_trajectories:
            for point in trajectory:
                lat, lon = point
                min_lat = min(min_lat, lat)
                max_lat = max(max_lat, lat)
                min_lon = min(min_lon, lon)
                max_lon = max(max_lon, lon)
        # Round bounds to 2 decimal places
        min_lat = round(min_lat, 2)
        max_lat = round(max_lat, 2)
        min_lon = round(min_lon, 2)
        max_lon = round(max_lon, 2)
        # print((min_lat, max_lat, min_lon, max_lon))
        return (min_lat, max_lat, min_lon, max_lon)

    def _is_bounding_rectangle_enclosed(self, rectangle, cell_bounds):
        """
        Checks if a bounding rectangle is fully enclosed within the cell bounds.
        """
        lat_min, lat_max, lon_min, lon_max = rectangle
        cell_lat_max, cell_lat_min, cell_lon_min, cell_lon_max = cell_bounds
        return (
            lat_min >= cell_lat_min
            and lat_max <= cell_lat_max
            and lon_min >= cell_lon_min
            and lon_max <= cell_lon_max
        )


    def _find_enclosing_cell(self, bounding_rectangle):
        """
        Finds the smallest cell that fully encloses the given bounding rectangle.
        """
        for l in reversed(range(self.pyramid_height + 1)):
            for i, cell in self.pyramid[l].items():
                if self._is_bounding_rectangle_enclosed(
                    bounding_rectangle, cell["bounds"]
                ):
                    return cell
        return None
    def _update_cell_with_model(self, cell, num_tokens):
        """
        Updates the cell with a new model and stores it in the models repository.
        """
        l = cell["height"]
        index = cell["index"]
        cell_path = os_path.join(self.model_repo_dir, self.operation, f"{l}_{index}")

        # Create the directory if it doesn't exist
        if not os_path.exists(cell_path):
            os_makedirs(cell_path)

        # Define the model path
        cell["model_path"] = cell_path
        cell["occupied"] = True
        # @YoussefDo: I need to think about the logic of integrating two datasets together
        # and linking the dataset in the trajectory story to this cell
        cell["num_tokens"] = num_tokens

        # @YoussefDo: Implement logic to train and save the model in the cell_path
        # For example:
        # with open(os_path.join(cell_path, 'model.pkl'), 'wb') as f:
        #     pickle.dump(model, f)

    # We have two pyramids one for pretraining and one for finetuning
    def update_pretraining_repository(self, data_path, metadata_path):
        """
        Updates the pretraining models repository with a model.

        Args:
            data_path: The path for the new trajectory dataset to update the repository.
            metadata_path: The path for metadata of the new trajectory dataset to update the repository.
        """
        new_trajectory_dataset = load_tokenized_trajectories(data_path)
        new_trajectory_dataset_metadata = load_metadata(metadata_path)
        num_tokens = int(new_trajectory_dataset_metadata.get("total_number_of_tokens"))
        # Calculate the minimum bounding rectangle of all trajectories
        min_bounding_rectangle = self._calculate_mbr(new_trajectory_dataset)
        # print(min_bounding_rectangle)
        # Find the smallest cell that fully encloses this minimum bounding rectangle
        target_cell = self._find_enclosing_cell(min_bounding_rectangle)
        print("target cell: ", target_cell)
        # Update the model repository
        if target_cell:
            # Only add new model to cell, if #tokens is at least k*4**(H-l)
            # @YoussefDo: Make sure this is correct, to get the dataset as number of tokens

            l = target_cell["height"]
            if num_tokens >= (
                self.tokens_threshold_per_cell * 4 ** (self.pyramid_height - l)
            ):
                self._update_cell_with_model(target_cell, num_tokens)
                self.save_pyramid()
                return target_cell["model_path"]
            else:
                raise ValueError("Not sufficient data to train a model.")
        else:
            raise ValueError(
                "No suitable cell found for the given trajectories in the pyramid."
            )

    def update_repository(self, data_path, metadata_path):
        """
        Updates the model repository with a model.

        Args:
            data_path: The path for the new trajectory dataset to update the repository.
            metadata_path: The path for metadata of the new trajectory dataset to update the repository.
        """
        new_trajectory_dataset = load_tokenized_trajectories(data_path)
        new_trajectory_dataset_metadata = load_metadata(metadata_path)
        num_tokens = new_trajectory_dataset_metadata.get("total_number_of_tokens")
        # Calculate the minimum bounding rectangle of all trajectories
        min_bounding_rectangle = self._calculate_mbr(new_trajectory_dataset)

        # Find the smallest cell that fully encloses this minimum bounding rectangle
        target_cell = self._find_enclosing_cell(min_bounding_rectangle)

        # Update the model repository
        if target_cell:
            # Only add new model to cell, if #tokens is at least k*4**(H-l)
            # @YoussefDo: Make sure this is correct, to get the dataset as number of tokens

            l = target_cell["height"]
            if num_tokens >= (
                self.tokens_threshold_per_cell * 4 ** (self.pyramid_height - l)
            ):
                self._update_cell_with_model(target_cell, num_tokens)
            else:
                raise ValueError("Not sufficient data to train a model.")
        else:
            raise ValueError(
                "No suitable cell found for the given trajectories in the pyramid."
            )

    def find_proper_model(self, test_data, operation_type):
        """
        Used in the testing mode to find the proper model for the passed query data

        Args:
            test_data: trajectory test data used to find proper model and load it in memory
        """
        pyramid = self.load_pyramid(self.pyramid_path)
        print(operation_type, pyramid)
        # Calculate the minimum bounding rectangle of all trajectories
        min_bounding_rectangle = self._calculate_mbr(test_data)

        # Find the smallest cell that fully encloses this minimum bounding rectangle
        target_cell = self._find_enclosing_cell(min_bounding_rectangle)
        if target_cell:  # Then we found a cell that encloses this trajectory data
            # @YoussefDo: need to load the model here
            model_path = target_cell["model_path"]
            # Tensorflow load model
            # print(model_path)
        else:
            raise ValueError(
                "No proper model found for requested trajectory query data"
            )
        return model_path
