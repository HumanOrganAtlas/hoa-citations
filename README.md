# Human Organ Atlas Citations

A repository to track citations of Human Organ Atlas data

## Code layout

The central data file is `citations.json5`. This contains a mapping from publication DOIs to HOA dataset DOIs.
The `scrape_citations.py` script can be run to get more information about publications (from CrossRef), and then saves one JSON file per dataset to the `data/` directory.