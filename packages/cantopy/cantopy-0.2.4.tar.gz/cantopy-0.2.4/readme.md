# CantoPy

CantoPy is an API wrapper and download utility designed for easy scraping of animal sound recordings from the Xeno-Canto database.

## Installation

Download the latest published version of this package from PyPI by running the following command:

```bash
pip install cantopy
```

## Usage
The CantoPy package contains three main components to look up and download recordings from the Xeno-Canto API: the **Query** class, **FetchManager**, and **DownloadManager**.

The following example demonstrates how to use these components to retrieve high-quality recordings of a common blackbird (*Turdus merula*):

```python
from cantopy import Query, FetchManager, DownloadManager

# Initialize the search query
query = Query(species_name="common blackbird", quality="A")

# Find matching query results on the Xeno-Canto database
query_result = FetchManager.send_query(query, max_pages=3)

# Initialize a DownloadManager
download_manager = DownloadManager("<download_base_folder>", max_workers=2)

# Download the corresponding recordings of the retrieved results
download_manager.download_all_recordings_in_queryresult(query_result)
```