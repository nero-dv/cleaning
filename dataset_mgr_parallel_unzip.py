import os
import logging
import zipfile
from typing import List, Tuple, Dict
from multiprocessing import Pool
from sort_hex import HexadecimalSorter
from dotenv import load_dotenv

load_dotenv()

# Configuring logging
logging.basicConfig(
    filename="dataset_mgr.log", level=logging.INFO, format="%(levelname)s:%(asctime)s:%(message)s"
)


class DatasetManager:
    def __init__(self, dataset_path: str, checklist_path: str):
        """
        Initialize the DatasetManager with dataset and checklist paths.

        :param dataset_path: Path to the dataset directory.
        :param checklist_path: Path to the checklist file.
        """
        self.dataset_path = dataset_path
        self.checklist_path = checklist_path
        logging.info(
            f"Initialized DatasetManager with dataset_path: {dataset_path} and checklist_path: {checklist_path}"
        )

    def check_dir(self) -> List[Tuple[str, str]]:
        """
        Read the checklist file and create a list of tuples.
        Each tuple contains a file path and its corresponding subdirectory.

        :return: List of tuples (file path, subdirectory).
        """
        with open(self.checklist_path, "r") as f:
            lines = f.readlines()
        logging.info(f"Read directory checklist from {self.checklist_path}")
        return [(line.strip(), line.strip().split("/")[1]) for line in lines]

    def list_zips_in_dataset(self) -> List[str]:
        """
        List all zip files in the dataset directory that contain an underscore in their name.

        :return: List of zip file names.
        """
        zip_files = [
            file
            for root, dirs, files in os.walk(self.dataset_path)
            for file in files
            if "zip" in file and "_" in file
        ]
        logging.info(f"Listed zip files in dataset: {zip_files}")
        return zip_files

    def check_folders_in_zip(self, zip_path: str) -> tuple:
        """
        Extract and sort folder names from a given zip file based on hexadecimal values.

        :param zip_path: Path to the zip file.
        :return: Sorted tuple of folder names.
        """
        hs = HexadecimalSorter()
        logging.info(f"Checking folders in zip file: {zip_path}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            file_names_in_zip: List[str] = [file for file in zip_ref.namelist()]
            prefixes: set[str] = {file.split("/")[0] for file in file_names_in_zip}
            sorted_prefixes = hs.sort_hexadecimal_strings(unsorted_hex_values=tuple(prefixes))
        return sorted_prefixes

    def reconstruct_zip_name(self) -> Dict[str, str]:
        """
        Create a mapping from folder names to their respective zip file names.

        :return: Dictionary mapping folder names to zip file names.
        """
        zips: List[str] = self.list_zips_in_dataset()
        subdir_map = {}
        for zip_file in zips:
            zip_path: str = os.path.join(self.dataset_path, zip_file)
            subfolders = self.check_folders_in_zip(zip_path)
            subdir_map.update({folder: zip_file for folder in subfolders})
        logging.info(f"Reconstructed zip name map: {subdir_map}")
        return subdir_map

    def extract_specific_file(self, zip_file: str, file_to_extract: str, output_dir: str) -> None:
        """
        Extract a specific file from a zip archive to the output directory.

        :param zip_file: Path to the zip file.
        :param file_to_extract: File path inside the zip to extract.
        :param output_dir: Output directory to extract the file to.
        """
        logging.info(f"Extracting {file_to_extract} from {zip_file} to {output_dir}")
        with zipfile.ZipFile(file=zip_file, mode="r") as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith(prefix := file_to_extract.split("/")[0]) and file.endswith(
                    file_to_extract
                ):
                    try:
                        zip_ref.extract(member=file, path=output_dir)
                        logging.info(f"Extracted {file} to {output_dir}")
                    except Exception as e:
                        logging.error(f"Failed to extract {file} to {output_dir}: {e}")
                        continue


def process_checklist_item(args):
    """
    Process a single checklist item by extracting the specified file.

    :param args: Tuple containing manager, item, prefix, zip file path, and output directory.
    """
    manager, item, prefix, zip_file_path, output_directory = args
    manager.extract_specific_file(zip_file_path, item.lstrip("./"), output_directory)


def process_checklist(config: dict):
    """
    Process the checklist based on the given configuration.

    :param config: Configuration dictionary containing dataset_path, checklist_path, and output_directory.
    """
    dataset_path, checklist_path, output_directory = (
        config["dataset_path"],
        config["checklist_path"],
        config["output_directory"],
    )

    os.makedirs(output_directory, exist_ok=True)
    logging.info(f"Output directory {output_directory} created")

    manager = DatasetManager(dataset_path, checklist_path)
    zip_dir_map: Dict[str, str] = manager.reconstruct_zip_name()
    checklist: List[Tuple[str, str]] = manager.check_dir()

    tasks = [
        (
            manager,
            item,
            prefix,
            os.path.abspath(os.path.join(dataset_path, zip_dir_map[prefix])),
            output_directory,
        )
        for item, prefix in checklist
        if prefix in zip_dir_map
    ]

    with Pool() as pool:
        pool.map(process_checklist_item, tasks)


if __name__ == "__main__":
    checklistConfig = {
        "dataset_path": os.getenv("dataset_path"),
        "checklist_path": os.getenv("checklist_path"),
        "output_directory": os.getenv("output_directory"),
    }
    process_checklist(checklistConfig)
