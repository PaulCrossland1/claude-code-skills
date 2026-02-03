#!/usr/bin/env python3
"""
Oxylabs Web Scraper API - Reusable Scraper Class

A comprehensive wrapper for the Oxylabs Web Scraper API supporting
Realtime, Push-Pull, and Proxy Endpoint integration methods.

Usage:
    from scraper import OxylabsScraper

    scraper = OxylabsScraper("USERNAME", "PASSWORD")

    # Realtime scraping
    result = scraper.scrape("https://example.com")

    # Amazon product
    result = scraper.amazon_product("B07FZ8S74R")

    # Google search
    result = scraper.google_search("web scraping")

    # Async batch scraping
    job_ids = scraper.batch_scrape(["https://url1.com", "https://url2.com"])
    results = scraper.get_results(job_ids)
"""

import requests
import time
from typing import Optional, Union, List, Dict, Any


class OxylabsScraper:
    """Oxylabs Web Scraper API wrapper."""

    REALTIME_URL = "https://realtime.oxylabs.io/v1/queries"
    ASYNC_URL = "https://data.oxylabs.io/v1/queries"
    BATCH_URL = "https://data.oxylabs.io/v1/queries/batch"
    PROXY_HOST = "realtime.oxylabs.io"
    PROXY_PORT = 60000

    def __init__(self, username: str, password: str):
        """
        Initialize the scraper with Oxylabs credentials.

        Args:
            username: Oxylabs API username
            password: Oxylabs API password
        """
        self.auth = (username, password)
        self.session = requests.Session()
        self.session.auth = self.auth

    def scrape(
        self,
        url: str,
        source: str = "universal",
        geo_location: Optional[str] = None,
        render: Optional[str] = None,
        parse: bool = False,
        parsing_instructions: Optional[Dict] = None,
        browser_instructions: Optional[List[Dict]] = None,
        user_agent_type: Optional[str] = None,
        session_id: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Scrape a URL using the Realtime API.

        Args:
            url: Target URL to scrape
            source: Scraper source (default: "universal")
            geo_location: Proxy location (e.g., "United States")
            render: Rendering mode ("html" or "png")
            parse: Enable parsing (default: False)
            parsing_instructions: Custom parser configuration
            browser_instructions: Browser automation steps
            user_agent_type: Browser type (e.g., "desktop_chrome")
            session_id: Session ID to maintain same IP
            **kwargs: Additional parameters

        Returns:
            API response as dictionary
        """
        payload = {
            "source": source,
            "url": url,
        }

        if geo_location:
            payload["geo_location"] = geo_location
        if render:
            payload["render"] = render
        if parse:
            payload["parse"] = parse
        if parsing_instructions:
            payload["parsing_instructions"] = parsing_instructions
        if browser_instructions:
            payload["browser_instructions"] = browser_instructions
        if user_agent_type:
            payload["user_agent_type"] = user_agent_type
        if session_id:
            payload["session_id"] = session_id

        payload.update(kwargs)

        response = self.session.post(self.REALTIME_URL, json=payload)
        response.raise_for_status()
        return response.json()

    def amazon_product(
        self,
        asin: str,
        geo_location: str = "United States",
        parse: bool = True
    ) -> Dict[str, Any]:
        """
        Scrape an Amazon product page.

        Args:
            asin: Amazon Standard Identification Number
            geo_location: Location (ZIP code or country)
            parse: Enable parsing (default: True)

        Returns:
            Parsed product data
        """
        payload = {
            "source": "amazon_product",
            "query": asin,
            "geo_location": geo_location,
            "parse": parse
        }

        response = self.session.post(self.REALTIME_URL, json=payload)
        response.raise_for_status()
        return response.json()

    def amazon_search(
        self,
        query: str,
        geo_location: str = "United States",
        parse: bool = True,
        pages: int = 1
    ) -> Dict[str, Any]:
        """
        Search Amazon.

        Args:
            query: Search term
            geo_location: Location
            parse: Enable parsing
            pages: Number of pages to retrieve

        Returns:
            Search results
        """
        payload = {
            "source": "amazon_search",
            "query": query,
            "geo_location": geo_location,
            "parse": parse,
            "pages": pages
        }

        response = self.session.post(self.REALTIME_URL, json=payload)
        response.raise_for_status()
        return response.json()

    def google_search(
        self,
        query: str,
        geo_location: Optional[str] = None,
        parse: bool = True,
        pages: int = 1
    ) -> Dict[str, Any]:
        """
        Search Google.

        Args:
            query: Search term
            geo_location: Location (e.g., "California,United States")
            parse: Enable parsing
            pages: Number of pages

        Returns:
            Search results
        """
        payload = {
            "source": "google_search",
            "query": query,
            "parse": parse,
            "pages": pages
        }

        if geo_location:
            payload["geo_location"] = geo_location

        response = self.session.post(self.REALTIME_URL, json=payload)
        response.raise_for_status()
        return response.json()

    def submit_async(
        self,
        url: str,
        source: str = "universal",
        callback_url: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Submit an async job (Push-Pull).

        Args:
            url: Target URL
            source: Scraper source
            callback_url: Webhook URL for completion notification
            **kwargs: Additional parameters

        Returns:
            Job ID
        """
        payload = {
            "source": source,
            "url": url,
        }

        if callback_url:
            payload["callback_url"] = callback_url

        payload.update(kwargs)

        response = self.session.post(self.ASYNC_URL, json=payload)
        response.raise_for_status()
        return response.json()["id"]

    def batch_scrape(
        self,
        urls: List[str],
        source: str = "universal",
        geo_location: Optional[str] = None,
        **kwargs
    ) -> List[str]:
        """
        Submit batch scraping job (up to 5,000 URLs).

        Args:
            urls: List of URLs to scrape
            source: Scraper source
            geo_location: Proxy location
            **kwargs: Additional parameters

        Returns:
            List of job IDs
        """
        payload = {
            "source": source,
            "url": urls,
        }

        if geo_location:
            payload["geo_location"] = geo_location

        payload.update(kwargs)

        response = self.session.post(self.BATCH_URL, json=payload)
        response.raise_for_status()

        result = response.json()
        return [query["id"] for query in result.get("queries", [])]

    def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get job status.

        Args:
            job_id: Job ID from submit_async or batch_scrape

        Returns:
            Job status information
        """
        response = self.session.get(f"{self.ASYNC_URL}/{job_id}")
        response.raise_for_status()
        return response.json()

    def get_results(
        self,
        job_id: str,
        result_type: str = "parsed",
        poll_interval: float = 2.0,
        timeout: float = 300.0
    ) -> Dict[str, Any]:
        """
        Wait for and retrieve job results.

        Args:
            job_id: Job ID
            result_type: "raw", "parsed", "png", or "markdown"
            poll_interval: Seconds between status checks
            timeout: Maximum wait time in seconds

        Returns:
            Job results

        Raises:
            TimeoutError: If job doesn't complete within timeout
            RuntimeError: If job fails
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            status = self.get_status(job_id)

            if status["status"] == "done":
                response = self.session.get(
                    f"{self.ASYNC_URL}/{job_id}/results",
                    params={"type": result_type}
                )
                response.raise_for_status()
                return response.json()

            elif status["status"] == "faulted":
                raise RuntimeError(f"Job {job_id} failed")

            time.sleep(poll_interval)

        raise TimeoutError(f"Job {job_id} timed out after {timeout}s")

    def get_proxy_url(self) -> str:
        """
        Get proxy URL for Proxy Endpoint integration.

        Returns:
            Proxy URL string
        """
        username, password = self.auth
        return f"http://{username}:{password}@{self.PROXY_HOST}:{self.PROXY_PORT}"

    def scrape_via_proxy(
        self,
        url: str,
        geo_location: Optional[str] = None,
        render: Optional[str] = None
    ) -> requests.Response:
        """
        Scrape via Proxy Endpoint (GET requests only).

        Args:
            url: Target URL
            geo_location: Proxy location
            render: Rendering mode

        Returns:
            requests.Response object
        """
        proxy_url = self.get_proxy_url()
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

        headers = {}
        if geo_location:
            headers["x-oxylabs-geo-location"] = geo_location
        if render:
            headers["x-oxylabs-render"] = render

        return requests.get(
            url,
            proxies=proxies,
            headers=headers,
            verify=False
        )


def main():
    """Example usage."""
    import os

    username = os.environ.get("OXYLABS_USERNAME", "YOUR_USERNAME")
    password = os.environ.get("OXYLABS_PASSWORD", "YOUR_PASSWORD")

    scraper = OxylabsScraper(username, password)

    # Example: Scrape a website
    print("Scraping example.com...")
    result = scraper.scrape(
        "https://example.com",
        render="html"
    )
    print(f"Status: {result['results'][0]['status_code']}")

    # Example: Amazon product
    print("\nFetching Amazon product...")
    result = scraper.amazon_product("B07FZ8S74R")
    if result.get("results"):
        content = result["results"][0].get("content", {})
        print(f"Title: {content.get('title', 'N/A')}")

    # Example: Google search
    print("\nSearching Google...")
    result = scraper.google_search("python web scraping")
    if result.get("results"):
        content = result["results"][0].get("content", {})
        organic = content.get("results", {}).get("organic", [])
        print(f"Found {len(organic)} organic results")


if __name__ == "__main__":
    main()
