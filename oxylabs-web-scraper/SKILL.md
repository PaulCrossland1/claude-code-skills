---
name: oxylabs-web-scraper
description: Expert implementation of Oxylabs Web Scraper API for data collection from websites, search engines, and e-commerce platforms. Use when building web scrapers, implementing data extraction pipelines, integrating Oxylabs API, or scraping Amazon, Google, e-commerce sites, or any website. Covers Realtime, Push-Pull, and Proxy Endpoint integration methods, custom parsers, browser instructions, and geo-targeting.
---

# Oxylabs Web Scraper API

## Overview

Oxylabs Web Scraper API handles the complete scraping workflow: URL crawling, IP blocking mitigation, data extraction, and cloud storage delivery. It supports 40+ platforms including search engines, e-commerce sites, and general websites.

## Quick Reference

**Base URLs:**
- Realtime (sync): `https://realtime.oxylabs.io/v1/queries`
- Push-Pull (async): `https://data.oxylabs.io/v1/queries`
- Proxy Endpoint: `realtime.oxylabs.io:60000`

**Authentication:** HTTP Basic Auth with `USERNAME:PASSWORD` from Oxylabs dashboard.

## Integration Methods

### Realtime (Synchronous)

Keep connection open until job completes. Best for immediate results.

```python
import requests

payload = {
    "source": "universal",
    "url": "https://example.com",
    "geo_location": "United States",
    "render": "html",
    "parse": True
}

response = requests.post(
    "https://realtime.oxylabs.io/v1/queries",
    auth=("USERNAME", "PASSWORD"),
    json=payload
)
result = response.json()
```

**Response structure:**
```json
{
  "results": [{
    "content": "<html>...</html>",
    "created_at": "2024-06-26 13:13:06",
    "url": "https://example.com/",
    "job_id": "12345678900987654321",
    "status_code": 200
  }]
}
```

### Push-Pull (Asynchronous)

Submit job, retrieve results later. Recommended for large volumes.

```python
import requests
import time

# Submit job
payload = {
    "source": "universal",
    "url": "https://example.com",
    "callback_url": "https://your-webhook.com/callback"  # Optional
}

response = requests.post(
    "https://data.oxylabs.io/v1/queries",
    auth=("USERNAME", "PASSWORD"),
    json=payload
)
job = response.json()
job_id = job["id"]

# Poll for results (or use callback_url)
while True:
    status = requests.get(
        f"https://data.oxylabs.io/v1/queries/{job_id}",
        auth=("USERNAME", "PASSWORD")
    ).json()

    if status["status"] == "done":
        break
    elif status["status"] == "faulted":
        raise Exception("Job failed")
    time.sleep(2)

# Retrieve results
results = requests.get(
    f"https://data.oxylabs.io/v1/queries/{job_id}/results",
    auth=("USERNAME", "PASSWORD")
).json()
```

**Batch processing (up to 5,000 items):**
```python
payload = {
    "source": "universal",
    "url": ["https://example1.com", "https://example2.com", "https://example3.com"],
    "geo_location": "United States"
}

response = requests.post(
    "https://data.oxylabs.io/v1/queries/batch",
    auth=("USERNAME", "PASSWORD"),
    json=payload
)
```

**Result types:** `?type=raw` (HTML), `?type=parsed` (JSON), `?type=png`, `?type=markdown`

### Proxy Endpoint

Use like a standard proxy. GET requests only.

```python
import requests

proxies = {
    "http": "http://USERNAME:PASSWORD@realtime.oxylabs.io:60000",
    "https": "http://USERNAME:PASSWORD@realtime.oxylabs.io:60000"
}

response = requests.get(
    "https://example.com",
    proxies=proxies,
    verify=False,  # Required
    headers={
        "x-oxylabs-geo-location": "Germany",
        "x-oxylabs-render": "html"
    }
)
```

## Sources

### Universal Source

Scrape any website. Use `source: "universal"` with a URL.

```python
payload = {
    "source": "universal",
    "url": "https://example.com",
    "geo_location": "United States",
    "render": "html",
    "parse": True
}
```

### Amazon Sources

| Source | Purpose | Query Type |
|--------|---------|------------|
| `amazon_product` | Product page | ASIN |
| `amazon_search` | Search results | Search term |
| `amazon_pricing` | Offer listings | ASIN |
| `amazon_sellers` | Seller info | Seller ID |
| `amazon_bestsellers` | Best sellers | Category |

```python
# Product by ASIN
payload = {
    "source": "amazon_product",
    "query": "B07FZ8S74R",
    "geo_location": "90210",
    "parse": True
}

# Search
payload = {
    "source": "amazon_search",
    "query": "laptop",
    "geo_location": "United States",
    "parse": True
}
```

### Google Sources

| Source | Purpose |
|--------|---------|
| `google_search` | Web, Image, News SERPs |
| `google_ads` | Ad-optimized SERPs |
| `google_shopping_search` | Shopping results |
| `google_shopping_product` | Product pages |
| `google_maps` | Local search |
| `google_trends_explore` | Trend data |
| `google_travel_hotels` | Hotel search |
| `google_lens` | Image recognition |

```python
payload = {
    "source": "google_search",
    "query": "web scraping",
    "geo_location": "California,United States",
    "parse": True
}
```

### Other Sources

E-commerce: `walmart`, `ebay`, `etsy`, `alibaba`, `aliexpress`
Travel: `airbnb`, `zillow`
Video: `youtube_search`, `tiktok_shop`

See `references/sources.md` for complete list with parameters.

## Key Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `source` | Scraper type (required) | `"universal"` |
| `url` | Target URL | `"https://example.com"` |
| `query` | Search term or ID | `"laptop"` or `"B07FZ8S74R"` |
| `geo_location` | Proxy location | `"United States"`, `"90210"` |
| `render` | JS rendering | `"html"` or `"png"` |
| `parse` | Enable parsing | `true` |
| `user_agent_type` | Browser type | `"desktop_chrome"` |
| `callback_url` | Webhook URL | `"https://your-site.com/hook"` |
| `session_id` | Maintain same IP | `"session123"` |

## Custom Parser

Extract structured data using XPath/CSS selectors.

```python
payload = {
    "source": "universal",
    "url": "https://example.com/products",
    "parse": True,
    "parsing_instructions": {
        "product_title": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//h1[@class='title']/text()"]}
            ]
        },
        "price": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//span[@class='price']/text()"]},
                {"_fn": "amount_from_string"}
            ]
        },
        "items": {
            "_fns": [
                {"_fn": "xpath", "_args": ["//li[@class='item']/text()"]},
                {"_fn": "length"}
            ]
        }
    }
}
```

**Functions:**
- `xpath_one` - Extract single element
- `xpath` - Extract multiple elements
- `amount_from_string` - Convert text to number
- `length` - Count items

**Parser Presets:** Save parsers for reuse via `parser_preset` parameter.

See `references/custom-parser.md` for detailed syntax.

## Browser Instructions

Automate interactions before scraping (clicks, scrolling, typing).

```python
payload = {
    "source": "universal",
    "url": "https://example.com",
    "render": "html",
    "browser_instructions": [
        {"type": "wait", "wait_time_s": 2},
        {"type": "click", "selector": {"type": "css", "value": "#load-more"}},
        {"type": "wait_for_element", "selector": {"type": "css", "value": ".results"}},
        {"type": "scroll", "y": 500},
        {"type": "input", "selector": {"type": "css", "value": "#search"}, "value": "query"}
    ]
}
```

## Error Handling

**Job statuses:**
- `pending` - Processing
- `done` - Complete
- `faulted` - Error (no charge)

**Parse status codes:**
- `12000` - Success
- `12005` - Parsed with warnings
- `12002/12006/12007` - Error (no charge)

**Connection timeout:** 150 seconds TTL

## Best Practices

1. **Use Push-Pull for volume** - More reliable for large datasets
2. **Enable `render: "html"`** - When pages load content via JavaScript
3. **Use `parse: true`** - Get structured JSON instead of raw HTML
4. **Set `geo_location`** - Match target audience location
5. **Use `session_id`** - Maintain same IP for multi-page sessions
6. **Handle rate limits** - Implement exponential backoff
7. **Store results** - Configure `storage_type` and `storage_url` for S3/GCS

## Resources

- `references/sources.md` - Complete source list with parameters
- `references/custom-parser.md` - Parser syntax and functions
- `scripts/scraper.py` - Reusable scraper class
