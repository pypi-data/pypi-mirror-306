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
    resource_path = 'resources/conta_list.txt'  # Path within the package
    try:
        # Open the resource from the package using importlib.resources
        with pkg_resources.open_text('itmfinder.resources', 'conta_list.txt') as file:
            lines = file.readlines()
        # Extract the second column (taxonomic IDs) from each line if it's numeric
        tax_ids = [line.strip().split()[1] for line in lines if len(line.strip().split()) > 1 and line.strip().split()[1].isdigit()]
        return tax_ids
    except Exception as e:
        print(f"Failed to load contamination list: {e}")
        return []
