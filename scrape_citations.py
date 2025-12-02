import json5
from models.dataset_model import Dataset
from models.publication_model import Publication
from pathlib import Path
if __name__ == "__main__":
    citations = json5.load(open("citations.json5"))
    print(f"Found {len(citations)} publications")

    all_datasets: dict[str, Dataset] = {}

    for publication_doi in citations:
        dataset_dois = citations[publication_doi]["datasets"]
        for dataset_doi in dataset_dois:
            if dataset_doi not in all_datasets:
                all_datasets[dataset_doi] = Dataset.from_doi(dataset_doi)

            all_datasets[dataset_doi].publications.append(Publication.from_doi(doi=publication_doi))

    for dataset in all_datasets:
        output_fpath = Path(__file__).parent / "data" / f"{dataset.replace('/', '--')}.json"
        with output_fpath.open("w") as f:
            f.write(all_datasets[dataset].model_dump_json(indent=4))
