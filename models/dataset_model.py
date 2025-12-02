from pydantic import BaseModel, Field
from .publication_model import Publication
import requests

API_DOMAIN = "https://icatplus.esrf.fr"

def get_token_session() -> str:
    """
    Get session token, acts as identifier to use the API.
    """
    # Use the public credentials to access the data on ICAT
    # reader:reader is the public account
    url_post = f"{API_DOMAIN}/session"
    body_session = {"plugin": "db", "username": "reader", "password": "reader"}

    session = requests.post(url_post, json=body_session)
    return session.json()["sessionId"]

class Dataset(BaseModel):
    doi: str
    publications: list[Publication] = Field(default_factory=list)

    @classmethod
    def from_doi(cls, doi: str):
        """
        Construct a new dataset from just a DOI.
        """
        """token_session = get_token_session()

        response = requests.get(
            f"{API_DOMAIN}/icat/catalogue/{token_session}/dataset?"
            f"datasetIds=571998122,572244401,572062098&parameters=samplepatient_age~gteq~60,TOMO_total_voi_dose~lt~4",
        )
        response.raise_for_status()
        print(response.json())"""
        return cls(doi=doi)