import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import torch
from tokenizers import Tokenizer
import importlib
import json
import inspect
import importlib.util
from transformers import *

# from transformers import (
#     PreTrainedTokenizerFast,
#     TrainingArguments,
#     Trainer,
#     DataCollatorForLanguageModeling,
# )
from tokenizers.models import WordPiece
from tokenizers.pre_tokenizers import Whitespace

import pandas as pd

# import torch
from sklearn.model_selection import train_test_split
from datasets import Dataset, DatasetDict

import logging

# Configure the logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
# Define the model class mapping
MODEL_CLASS_MAPPING = {
    "albert": {"model_class": AlbertForMaskedLM, "config_class": AlbertConfig},
    "bart": {"model_class": BartForCausalLM, "config_class": BartConfig},
    "bert": {"model_class": BertForMaskedLM, "config_class": BertConfig},
    "bertgeneration": {
        "model_class": BertGenerationEncoder,
        "config_class": BertGenerationConfig,
    },
    "bigbird": {"model_class": BigBirdModel, "config_class": BigBirdConfig},
    "bigbirdpegasus": {
        "model_class": BigBirdPegasusModel,
        "config_class": BigBirdPegasusConfig,
    },
    "biogpt": {"model_class": BioGptModel, "config_class": BioGptConfig},
    "blenderbot": {"model_class": BlenderbotModel, "config_class": BlenderbotConfig},
    "blenderbotsmall": {
        "model_class": BlenderbotSmallModel,
        "config_class": BlenderbotSmallConfig,
    },
    "bloom": {"model_class": BloomModel, "config_class": BloomConfig},
    "camembert": {"model_class": CamembertModel, "config_class": CamembertConfig},
    "canine": {"model_class": CanineModel, "config_class": CanineConfig},
    "codegen": {"model_class": CodeGenModel, "config_class": CodeGenConfig},
    "convbert": {"model_class": ConvBertModel, "config_class": ConvBertConfig},
    "cpmannt": {"model_class": CpmAntModel, "config_class": CpmAntConfig},
    "ctrl": {"model_class": CTRLModel, "config_class": CTRLConfig},
    "deberta": {"model_class": DebertaModel, "config_class": DebertaConfig},
    "debertav2": {"model_class": DebertaV2Model, "config_class": DebertaV2Config},
    "distilbert": {"model_class": DistilBertModel, "config_class": DistilBertConfig},
    "dpr": {"model_class": DPRQuestionEncoder, "config_class": DPRConfig},
    "electra": {"model_class": ElectraModel, "config_class": ElectraConfig},
    "encdec": {
        "model_class": EncoderDecoderModel
    },  # EncoderDecoder models are more generic
    "ernie": {"model_class": ErnieModel, "config_class": ErnieConfig},
    "erniem": {"model_class": ErnieMModel, "config_class": ErnieMConfig},
    "esm": {"model_class": EsmModel, "config_class": EsmConfig},
    "falcon": {"model_class": FalconModel, "config_class": FalconConfig},
    "flaubert": {"model_class": FlaubertModel, "config_class": FlaubertConfig},
    "fnet": {"model_class": FNetModel, "config_class": FNetConfig},
    "fsmt": {"model_class": FSMTModel, "config_class": FSMTConfig},
    "gpt2": {"model_class": GPT2LMHeadModel, "config_class": GPT2Config},
    "gptneo": {"model_class": GPTNeoModel, "config_class": GPTNeoConfig},
    "gptneox": {"model_class": GPTNeoXModel, "config_class": GPTNeoXConfig},
    "gptj": {"model_class": GPTJModel, "config_class": GPTJConfig},
    "llama": {"model_class": LlamaModel, "config_class": LlamaConfig},
    "longformer": {"model_class": LongformerModel, "config_class": LongformerConfig},
    "longt5": {"model_class": LongT5Model, "config_class": LongT5Config},
    "luke": {"model_class": LukeModel, "config_class": LukeConfig},
    "marianmt": {"model_class": MarianMTModel, "config_class": MarianConfig},
    "mbart": {"model_class": MBartModel, "config_class": MBartConfig},
    "megatronbert": {
        "model_class": MegatronBertModel,
        "config_class": MegatronBertConfig,
    },
    "mobilebert": {"model_class": MobileBertModel, "config_class": MobileBertConfig},
    "mpnet": {"model_class": MPNetModel, "config_class": MPNetConfig},
    "mt5": {"model_class": MT5Model, "config_class": MT5Config},
    "nezha": {"model_class": NezhaModel, "config_class": NezhaConfig},
    "nystromformer": {
        "model_class": NystromformerModel,
        "config_class": NystromformerConfig,
    },
    "opt": {"model_class": OPTModel, "config_class": OPTConfig},
    "pegasus": {"model_class": PegasusModel, "config_class": PegasusConfig},
    "plbart": {"model_class": PLBartModel, "config_class": PLBartConfig},
    "prophetnet": {"model_class": ProphetNetModel, "config_class": ProphetNetConfig},
    "qdqbert": {"model_class": QDQBertModel, "config_class": QDQBertConfig},
    "reformer": {"model_class": ReformerModel, "config_class": ReformerConfig},
    "rembert": {"model_class": RemBertModel, "config_class": RemBertConfig},
    "retrivbert": {"model_class": RetriBertModel, "config_class": RetriBertConfig},
    "roberta": {"model_class": RobertaModel, "config_class": RobertaConfig},
    "roformer": {"model_class": RoFormerModel, "config_class": RoFormerConfig},
    "squeezebert": {"model_class": SqueezeBertModel, "config_class": SqueezeBertConfig},
    "t5": {"model_class": T5Model, "config_class": T5Config},
    "xlm": {"model_class": XLMModel, "config_class": XLMConfig},
    "xlmroberta": {"model_class": XLMRobertaModel, "config_class": XLMRobertaConfig},
    "xlnet": {"model_class": XLNetModel, "config_class": XLNetConfig},
}


def load_training_args(json_path, model_path):
    with open(json_path, "r") as f:
        config = json.load(f)
    # print(config)
    config["output_dir"] = os.path.join(model_path, "training_results")
    return TrainingArguments(**config)


def read_and_process_file(file_path, tokenizer, max_length):
    """
    Read a text file where each line represents a trajectory and tokenize the data.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    tokenized_lines = []
    for line in lines:
        tokens = line.strip().split()
        token_ids = tokenizer.convert_tokens_to_ids(tokens)
        tokenized_lines.append(token_ids)

    return tokenized_lines


def pad_and_truncate(tokenized_lines, max_length, tokenizer):
    """
    Pad and truncate tokenized data to ensure all sequences have the same length.
    """
    padded_lines = []
    for line in tokenized_lines:
        if len(line) < max_length:
            # Padding
            padded_line = line + [tokenizer.pad_token_id] * (max_length - len(line))
        else:
            # Truncation
            padded_line = line[:max_length]
        padded_lines.append(padded_line)

    return padded_lines


def prepare_and_save_datasets(txt_file_path, output_dir, tokenizer, max_length=512):
    """
    Prepare datasets by reading, tokenizing, padding, and splitting data, then save them.
    """
    output_dir = os.path.join(output_dir, "data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read and process data
    tokenized_data = read_and_process_file(txt_file_path, tokenizer, max_length)

    # Split data
    train_data, temp_data = train_test_split(
        tokenized_data, test_size=0.2, random_state=42
    )
    val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

    # Pad and truncate
    train_data = pad_and_truncate(train_data, max_length, tokenizer)
    val_data = pad_and_truncate(val_data, max_length, tokenizer)
    test_data = pad_and_truncate(test_data, max_length, tokenizer)

    # Convert to PyTorch tensors
    train_dataset = torch.tensor(train_data, dtype=torch.long)
    val_dataset = torch.tensor(val_data, dtype=torch.long)
    test_dataset = torch.tensor(test_data, dtype=torch.long)

    # Save datasets
    torch.save(train_dataset, os.path.join(output_dir, "train_dataset.pt"))
    torch.save(val_dataset, os.path.join(output_dir, "val_dataset.pt"))
    torch.save(test_dataset, os.path.join(output_dir, "test_dataset.pt"))

    logging.info(f"Datasets saved to:{output_dir}")
    return train_dataset, val_dataset, test_dataset


# def prepare_and_save_datasets(dataset_file_path, tokenizer, output_dir):
#     """
#     Splits the tokenized trajectories in the .pkl file into train, eval, and test sets,
#     converts them to PyTorch datasets, and saves them to the specified output directory.

#     Args:
#         dataset_file_path (str): The path to the .pkl file containing tokenized trajectories.
#         output_dir (str): The directory where the datasets will be saved.

#     Returns:
#         train_dataset (torch.utils.data.TensorDataset): The training dataset.
#         eval_dataset (torch.utils.data.TensorDataset): The validation dataset.
#         test_dataset (torch.utils.data.TensorDataset): The test dataset.
#     """
#     # Check if output directory exists, otherwise create it


#     # Load the tokenized trajectories from the .pkl file
#     if not os.path.isfile(dataset_file_path):
#         raise FileNotFoundError(f"Dataset file not found at: {dataset_file_path}")

#     with open(dataset_file_path, "rb") as f:
#         data = pickle.load(f)
#     print(data[0])
#     # If data is not tokenized, tokenize it using the provided tokenizer
#     if isinstance(data[0], str):
#         data = [
#             tokenizer.encode(trajectory, truncation=True, padding="max_length")
#             for trajectory in data
#         ]

#     # Split the data into train, val, and test sets
#     train_data, temp_data = train_test_split(data, test_size=0.2, random_state=42)
#     val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)

#     # Convert the data into PyTorch tensors
#     train_dataset = torch.tensor(train_data)
#     eval_dataset = torch.tensor(val_data)
#     test_dataset = torch.tensor(test_data)

#     # Save datasets to the output directory
#     os.makedirs(output_dir, exist_ok=True)
#     torch.save(train_dataset, os.path.join(output_dir, "train_dataset.pt"))
#     torch.save(eval_dataset, os.path.join(output_dir, "eval_dataset.pt"))
#     torch.save(test_dataset, os.path.join(output_dir, "test_dataset.pt"))

#     return train_dataset, eval_dataset, test_dataset


def train_wordpiece_tokenizer(vocab_file_path, metadata_path, save_dir):
    """
    Trains a WordPiece tokenizer from a vocab file and metadata file.

    Args:
        vocab_file_path (str): Path to the vocabulary file (e.g., 'datasetname_vocab_file.txt').
        metadata_path (str): Path to the metadata file (e.g., 'datasetname_metadata.json').

    Returns:
        PreTrainedTokenizerFast: The trained WordPiece tokenizer.
    """
    # Initialize the tokenizer
    tokenizer = Tokenizer(WordPiece(unk_token="[UNK]"))

    # Set normalization to remove accents and lowercase the text
    # tokenizer.normalizer = NFD() + Lowercase() + StripAccents()

    # Set a pre-tokenizer to split by whitespace
    tokenizer.pre_tokenizer = Whitespace()

    # Load the vocabulary from the vocab file
    vocab = {}
    with open(
        vocab_file_path,
        "r",
    ) as f:
        for idx, token in enumerate(f):
            vocab[token.strip()] = idx

    # Set the vocab to the WordPiece model
    tokenizer.model = WordPiece(vocab=vocab, unk_token="[UNK]")
    tokenizer_location = os.path.join(save_dir, "tokenizerWordPiece")
    tokenizer.save(tokenizer_location)
    FastTokenizer = PreTrainedTokenizerFast(
        tokenizer_file=tokenizer_location,
        vocab_file=vocab_file_path,
        unk_token="[UNK]",
        pad_token="[PAD]",
        mask_token="[MASK]",
    )
    return FastTokenizer


def load_model_from_huggingface(model_name, config_path):
    """
    Dynamically load a model and its configuration from HuggingFace's transformers library.

    Args:
        model_name (str): The name of the model, e.g., "bert" for BertModel.
        config_path (str): Path to the model configuration file (configs.json).

    Returns:
        model (nn.Module): Instantiated transformer model.
    """

    try:
        # Capitalize the first letter of model_name
        # model_class_name = f"{model_name.capitalize()}Model"
        # config_class_name = f"{model_name.capitalize()}Config"
        model_class = MODEL_CLASS_MAPPING[model_name.lower()]["model_class"]
        config_class = MODEL_CLASS_MAPPING[model_name.lower()]["config_class"]
        # print(model_class)
        # transformers_module = importlib.import_module("transformers")
        # model_class = getattr(transformers_module, model_class_name)
        # config_class = getattr(transformers_module, config_class_name)

        # Load the configuration from the json file
        with open(config_path, "r") as f:
            config_dict = json.load(f)

        # Get the signature of the config class to know what arguments it accepts
        config_signature = inspect.signature(config_class)

        # Filter the config_dict to only include arguments accepted by the config class
        valid_config_params = {
            k: v for k, v in config_dict.items() if k in config_signature.parameters
        }

        # Initialize the configuration and model with valid parameters
        config = config_class(**valid_config_params)
        model = model_class(config)

        # logging.info(f"Loaded {model_class_name} with provided configurations.")
        return model

    except (ImportError, AttributeError) as e:
        raise ImportError(
            f"Model {model_name} is not available in HuggingFace transformers."
        )


def load_model_from_file(model_file, config_path):
    """Loads the user-defined model from a Python file."""
    spec = importlib.util.spec_from_file_location("user_defined_model", model_file)
    user_model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_model)
    with open(config_path) as config_file:
        config_data = json.load(config_file)
    model_config = user_model.ModelConfig(
        **config_data
    )  # Assuming a defined ModelConfig
    # Assuming the user defines Model class
    model = user_model.Model(model_config)
    return model
