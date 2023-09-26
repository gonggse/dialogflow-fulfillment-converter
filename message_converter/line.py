from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from .datatypes import *
from typing import Optional, Union, List, Dict
from .utils import exclude_if_none

@dataclass_json
@dataclass
class LineMessage(GenericMessage):
    def dummy(): return
    


    

        

