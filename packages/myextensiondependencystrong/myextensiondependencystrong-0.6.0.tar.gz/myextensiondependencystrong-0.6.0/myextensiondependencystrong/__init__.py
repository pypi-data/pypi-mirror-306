import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def hello_world():
    return "Hello from mypackage_v0.6!"

def get_data_from_api(url):
    """Function to make a GET request to an API endpoint and return the response"""
    try:
        logging.info(f"Making GET request to {url}")
        response = requests.get(url)
        response.raise_for_status()
        logging.info("Request was successful. Processing data.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred: {e}")
        raise

def get_env_variable(var_name):
    """Retrieve the value of an environment variable, or log if not set"""
    value = os.getenv(var_name)
    if value:
        logging.info(f"Environment variable '{var_name}' found with value: {value}")
    else:
        logging.warning(f"Environment variable '{var_name}' is not set")
    return value

def set_env_variable(var_name, new_value):
    """Temporarily set an environment variable and return the old value for restoration"""
    old_value = os.getenv(var_name)
    os.environ[var_name] = new_value
    logging.info(f"Environment variable '{var_name}' set to '{new_value}' (was '{old_value}')")
    return old_value

def restore_env_variable(var_name, original_value):
    """Restore an environment variable to its original value"""
    if original_value is None:
        os.environ.pop(var_name, None)  # Remove the variable if it didn't exist before
        logging.info(f"Environment variable '{var_name}' removed")
    else:
        os.environ[var_name] = original_value
        logging.info(f"Environment variable '{var_name}' restored to '{original_value}'")
