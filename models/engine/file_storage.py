#!/usr/bin/python
"""_summary_
"""


import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage():
    """Class that serializes instances to a JSON file
        and deserializes JSON file to instances.
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects

        Returns:
            dict: dictionary to store objects
        """
        if cls == None:
            return FileStorage.__objects
        else:
            cls_dict = {}
            for key, value in FileStorage.__objects.items():
                if type(value).__name__ == cls.__name__:
                    cls_dict[key] = value
            return cls_dict

    def new(self, obj):
        """sets in __objects the obj with key
            <obj class name>.id

        Args:
            obj: object 
        """
        FileStorage.__objects[f"{type(obj).__name__}.{obj.id}"] = obj

    def save(self):
        """_summary_
        """
        with open(FileStorage.__file_path, 'w', encoding='utf-8') as my_file:
            my_dict_copy = FileStorage.__objects.copy()

            for obj_key, obj_value in FileStorage.__objects.items():
                my_dict_copy[obj_key] = obj_value.to_dict()
            my_file.write(json.dumps(my_dict_copy))

    def reload(self):
        """_summary_
        """
        try:
            with open(FileStorage.__file_path, "r") as my_file2:
                my_dict = json.loads(my_file2.read())

            for obj_value in my_dict.values():
                new_object = eval(obj_value["__class__"])(**obj_value)
                self.new(new_object)
        except IOError:
            pass

    def delete(self, obj=None):
        """_summary_

        Args:
            obj (_type_, optional): _description_. Defaults to None.
        """
        if obj is not None:
            if obj in FileStorage.__objects.values():
                for key, value in FileStorage.__objects.items():
                    if value == obj:
                        del FileStorage.__objects[key]
                        break

    def close(self):
        """call reload() method for deserializing
            the JSON file to objects
        """
        self.reload()

    def get(self, cls, id):
        """method to retrieve one object"""
        objs = self.all(cls)
        for value in objs.values():
            if value.id == id:
                return value 

    def count(self, cls=None):
        """method to count the number of objects in storage"""
        objs = self.all(cls)
        return len(objs)
