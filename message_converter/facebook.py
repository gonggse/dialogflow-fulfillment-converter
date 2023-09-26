from dataclasses import dataclass, field, InitVar
from dataclasses_json import dataclass_json, config
from typing import Optional, List, Dict, Union
from .utils import exclude_if_none
from .datatypes import *

@dataclass_json
@dataclass
class FacebookExtractButton(GenericComponentButton):
    # temp var
    _type: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    title: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    payload: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    url: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

    def handle_button_type(self, line_action_type: str) -> str:
        fb_button_type: str = "postback"
        if line_action_type == "message":
            self.payload = self.action["text"]
            return fb_button_type
        elif line_action_type == "uri":
            fb_button_type = "web_url"
            self.url = self.action["uri"]
            return fb_button_type
        else:
            return fb_button_type

    def __post_init__(self):
        try :
            self.title = self.action["label"]
            self.content_type = "text"
            self._type = self.handle_button_type(self.action["type"])
            self.type = self._type
            self.action = None
            self.color = None
            self.style = None
            self._type = None
        except:
            pass

@dataclass_json
@dataclass
class FacebookButton: 
    type: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    title: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    payload: str = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

@dataclass_json
@dataclass
class FacebookElement(GenericComponentButton):
    title: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    subtitle: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    image_url: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    default_action: Optional[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    payload: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    buttons: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

@dataclass_json
@dataclass
class FacebookQuickReplyItems:
    type: str = field(
        metadata=config(exclude=exclude_if_none)
    )
    action: dict = field(
        metadata=config(exclude=exclude_if_none)
    )
    title: str = field(init=False) 
    payload: str = field(init=False) 
    content_type: str = field(init=False) 

    def __post_init__(self):
        # flatten json payload from global here
        self.title = self.action["label"]
        self.payload = self.action["text"]
        self.content_type = "text"
        # remove unused target field
        self.type = None
        self.action = None

@dataclass_json
@dataclass
class FacebookInterfaceQuickReplyItems:
    items: List[FacebookQuickReplyItems] = None

# pass body but body hard-code as boxcomponent tpye **
@dataclass_json
@dataclass
class FacebookAttachmentPayloadBuilder:
    # target fields
    template_type: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    # data interface to export
    elements: Optional[ List[FacebookElement]] = field(
        metadata=config(
            exclude=exclude_if_none 
        ), 
        default=None
    )

@dataclass_json
@dataclass
class FacebookAttachmentPayload(GenericComponentBox, GenericComponentImage):
    # target fields
    url: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    template_type: Optional[str] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    # data interface to receive
    contents: Optional[ List[FacebookElement]] = field(
        metadata=config(
            exclude=exclude_if_none,
            field_name="contents" # to match with field 'contents', GenericComponentBox.contents
        ), 
        default=None
    )
    # data interface to export
    elements: Optional[ List[FacebookElement]] = field(
        metadata=config(
            exclude=exclude_if_none 
        ), 
        default=None
    )

    def __post_init__(self):
        print(self)
        self.contents = None
        self.imageUrl = None


@dataclass_json
@dataclass
class FacebookAttachment:
    type:str
    payload:FacebookAttachmentPayload

@dataclass_json
@dataclass
class FacebookMessage(GenericMessage):
    quick_replies: Optional[List] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    attachment: Optional[FacebookAttachment] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    contents_carousel: Optional[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )
    contents_bubble: Optional[any] = field(
        metadata=config(
            exclude=exclude_if_none
        ), 
        default=None
    )

    def generate_quick_reply(self) -> FacebookQuickReplyItems:
        # save old obj to dict and map dataclasses json again to FacebookInterfaceQuickReplyItems
        return FacebookInterfaceQuickReplyItems.from_dict(
                (self.quickReply.to_dict())
        )
    
    @staticmethod
    def handle_hero(contents_payload: GenericContainerBubble) -> str:
        """
        parse only image url, text(not finished) **
        """
        hero_obj = contents_payload.hero
        hero_type = hero_obj.type
        if hero_type == GenericComponentType.image:
            return hero_obj.url
        else:
            return None
        
    @staticmethod
    def handle_body(contents_bubble: GenericContainerBubble) -> dict():
        """
        extract only text from body
        """ 
        # get only first body string component 
        body_dict = {
            "text": None,
            "button_list": []
        }
        body_obj = contents_bubble.body

        if body_obj:
            try:
                body_dict["text"] = contents_bubble.body.contents[0]["text"]
            except:
                pass
            try:
                body_dict["text"] = contents_bubble.body.contents[0]["text"]
            except:
                pass
            body_dict["button_list"] = FacebookMessage.extract_button(body_obj.contents)
        
        return body_dict

    @staticmethod
    def extract_button(contents_payload: dict) -> dict:
        button_out = []
        for component in contents_payload:
            if component["type"] == "button":
                component_dict = component
                button_out.append(FacebookExtractButton.from_dict(component_dict).to_dict())
        return button_out

    @staticmethod
    def handle_footer(contents_bubble: GenericContainerBubble) -> list:
        """
        !! parse only button component from footer
        """ 
        footer_obj = contents_bubble.footer
        if footer_obj:
            footer_buttons_list = FacebookMessage.extract_button(footer_obj.contents)
            return footer_buttons_list
        
    @staticmethod
    def handle_bubble(line_contents: dict, title: str = None) -> list:
        elements = []
        contents_bubble_obj = GenericContainerBubble.from_dict(line_contents)
        hero_data = FacebookMessage.handle_hero(contents_bubble_obj)
        body_data = FacebookMessage.handle_body(contents_bubble_obj) 
        footer_data = FacebookMessage.handle_footer(contents_bubble_obj)
        buttons = body_data["button_list"] + footer_data # collect buttons from body first in sequence
        buttons_len = len(buttons)
        # partion buttons each bubble to 3 because facebook limit
        for i in range(0,buttons_len, 3):
            _buttons = buttons[i:i+3]
            _element = FacebookElement(
                    title = title,
                    subtitle = body_data["text"],
                    image_url=hero_data,
                    buttons = _buttons
                )
            elements.append(_element)
        
        return elements

    def generate_template_generic(self) -> FacebookAttachmentPayload:
        type = self.contents["type"]
        if type == "carousel":
            elements= []
            content_carouse_obj = GenericContainerCarousel.from_dict(self.contents_carousel)
            for bubble in content_carouse_obj.contents:
                bubble_dict = bubble.to_dict()
                bubble_obj = self.handle_bubble(bubble_dict, self.altText)
                elements = elements + bubble_obj

            attachment_obj = FacebookAttachmentPayload(
                template_type="generic", # ** dont hardcode here
                elements=elements
            )
        elif type == "bubble":
            bubble_obj = self.handle_bubble(self.contents_bubble, self.altText)
            attachment_obj = FacebookAttachmentPayload(
                template_type="generic", # ** dont hardcode here
                elements=bubble_obj
            )
        self.contents_bubble = None
        self.contents_carousel = None
        return attachment_obj
    
    def generate_attachment(self) -> FacebookAttachment:
        attachment_type = GenricToFacebookAttachmentType.get_attachment_type(self.type)
        if self.type == MessageType.image:
            kk = FacebookAttachment(
                attachment_type,
                FacebookAttachmentPayload(url=self.imageURL)
        )
            print(kk)
            return FacebookAttachment(
                attachment_type,
                FacebookAttachmentPayload(url=self.imageURL)
        )
        elif self.type == MessageType.template:...
        elif self.type == MessageType.flex:
            return FacebookAttachment(
                attachment_type,
                self.generate_template_generic()
        )
        elif self.type == MessageType.audio:...
        #elif self.type == MessageType.file:...

    def __post_init__(self):
        # handle quick reply
        if bool(self.quickReply) :
            self.quick_replies = self.generate_quick_reply().items
            self.quickReply = None
        
        # handle facebok attachment if type in GenricToFacebookAttachmentType
        if self.type in GenricToFacebookAttachmentType.__dict__:
            self.attachment = self.generate_attachment()
            print(self.attachment)
            self.contents = None
            self.altText = None

        # facebook doesnt have type field 
        self.type = None   

class GenricToFacebookAttachmentType:
    audio: str = "audio"
    file: str = "file"
    image: str = "image"
    template: str = "template"
    flex: str = "template"
    video: str = "video"

    # to map and return facebook attachment type
    @classmethod
    def get_attachment_type(self, obj:any) -> str:
        try :
            type = getattr(self, obj)
            return type
        except :
            return None

        

    
