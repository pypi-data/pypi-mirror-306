import xml.etree.ElementTree as ET
import os
from box import Box

class ConfigReader:
    def __init__(self, xml_file):
        if 'MARKER_PATH' not in os.environ:
            raise ValueError('MARKER_PATH environment variable is not set. Please ensure it is defined in your environment.')

        if os.path.isabs(xml_file):
            self.xml_file = xml_file
        else:
            self.xml_file = os.path.join(os.environ['MARKER_PATH'], xml_file)  # Assume the XML file is in the specified path
        
        if not os.path.isfile(self.xml_file):
            raise FileNotFoundError(f'The config file does not exist: {self.xml_file}')
        
        self.config_data = self.read_config()
        self.box = Box(self.config_data)

    def reload(self):
        """Reload the configuration from the XML file."""
        self.config_data = self.read_config()
        self.box = Box(self.config_data)

    def __call__(self):
        return self.box

    def read_config(self):
        """Reads and parses the XML configuration file."""
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        config_data = {}

        # Iterate over the sections in the XML
        for section in root:
            section_data = {}

            # Iterate over each element in the section
            for element in section:
                key = element.tag
                value = element.text
                value_type = element.attrib.get('type', 'string').lower()  # Default to string if type is not specified

                # Convert the value based on its type
                if value_type == 'int':
                    section_data[key] = int(value)
                elif value_type == 'float':
                    section_data[key] = float(value)
                elif value_type == 'bool':
                    section_data[key] = value.lower() == 'true'
                elif value_type.startswith('list'):
                    # Handling lists
                    item_type = value_type.split(':')[1].lower() if ':' in value_type else 'string'
                    section_data[key] = self.parse_list(value, item_type)
                else:  # Assume string
                    section_data[key] = value
            config_data[section.tag] = section_data
        
        return config_data

    def parse_list(self, value, item_type):
        """Parse a list of items from a comma-separated string based on item_type."""
        items = value.split(',')
        if item_type == 'int':
            return [int(item) for item in items]
        elif item_type == 'float':
            return [float(item) for item in items]
        elif item_type == 'bool':
            return [item.lower() == 'true' for item in items]
        else:  # Assume string
            return items
