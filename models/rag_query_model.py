from pydantic import BaseModel


class QueryInput(BaseModel):
    """ 
    The construct for the request messages for RAG queries
    """
    query: str


class QueryOutput(BaseModel):
    """ 
    The construct for the response messages for RAG queries
    """
    query: str
    response: str
    sources: list[str]
