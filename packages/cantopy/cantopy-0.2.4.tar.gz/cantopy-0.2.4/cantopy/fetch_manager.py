import requests
import urllib.parse
from cantopy.xenocanto_components import Query, QueryResult, ResultPage


class FetchManager:
    """Class for managing the fetching of data from the Xeno Canto API.

    This class is responsible for sending queries to the Xeno Canto API and
    returning the results in a structured format. It is the main interface
    between the user and the Xeno Canto API.
    """

    # The base url to the XenoCanto API
    _base_url = "https://www.xeno-canto.org/api/2/recordings"

    @classmethod
    def send_query(cls, query: Query, max_pages: int = 1) -> QueryResult:
        """Send a query to the Xeno Canto API.

        Parameters
        ----------
        query
            The query to send to the Xeno Canto API.
        max_pages : optional
            Specify a maximum number of pages of recordings to fetch.
            This max_pages argument can to be passed the XenoCanto API to account for
            queries with a lot of results, since we can't fetch them all at once,
            XenoCanto divides the result up into a number of pages, which we need to
            fetch seperately. If for example, we set that max_pages attribute to 5, this
            method will only fetch the first 5 result pages.

        Returns
        -------
        QueryResult
            The QueryResult wrapper object containing the results of the query.
        """

        # We need to first send an initial query to determine the number of available result pages
        query_str = query.to_string()
        query_metadata, result_page_1 = cls._fetch_result_page(query_str, page=1)

        result_pages: list[ResultPage] = []
        result_pages.append(result_page_1)

        # Fetch the other requested result pages
        for i in range(1, min(max_pages, int(query_metadata["available_num_pages"]))):
            result_pages.append(cls._fetch_result_page(query_str, page=i + 1)[1])

        return QueryResult(query_metadata, result_pages)

    @classmethod
    def _fetch_result_page(
        cls, query_str: str, page: int
    ) -> tuple[dict[str, int], ResultPage]:
        """Fetch a specific page from the XenoCanto API.

        Parameters
        ----------
        query_str
            The query to send to the Xeno Canto API, printed in string format.
        page : optional
            The number id of the page we want to fetch.

        Returns
        -------
        tuple[dict[str, int], ResultPage]
            A tuple containing both a dictionary with query metadata (keys: "available_num_recordings",
            "available_num_species", "available_num_pages") and a ResultPage wrapper containing
            the requested page.
        """
        # Encode the http payload
        payload_str = urllib.parse.urlencode(
            {
                "query": query_str,
                "page": page,
            },
            safe=":+",
        )

        # Send request and open json return as dict
        query_response = requests.get(
            cls._base_url,
            params=payload_str,
            timeout=30.0,
        ).json()

        # Extract the metadata information of this query
        query_metadata = {
            "available_num_recordings": int(query_response["numRecordings"]),
            "available_num_species": int(query_response["numSpecies"]),
            "available_num_pages": int(query_response["numPages"]),
        }

        return query_metadata, ResultPage(query_response)
