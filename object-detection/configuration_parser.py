"""
"""
import json, yaml

class ConfigurationParser:
    """
    """
    def __init__(self, path=None, module_name=None):
        """
        """
        self._yaml_path = path
        self._module_name = module_name
        self._yaml_config_dict = self.parseYamlFile()
        self._json_path = self.getJsonConfigPath()
        self._config_dict = self.parseJsonFile()
        
    def parseJsonFile(self):
        """
        """
        config_dict = {}
        file = open(self._json_path, 'r')
        config_dict = json.load(file)
        return config_dict

    def parseYamlFile(self):
        """
        """
        config_dict = {}
        file = open(self._yaml_path, 'r')
        config_dict = yaml.load(file, Loader=yaml.FullLoader)
        return config_dict

    def getJsonConfigPath(self):
        """
        """
        return self._yaml_config_dict[self._module_name]['config_path']

    def getModelConfigPath(self):
        """
        """
        return self._yaml_config_dict[self._module_name]['model']['config_path']

    def getModelPath(self):
        """
        """
        return self._yaml_config_dict[self._module_name]['model']['model_path']

    def getMinConfidence(self):
        """
        """
        return self._yaml_config_dict[self._module_name]['model']['min_confidence']

    def getConfigValue(self, key):
        """
        """
        return self._config_dict[key]