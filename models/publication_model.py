from pydantic import BaseModel
from datetime import date, timedelta

from requests_cache import CachedSession

from models.author_model import Author

session = CachedSession(
    'publication_cache',
    use_cache_dir=True,  # Save files in the default user cache dir
    expire_after=timedelta(days=1),  # Otherwise expire responses after one day
    allowable_codes=[200, 400],  # Cache 400 responses as a solemn reminder of your failures
    allowable_methods=['GET', 'POST'],  # Cache whatever HTTP methods you want
    stale_if_error=True,  # In case of request errors, use stale cache data if possible
)


class Publication(BaseModel):
    doi: str
    title: str
    publication_date: date
    authors: list[Author]


    @classmethod
    def from_doi(cls, doi: str):
        url = f"https://api.crossref.org/works/{doi}"
        response = session.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract title (it's usually a list with one element)
        title = data['message']['title'][0]
        publication_date = date(*data["message"]["published"]["date-parts"][0])

        authors = [
            Author(
                name=f"{a["given"]} {a["family"]}" if "given" in a else a["name"],
                orcid=(a["ORCID"]) if "ORCID" in a else None
            ) for a in  data['message']['author']
        ]

        return cls(doi=doi, title=title, authors=authors, publication_date=publication_date)
