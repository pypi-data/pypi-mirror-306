from typing import Optional, Union, Any

import pydantic
from pydantic import BaseModel

from silverriver.interfaces.data_models import Observation


class ChromeRole(BaseModel):
    type: str
    value: int


class PropertyValue(BaseModel):
    name: str
    value: dict


class Role(BaseModel):
    type: str
    value: str


class Name(BaseModel):
    sources: list[dict] = pydantic.Field(default_factory=list)
    type: str = ""
    value: str = ""


class AXTreeNode(BaseModel):
    backendDOMNodeId: Optional[int] = None
    childIds: list[str]
    chromeRole: ChromeRole
    frameId: Optional[str] = None
    ignored: bool
    ignoredReasons: Optional[list[PropertyValue]] = None
    name: Name
    nodeId: str
    parentId: Optional[str] = None
    properties: Optional[list[PropertyValue]] = None
    role: Role
    browsergym_id: Optional[str] = None


class AXTree(BaseModel):
    nodes: list[AXTreeNode]


class Layout(BaseModel):
    bounds: list[list[Union[int, float]]]
    clientRects: list[list[Union[int, float]]]
    nodeIndex: list[int]
    offsetRects: list[list[Union[int, float]]]
    paintOrders: list[int]
    scrollRects: list[list[Union[int, float]]]
    stackingContexts: dict[str, list[int]]
    styles: list[list]
    text: list[int]


class Nodes(BaseModel):
    attributes: list[list]
    backendNodeId: list[int]
    contentDocumentIndex: dict[str, list]
    currentSourceURL: dict[str, list]
    inputChecked: dict[str, list]
    inputValue: dict[str, list]
    isClickable: dict[str, list[Any]]
    nodeName: list[int]
    nodeType: list[int]
    nodeValue: list[int]
    optionSelected: dict[str, list]
    originURL: dict[str, list]
    parentIndex: list[int]
    pseudoIdentifier: dict[str, list]
    pseudoType: dict[str, list]
    shadowRootType: dict[str, list]
    textValue: dict[str, list]


class TextBoxes(BaseModel):
    bounds: list[list[Union[int, float]]]
    layoutIndex: list[int]
    length: list[int]
    start: list[int]


class Document(BaseModel):
    baseURL: int
    contentHeight: int
    contentWidth: int
    contentLanguage: int
    documentURL: int
    encodingName: int
    frameId: int
    layout: Layout
    nodes: Nodes
    publicId: int
    scrollOffsetX: int
    scrollOffsetY: int
    systemId: int
    textBoxes: TextBoxes
    title: int


class DOMObject(BaseModel):
    documents: list[Document]
    strings: list[str]


class ElementProperties(BaseModel):
    bbox: Union[str, list[Union[int, float]]]
    clickable: bool
    set_of_marks: bool
    visibility: float


class BrowsergymObservation(Observation, extra="forbid"):
    # Notice that Observation uses last_action_error: str as general error
    # while BrowsergymObservation uses it as last_browser_error
    # on the server we move last_action_error to last_browser_error so all the keys in browsergym
    # are the same except for the last_action_error
    active_page_index: list[int]
    axtree_object: AXTree
    dom_object: DOMObject
    elapsed_time: list[float]
    extra_element_properties: dict[str, ElementProperties]
    focused_element_bid: str
    goal: str
    goal_object: list
    last_action: str
    open_pages_titles: list[str]
    open_pages_urls: list[str]
    screenshot: str
    url: str
