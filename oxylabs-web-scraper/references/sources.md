# Oxylabs Web Scraper API - Complete Sources Reference

## Table of Contents
- [Universal Source](#universal-source)
- [Amazon Sources](#amazon-sources)
- [Google Sources](#google-sources)
- [E-Commerce Sources](#e-commerce-sources)
- [Travel & Real Estate](#travel--real-estate)
- [Video & Social](#video--social)
- [AI Sources](#ai-sources)

## Universal Source

Scrape any website not covered by dedicated sources.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"universal"` |
| `url` | Yes | Target URL |
| `geo_location` | No | Country name (249 supported) |
| `render` | No | `"html"` or `"png"` |
| `parse` | No | `true` for structured data |
| `user_agent_type` | No | `"desktop"`, `"desktop_chrome"`, `"mobile"` |
| `session_id` | No | String to maintain same IP |
| `parsing_instructions` | No | Custom parser object |
| `browser_instructions` | No | Browser automation array |

```python
payload = {
    "source": "universal",
    "url": "https://example.com",
    "geo_location": "United States",
    "render": "html",
    "parse": True
}
```

## Amazon Sources

### amazon_product
Product page by ASIN.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"amazon_product"` |
| `query` | Yes | ASIN (e.g., `"B07FZ8S74R"`) |
| `geo_location` | No | ZIP code or country |
| `parse` | No | `true` for structured data |

```python
payload = {
    "source": "amazon_product",
    "query": "B07FZ8S74R",
    "geo_location": "90210",
    "parse": True
}
```

### amazon_search
Search results page.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"amazon_search"` |
| `query` | Yes | Search term |
| `geo_location` | No | ZIP code or country |
| `parse` | No | `true` for structured data |
| `start_page` | No | Page number (default: 1) |
| `pages` | No | Number of pages |

```python
payload = {
    "source": "amazon_search",
    "query": "laptop",
    "geo_location": "United States",
    "parse": True,
    "pages": 3
}
```

### amazon_pricing
Offer listings for an ASIN.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"amazon_pricing"` |
| `query` | Yes | ASIN |
| `geo_location` | No | ZIP code or country |
| `parse` | No | `true` for structured data |

### amazon_sellers
Seller information page.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"amazon_sellers"` |
| `query` | Yes | Seller ID |
| `geo_location` | No | ZIP code or country |
| `parse` | No | `true` for structured data |

### amazon_bestsellers
Best sellers by category.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"amazon_bestsellers"` |
| `query` | Yes | Category URL or ID |
| `geo_location` | No | ZIP code or country |
| `parse` | No | `true` for structured data |

### amazon (generic)
Any Amazon URL.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"amazon"` |
| `url` | Yes | Full Amazon URL |
| `geo_location` | No | ZIP code or country |
| `parse` | No | Limited parsing support |

## Google Sources

### google_search
Web, Image, News SERPs.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_search"` |
| `query` | Yes | Search term |
| `geo_location` | No | `"City,State,Country"` format |
| `parse` | No | `true` for structured data |
| `start_page` | No | Page number |
| `pages` | No | Number of pages |
| `locale` | No | Language code (e.g., `"en"`) |

```python
payload = {
    "source": "google_search",
    "query": "web scraping python",
    "geo_location": "California,United States",
    "parse": True
}
```

### google_ads
Ad-optimized SERPs (limited to 10 results).

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_ads"` |
| `query` | Yes | Search term |
| `geo_location` | No | Location |
| `parse` | No | `true` for structured data |

### google_shopping_search
Shopping search results.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_shopping_search"` |
| `query` | Yes | Search term |
| `geo_location` | No | Location |
| `parse` | No | `true` for structured data |

### google_shopping_product
Individual shopping product page.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_shopping_product"` |
| `query` | Yes | Product ID |
| `geo_location` | No | Location |
| `parse` | No | `true` for structured data |

### google_maps
Local search results.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_maps"` |
| `query` | Yes | Search term |
| `geo_location` | No | Location |
| `parse` | No | `true` for structured data |

### google_trends_explore
Trend data.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_trends_explore"` |
| `query` | Yes | Trend topic |
| `geo_location` | No | Location |

### google_travel_hotels
Hotel search.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_travel_hotels"` |
| `query` | Yes | Hotel search term |
| `geo_location` | No | Location |
| `parse` | No | `true` for structured data |

### google_lens
Image recognition.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_lens"` |
| `url` | Yes | Image URL |
| `parse` | No | `true` for structured data |

### google_ai_mode
Conversational AI responses.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"google_ai_mode"` |
| `query` | Yes | Question/prompt |

## E-Commerce Sources

### walmart
| Source | Query Type |
|--------|------------|
| `walmart_search` | Search term |
| `walmart_product` | Product ID |
| `walmart` | URL |

### ebay
| Source | Query Type |
|--------|------------|
| `ebay_search` | Search term |
| `ebay_product` | Product ID |

### etsy
| Source | Query Type |
|--------|------------|
| `etsy_search` | Search term |
| `etsy_product` | Product ID |

### alibaba / aliexpress
| Source | Query Type |
|--------|------------|
| `alibaba_search` | Search term |
| `alibaba_product` | Product ID |
| `aliexpress_search` | Search term |
| `aliexpress_product` | Product ID |

### Other E-Commerce
- `bestbuy` - Best Buy
- `target` - Target
- `costco` - Costco
- `lowes` - Lowe's
- `kroger` - Kroger
- `instacart` - Instacart
- `allegro` - Allegro (EU)
- `mediamarkt` - MediaMarkt (EU)
- `cdiscount` - Cdiscount (EU)
- `idealo` - Idealo (EU)
- `lazada` - Lazada (Asia)
- `tokopedia` - Tokopedia (Asia)
- `flipkart` - Flipkart (Asia)
- `rakuten` - Rakuten (Japan)
- `mercadolibre` - MercadoLibre (LATAM)
- `magazineluiza` - Magazine Luiza (Brazil)
- `falabella` - Falabella (LATAM)

## Travel & Real Estate

### airbnb
| Source | Query Type |
|--------|------------|
| `airbnb_search` | Location search |
| `airbnb_listing` | Listing ID |

### zillow
| Source | Query Type |
|--------|------------|
| `zillow_search` | Location search |
| `zillow_property` | Property ID |

## Video & Social

### youtube
| Source | Query Type |
|--------|------------|
| `youtube_search` | Search term |
| `youtube_video` | Video ID |
| `youtube_channel` | Channel ID |
| `youtube_transcript` | Video ID (for subtitles) |

### tiktok_shop
| Source | Query Type |
|--------|------------|
| `tiktok_shop_search` | Search term |
| `tiktok_shop_product` | Product ID |

## AI Sources

### chatgpt
| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"chatgpt"` |
| `query` | Yes | Prompt |

Note: Not available in batch mode.

### perplexity
| Parameter | Required | Description |
|-----------|----------|-------------|
| `source` | Yes | `"perplexity"` |
| `query` | Yes | Prompt |

Note: Not available in batch mode.

## Geo-Location Reference

The `geo_location` parameter accepts:
- **Country names**: `"United States"`, `"Germany"`, `"Japan"`
- **US ZIP codes**: `"90210"`, `"10001"`
- **City,State,Country**: `"Los Angeles,California,United States"`
- **Coordinates**: Some sources accept lat/long

Supported: 249 countries and territories.
