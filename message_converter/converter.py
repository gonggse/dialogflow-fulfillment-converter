import json
from .datatypes import  *
from .facebook import *
from .line import *

class Converter :
    """
    Every Channel Message will be converted to this class like generic contents
    """
    
    def __init__(self,  file_path:str, message_type:str = "line") :
        self.message_type = message_type
        self.file_path = file_path
        self.read_content_file()
        self.convert_to_generic()

    def read_content_file(self) -> dict:
        with open(self.file_path, 'r') as file:
            contents = json.load(file)
            self.contents = contents
        print(f"[INFO] Read File of '{self.file_path}' -> Success !!")
        return contents
    
    def map_message_channel(self) -> any:
        print(f"[INFO] Got message type -> {self.message_type}")
        if self.message_type == ChannelsMapping.lineChannel:
            return LineMessage.from_dict(self.contents)
        elif self.message_type == ChannelsMapping.facebookChannel:
            return FacebookMessage.from_dict(self.contents)
        else:...
    
    def convert_to_generic(self) -> GenericMessage:
        message = self.map_message_channel()
        message_dict = message.to_dict()
        self.message_generic = GenericMessage.from_dict(message_dict)
        return self.message_generic
    
    def convert_to_target_type(self, message:any, type:str) -> any:
        if type == TargetMessageType.jsonType:
            return message.to_json(indent=4, ensure_ascii=False)
        elif type == TargetMessageType.dictType:
            return message.to_dict()
        elif type == TargetMessageType.textType:
            return message.from_dict()
        elif type == TargetMessageType.object:
            return message
        else :
            return message

    def to_line_message(self, type:str= TargetMessageType.object) -> any:
        message_dict = self.message_generic.to_dict()
        message = LineMessage.from_dict(message_dict)
        return self.convert_to_target_type(message, type)
    
    def to_facebook_message(self, type:str= TargetMessageType.object) -> any:
        print(f"[INFO] Convert to: facebook type: {type}")
        message_dict = self.message_generic.to_dict()
        message = FacebookMessage.from_dict(message_dict)
        return self.convert_to_target_type(message, type)







