import os
import uuid
import json
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import sys
import shutil


def compile_unique_dictionary_values(dictionary: dict):
    """
    Compile the values of a dictionary and remove duplicates.

    Args:
        dictionary (dict): The input dictionary.

    Returns:
        list: A list of unique values from the dictionary.
    """
    unique_elems = []
    for values in dictionary.values():
        for value in values['gold labels']:
            if value not in unique_elems:
                unique_elems.append(value)

    return unique_elems


def get_unique_elements_from_dict_values(dictionary: dict):
    unique_elements = set()
    for value in dictionary.values():
        if isinstance(value, list):
            unique_elements.update(value)
        else:
            unique_elements.add(value)
    return unique_elements


def get_substring_up_to_first_dot(s):
    """
    Returns the substring up to the first dot in the given string from left to right.

    Args:
        s (str): The input string.

    Returns:
        str: The substring up to the first dot, or the entire string if no dot is found.
    """
    dot_index = s.find('.')
    if dot_index != -1:
        return s[:dot_index]
    else:
        return s


def iterate_files_in_subfolders(parent_folder):
    """
    Iterate over all files in the subfolders of a parent folder and print their paths.

    Args:
        parent_folder (str): The path to the parent folder.
    """
    dict_of_decisions = {}
    for root, dirs, files in os.walk(parent_folder):
        for file in files:
            file_path = os.path.join(root, file)
            # Do something with the file_path
            # For example, print the file_path
            dict_of_decisions[get_substring_up_to_first_dot(file)] = file_path
    
    return dict_of_decisions


def open_json_file(file_path):
    """
    Open and read a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def upload_file_to_blob(blob_service_client, container_name, local_file_name, upload_file_path):
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

    # print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

    # Upload the created file
    with open(file=upload_file_path, mode="rb") as data:
        blob_client.upload_blob(data)


def filter_dict_keys(dictionary: dict, keys_to_keep: list):
    """
    Filter the keys in a dictionary based on a list of keys to keep.

    Args:
        dictionary (dict): The input dictionary.
        keys_to_keep (list): The list of keys to keep.

    Returns:
        dict: The filtered dictionary.
    """
    filtered_dict = {key: value for key, value in dictionary.items() if key in keys_to_keep}
    return filtered_dict


def save_copy_to_folder(file_path, destination_folder):
    """
    Save a copy of a file to a destination folder.

    Args:
        file_path (str): The full path to the file.
        destination_folder (str): The path to the destination folder.
    """
    file_name = os.path.basename(file_path)
    destination_path = os.path.join(destination_folder, file_name)
    shutil.copy(file_path, destination_path)


def copy_files_to_directory(file_paths, destination_directory):
    """
    Copies a list of files to the specified directory.

    :param file_paths: List of full paths to the files to be copied.
    :param destination_directory: Directory where the files will be copied.
    """
    # Ensure the destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Copy each file to the destination directory
    for file_path in file_paths:
        if os.path.isfile(file_path):
            shutil.copy(file_path, destination_directory)
        else:
            print(f"Warning: {file_path} does not exist or is not a file.")



if __name__ == "__main__":
    # #lee el nombre de cada archivo en los subfolders que están al interior del folder que se pasa como parámetro
    # parent_folder = r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corte Constitucional\T-1992-to-2023'
    # parent_folder = r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corte Constitucional\USB_Corte'
    # all_decisions = iterate_files_in_subfolders(parent_folder)

    # #crea una lista con los valores únicos de la lista de json
    # json_file_path = r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corpus2\benchmarks\new_queries_dict.json'
    # json_data = open_json_file(json_file_path)
    # decisiones_digesto = compile_unique_dictionary_values(json_data)

    #filtered dict keys
    # filtered_decisions = filter_dict_keys(all_decisions, decisiones_digesto)


    root_folder = r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\decisiones_digesto_educacion\txt'
    all_files = iterate_files_in_subfolders(root_folder)

    account_url = "https://corteconstitucional.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    # Create a unique name for the container
    container_name = "educacion"

    # Create the container
    container_client = blob_service_client.get_container_client(container=container_name)
    # container_client = blob_service_client.create_container(container_name)

    #upload to Blob storage 
    counter = 0
    for k,v in all_files.items():
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=k)
        print("\nUploading to Azure Storage as blob:\n\t" + k)

        with open(file=all_files[k], mode="rb") as data:
            blob_client.upload_blob(data)

    print("\nListing blobs ...")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)
        # blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob)
        # blob_client.delete_blob()





    sys.exit()
    #lee el nombre de cada archivo en los subfolders que están al interior del folder que se pasa como parámetro
    parent_folder = r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corte Constitucional\T-1992-to-2023'
    parent_folder = r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corte Constitucional\USB_Corte'
    all_decisions = iterate_files_in_subfolders(parent_folder)

    #crea una lista con los valores únicos de la lista de json
    json_file_path = r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\Corpus2\benchmarks\new_queries_dict.json'
    json_data = open_json_file(json_file_path)
    decisiones_digesto = compile_unique_dictionary_values(json_data)

    #filtered dict keys
    filtered_decisions = filter_dict_keys(all_decisions, decisiones_digesto)

    copy_files_to_directory(filtered_decisions.values(), r'C:\Users\Andres.DESKTOP-D77KM25\OneDrive - Stanford\Laboral\Lawgorithm\decisiones_digesto_educacion')




    sys.exit()
    account_url = "https://corteconstitucional.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)

    # Create a unique name for the container
    container_name = "educacion"

    # Create the container
    container_client = blob_service_client.create_container(container_name)

    #upload to Blob storage 
    counter = 0
    for k,v in filtered_decisions.items():
        # print(k,v)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=k)
        print("\nUploading to Azure Storage as blob:\n\t" + k)

        with open(file=filtered_decisions[k], mode="rb") as data:
            blob_client.upload_blob(data)

    print("\nListing blobs ...")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)








