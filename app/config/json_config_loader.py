import json
from typing import Dict, List, Union

class JSONConfig:
    configuration: str = ""

    @staticmethod
    def load_config(config_type: str, file_path: str = "./") -> None:
        """
        Loads the configuration from a JSON file located at the specified path.
        
        ### Parameters:
            config_type (str): The name of the configuration file without the '.json' extension.
            file_path (str): The directory path where the configuration file is located. Defaults to the current directory.

        ### Returns:
            None
            
        ### Raises:
            Exception: If the configuration file cannot be found or loaded.
        """

        with open(file_path + config_type + '.json', 'r') as f:
            JSONConfig.configuration = json.load(f)

        if JSONConfig.configuration is None:
            raise Exception(f"configuration file not found on: {file_path + config_type}.json.")


    @staticmethod
    def get_config(keys: Union[str, List[str]]) -> str | Dict[str, str]:
        """
        Retrieves a configuration value for the specified key or nested keys.
        
        If a list of keys is provided, it traverses the nested configuration dictionary to retrieve the value.
        If no key is provided, it returns the entire configuration dictionary.
        
        ### Parameters:
            keys (Union[str, List[str]]): The key or list of keys for which to retrieve the value. Optional. 

        ### Returns:
            The configuration value corresponding to the provided key(s) or the entire configuration if no key is provided.

        ### Raises:
            Exception: If the configuration has not been loaded.
        """

        # ensure configuration is loaded
        if JSONConfig.configuration is None:
            raise Exception("Configuration not loaded, you should call load_config first.")

        # key is None then return entire configuration
        if keys is None:
            return JSONConfig.configuration

        # find value from nested keys
        elif isinstance(keys, str):
            keys = [keys]

        result = JSONConfig.configuration

        for key in keys:
            result = result.get(key, None)
            if result is None:
                break

        return result
