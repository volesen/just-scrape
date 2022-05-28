# just-scrape

A [Just Eat](https://www.just-eat.dk/) scraper, using reverse-engineered Android app endpoints.

## Usage

To run the scraping pipeline:
```bash
$ pip install -r requirements.txt
$ python src/pipeline.py
```

The scraping result is stored in the `data/` directory.

## Geo data

Postal codes and associated data were fecthed from [Dataforsyningen](https://api.dataforsyningen.dk/postnumre).