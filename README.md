# Dataset Manager

This `DatasetManager` program is designed to handle and manage large datasets in the form of zip files. It includes functionalities to extract specific files based on a given checklist, sort hexadecimal strings, and use multiprocessing to speed up the process. The program also uses logging to keep track of its operations.

## Features

- **Initialization**: Initialize the `DatasetManager` with paths to the dataset and a checklist.
- **Checklist Parsing**: Read and parse the checklist file to extract required file paths.
- **Zip File Listing**: List all zip files present in the dataset directory.
- **Folder Checking**: Inspect zip files to extract folder names and sort them using hexadecimal sorting.
- **Extract Specific Files**: Extract specified files from zip files and save them to an output directory.
- **Multiprocessing Support**: Use Python's `multiprocessing` to process checklist items concurrently.
- **Logging**: Log operations and errors for monitoring and debugging purposes.
- **Environment Variable Support**: Configurations can be read from environment variables using `python-dotenv`.

## Installation

Ensure you have Python installed along with the necessary packages:

```bash
pip install python-dotenv
```

## Configuration
Create a .env file in the project root directory to store the configuration paths:
```
dataset_path=/path/to/dataset
checklist_path=/path/to/checklist.txt
output_directory=/path/to/output/directory
```

## Usage
Initialize the Manager: The DatasetManager class is initialized with the dataset path and the checklist path.

Process the Checklist: The process_checklist function handles the process of extracting files listed in the checklist. It creates the output directory and uses multiprocessing to fasten the extraction process.

Run the Script: Execute the script using the following command:
```
python dataset_manager.py
```
Ensure that the necessary paths are correctly set in the .env file.

## Logging
All operations are logged in the dataset_mgr.log file, including:

- Initialization of DatasetManager
- Reading the checklist
- Listing zip files in the dataset
- Checking folders within zip files
- Reconstructing zip file names mapping
- Extracting specific files and any errors encountered during extraction

## Example
Here's an example of how to run the script programmatically:

```Python Script:
if __name__ == "__main__":
    checklistConfig = {
        "dataset_path": os.getenv("dataset_path"),
        "checklist_path": os.getenv("checklist_path"),
        "output_directory": os.getenv("output_directory"),
    }
    process_checklist(checklistConfig)
```
Ensure that the environment variables are correctly set in your .env file, and run the script to manage your dataset efficiently.

## License
This project is licensed under the AGPL-3.0 license. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please create an issue or submit a pull request.

## Author
Created by Louis Del Valle (@gh:nero-dv) Feel free to reach out for any queries or support.
