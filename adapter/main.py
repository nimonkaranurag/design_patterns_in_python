from abc import ABC, abstractmethod
from pathlib import Path
import json
import rich
from typing import Dict
import xml.etree.ElementTree as ET

class Display:

    def __init__(self, **kwargs):

        assert kwargs

        self.records=[
            (field,kwargs[field]) for field in kwargs.keys()
        ]
    
    def display(self):

        rich.print(
            "📜 [b cyan] The following data was loaded:\n[/b cyan][b yellow]"
            f"{str(self)}"
        )

    def __str__(self):
        return "\n-".join(f"{key} | {value}" for key, value in self.records)


class FileReader(ABC):

    def __init__(self, file_path: Path):
        self.file_path = file_path

    @abstractmethod
    def read(self) -> str:
        pass

class JSONFileReader(FileReader):
    
    def read(self):
        with open(self.file_path, "r") as f:
            content = f.read()
    
        return content
    
class XMLFileReader(FileReader):
    
    def read(self):
        with open(self.file_path, "r") as f:
            content = f.read()
        
        return content

class DisplayAdapter(ABC):

    def __init__(self, file_reader: FileReader):
        self.file_reader = file_reader
    
    @abstractmethod
    def get_records(self) -> Dict[str, str]:
        pass

class JSONAdapter(DisplayAdapter):

    def get_records(self):

        json_string = self.file_reader.read()

        return json.loads(json_string)

class XMLAdapter(DisplayAdapter):

    def get_records(self):
        
        xml_string = self.file_reader.read()
        root = ET.fromstring(xml_string)
        
        records_list = []
        
        for book in root.findall('book'):

            record = {}
            record['id'] = book.get('id', '')
            
            for child in book:
                record[child.tag] = child.text.strip() if child.text else ''
            
            records_list.append(record)
        
        return records_list

if __name__=="__main__":
    
    json_reader = JSONFileReader(Path("adapter/data/dummy.json"))
    json_adapter = JSONAdapter(json_reader)
    records_list = json_adapter.get_records()
    
    for idx, records in enumerate(records_list, 1):
        Display(**records).display()

    xml_reader = XMLFileReader(Path("adapter/data/dummy.xml"))
    xml_adapter = XMLAdapter(xml_reader)
    records_list = xml_adapter.get_records()
    
    for idx, records in enumerate(records_list, 1):
        Display(**records).display()