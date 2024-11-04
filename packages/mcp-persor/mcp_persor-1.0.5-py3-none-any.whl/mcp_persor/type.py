from typing import Optional, TypedDict, List

class JointData(TypedDict):
    joint: Optional[str]
    children: List[str]
    offset: List[int]
    channels: List[str]
