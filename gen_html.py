import markdown
from pathlib import Path
from models.dataset_model import Dataset
from models.publication_model import Publication
from scrape_citations import scrape

if __name__ == "__main__":
    scrape()
    md_text = ""
    md_text += "# Research using data from [The Human Organ Atlas](https://human-organ-atlas.esrf.fr/)\n"
    md_text += "\n"

    pubs: dict[str, Publication] = {}
    for dataset_path in (Path(__file__).parent / "data").glob("*.json"):
        dataset = Dataset.model_validate_json(open(dataset_path).read())
        for pub in dataset.publications:
            pubs[pub.doi] = pub

    pubs_sorted = sorted(pubs.values(), key=lambda pub: pub.publication_date)
    md_text += f"Number of publications: {len(pubs_sorted)}\n"
    md_text += "<hr>\n"
    for pub in pubs_sorted[::-1]:
        authors = ", ".join([p.name.replace(" ", "&nbsp;") for p in pub.authors])
        md_text += f"**{pub.title}**<br><br>{authors} ({pub.publication_date.year})<br><br>[DOI:{pub.doi}](https://dx.doi.org/{pub.doi})\n"
        md_text += "<hr>\n"
    md_text += "*Is your publication missing? Email d.stansby@ucl.ac.uk with the publication DOI, and a list of HOA datasets it uses.*"
    html = markdown.markdown(md_text)

    with open(Path(__file__).parent / "html" / "index.html", "w", encoding="UTF-8") as f:
        f.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
        f.write('<link rel="stylesheet" href="style.css">\n')
        f.write("<body>\n")
        f.write(html)
        f.write("</body>\n")
