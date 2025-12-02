from pydantic import BaseModel

class Author(BaseModel):
    name: str
    orcid: str | None