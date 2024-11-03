import json
import urllib.request
from typing import Any, Optional
from urllib.parse import urlparse

API_URL = "https://api.rocketscraper.com"

VALID_TYPES = [
    "boolean",
    "object",
    "array",
    "number",
    "string",
    "integer",
]


class RocketClient:
    """A client for interacting with the RocketScraper API.

    This client provides methods to scrape web content using the RocketScraper service.

    Args:
        api_key (str): The API key for authentication with RocketScraper.

    Raises:
        ValueError: If the API key is empty or invalid.
    """

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("You must provide a valid API key")
        self.api_key = api_key

    def _validate_url(self, url: str) -> None:
        """Validates the provided URL.

        Args:
            url (str): The URL to validate.

        Raises:
            ValueError: If the URL is empty, malformed, or uses an unsupported protocol.
        """
        if not url:
            raise ValueError("You must provide a valid URL to scrape")

        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                raise ValueError("Invalid URL format")
            if result.scheme not in ["http", "https"]:
                raise ValueError("URL must use HTTP or HTTPS protocol")
        except Exception:
            raise ValueError("Invalid URL format")

    def _validate_schema_types(
        self, schema_part: dict, valid_types: list[str] = VALID_TYPES
    ) -> None:
        """Recursively validates schema types.

        Args:
            schema_part (dict): The schema or schema part to validate.

        Raises:
            ValueError: If the schema contains invalid types.
        """
        for key, value in schema_part.items():
            if isinstance(value, dict):
                # Recursively validate nested objects
                self._validate_schema_types(value)
            elif isinstance(value, list):
                # Validate each item in array
                for item in value:
                    if isinstance(item, dict):
                        self._validate_schema_types(item)
            else:
                if value not in valid_types:
                    raise ValueError(
                        f"Invalid type '{value}' for key '{key}'. "
                        f"Valid types are: {', '.join(valid_types)}"
                    )

    def _validate_schema(self, schema: dict[str, Any]) -> None:
        """Validates the provided schema.

        Args:
            schema (dict[str, Any]): The schema to validate.

        Raises:
            ValueError: If the schema is empty, not a dictionary
            or contains invalid types.
        """
        if not schema:
            raise ValueError("Schema cannot be empty")

        self._validate_schema_types(schema)

    def scrape(
        self, url: str, schema: dict[str, Any], task_description: Optional[str] = None
    ) -> dict[str, Any]:
        """Scrapes data from a webpage according to the provided schema.

        Args:
            url (str): The URL of the webpage to scrape.
            schema (dict[str, Any]): The schema defining what data to extract.
            task_description (Optional[str], optional): A natural language description
            of the scraping task. Defaults to None.

        Returns:
            dict[str, Any]: The scraped data structured according to the schema.

        Raises:
            ValueError: If the URL or schema is empty or invalid.
            Exception: If there's an HTTP error or network issue during the request.
        """
        self._validate_url(url)
        self._validate_schema(schema)

        data = json.dumps(
            {"url": url, "schema": schema, "task_description": task_description}
        ).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }
        req = urllib.request.Request(
            f"{API_URL}/scrape", data=data, headers=headers, method="POST"
        )

        try:
            with urllib.request.urlopen(req) as response:
                response_body = response.read()
                if response.status == 200:
                    return json.loads(response_body)
                else:
                    raise Exception(
                        f"HTTP status code {response.status}: "
                        f'{response_body.decode("utf-8")}'
                    )
        except urllib.error.URLError as e:
            raise Exception(f"Request error: {str(e)}")
