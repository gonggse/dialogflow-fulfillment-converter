from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Optional, List, Union
from .utils import exclude_if_none

# struct dataclass because of some channels have different json field
# so you can handle/convert/ignore by dataclass -> dict -> dataclass (also have nested dataclass too)
# Separate Each Channel Data Type Structs to eachfile
# - line.py
# - facebook.py
# and extension functions 
# - utils.py
@dataclass_json
@dataclass
class GenericAction:
    text: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    tyoe: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    label: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

@dataclass_json
@dataclass
class GenericComponentButton:
    type: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    action: Optional[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    style: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    color: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

@dataclass_json
@dataclass
class GenericComponentImage:
    type:str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    url:str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    size:Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    aspectRatio:Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

@dataclass_json
@dataclass
class GenericComponentText:
    type: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    text: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

@dataclass_json
@dataclass
class GenericComponentVideo:...

@dataclass_json
@dataclass
class GenericComponentBox:
    type: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    layout: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    contents: List[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

@dataclass_json
@dataclass
class GenericContainerBubble:
    type: str
    # hero depended on [LineBox, LineImage, LineComponentVideo]
    hero: Optional[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

    body: Optional[GenericComponentBox] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    size: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    footer: Optional[GenericComponentBox] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

    def __post_init__(self):
        # replace prop class after init because of many component class
        if bool(self.hero):
            self.hero = GenericComponentType.get_compoent(self.hero)
        # if bool(self.footer):
        #     footer = self.footer
        #     contents = footer._contents
        #     for component in contents:
        #         converted_component = GenericComponentType.get_compoent(component.to_dict())

@dataclass_json
@dataclass
class GenericContainerCarousel:
    type:str
    contents: Optional[ List[GenericContainerBubble]]

@dataclass_json
@dataclass
class GenericContainerInterface:
    type:str
    contents: Optional[ any]

    # def __post_init__(self):
    #     # test = GenericContainerType.get_container(self.contents)
    #     self.contents = GenericContainerType.get_container(self)
    #     print("\n +++++ ", self.contents)
    

@dataclass_json
@dataclass
class GenericAction:
    label:str
    type:str
    text:str

@dataclass_json
@dataclass
class GenericQuickReplyItems:
    type:str
    action:GenericAction

@dataclass_json
@dataclass
class GenericQuickReply:
    items: List[GenericQuickReplyItems]

@dataclass_json
@dataclass
class GenericMessage:
    text:Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    type:Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    quickReply:Optional[GenericQuickReply] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    imageURL:Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    altText:Optional[str]= field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    contents: Optional[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    originalContentUrl: Optional[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

    # to map 2 container types
    contents_carousel: Optional[GenericContainerCarousel] = field(init=False, default=None) 
    
    contents_bubble: Optional[GenericContainerBubble] = field(init=False, default=None) 
    

    def __post_init__(self):

        if self.contents:
            content = GenericContainerType.get_container(self.contents)
            self.contents = content
            self.contents_carousel = content
            self.contents_bubble = content
        
        if self.originalContentUrl:
            self.imageURL = self.originalContentUrl
            self.originalContentUrl= None
        

class ChannelsMapping:
    lineChannel:str = "line"
    facebookChannel:str = "facebook"
    webchatChennel:str = "webchat"

class TargetMessageType:
    jsonType:str = "json"
    dictType:str = 'dict'
    textType:str = "text"
    object:str = "object"

class MessageType:
    text:str = "text"
    sticker:str = "sticker"
    image:str = "image"
    video:str = "video"
    audio:str = "audio"
    location:str = "location"
    template:str = "template"
    flex:str = "flex"

class GenericContainerType:
    bubble:str = "bubble"
    carousel:str = "carousel"
    
    @classmethod
    def get_container(self, payload:"GenericContainer_Dictionary"):
        type = payload["type"]
        if type == self.bubble:
            return GenericContainerBubble.from_dict(payload)
        elif type == self.carousel:
            return GenericContainerCarousel.from_dict(payload)
        else:...

class GenericComponentType:
    box:str = "box"
    text:str = "text"
    image:str = "image"
    video:str = "video"  

    @classmethod
    def get_compoent(self, payload:dict) -> Union[GenericComponentBox, GenericComponentImage, GenericComponentVideo, GenericComponentText]:
        """
        handle each component which can be box, image, video
        """
        type = payload["type"]
        if type == self.box:
            return GenericComponentBox.from_dict(payload)
        elif type == self.image:
            return GenericComponentImage.from_dict(payload)
        elif type == self.video:
            return GenericComponentVideo.from_dict(payload)
        elif type == self.text:
            return GenericComponentText.from_dict(payload)
        else:...