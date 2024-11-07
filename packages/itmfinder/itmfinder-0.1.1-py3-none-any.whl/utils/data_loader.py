# File path: itmfinder/utils/data_loader.py
import importlib.resources as pkg_resources

def load_contamination_list():
    """
    Load the contamination list from the package resources.
    This function reads the 'conta_list.txt' from the 'resources' directory,
    parsing it to extract a list of taxonomic IDs.
    
    Returns:
        list of str: A list of taxonomic IDs.
    """
    try:
        # Open the resource from the package using importlib.resources
        with pkg_resources.files('itmfinder.resources').joinpath('conta_list.txt').open('r') as file:
            lines = file.readlines()
        
        # Extract the second column (taxonomic IDs) from each line if it's numeric
        tax_ids = [line.strip().split()[1] for line in lines if len(line.strip().split()) > 1 and line.strip().split()[1].isdigit()]
        return tax_ids
    except FileNotFoundError:
        print("The contamination list file 'conta_list.txt' was not found in 'resources'.")
        return []
    except IndexError:
        print("Failed to parse taxonomic IDs from 'conta_list.txt'. Please ensure the file format is correct.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading the contamination list: {e}")
        return []
