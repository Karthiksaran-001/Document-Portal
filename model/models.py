from pydantic import BaseModel , Field , RootModel
from typing import List, Optional , Any , Dict , Union

class MetaData(BaseModel):
    Summary : List[str] = Field(default_factory=list , description= "Summary of the Document")
    Tile : str 
    Author: str 
    DateCreated: str   
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]  # Can be "Not Available"
    SentimentTone: str

class ChangeFormat(BaseModel):
    Page: str
    changes: str
    
class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass