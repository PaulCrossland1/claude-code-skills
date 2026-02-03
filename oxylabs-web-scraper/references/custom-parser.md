# Custom Parser Reference

## Table of Contents
- [Overview](#overview)
- [Syntax](#syntax)
- [Functions](#functions)
- [Examples](#examples)
- [Parser Presets](#parser-presets)
- [Status Codes](#status-codes)

## Overview

Custom Parser extracts structured data from HTML using XPath/CSS selectors. Functions are chained in a pipeline where each function takes the output of the previous.

## Syntax

```json
{
    "source": "universal",
    "url": "https://example.com",
    "parse": true,
    "parsing_instructions": {
        "field_name": {
            "_fns": [
                {"_fn": "function_name", "_args": ["argument1", "argument2"]},
                {"_fn": "next_function"}
            ]
        }
    }
}
```

**Key points:**
- `parse: true` must be set
- Field names become keys in the output JSON
- Functions execute in order, passing output to the next
- `_fns` is an array of function objects
- `_fn` specifies the function name
- `_args` provides function arguments

## Functions

### xpath_one
Extract a single element using XPath.

```json
{"_fn": "xpath_one", "_args": ["//h1/text()"]}
```

**Common XPath patterns:**
- `//h1/text()` - Text content of h1
- `//div[@class='price']/text()` - Text of div with class
- `//a/@href` - href attribute of links
- `//img/@src` - src attribute of images
- `//meta[@name='description']/@content` - Meta tag content
- `//span[contains(@class, 'rating')]/text()` - Partial class match

### xpath
Extract multiple elements as an array.

```json
{"_fn": "xpath", "_args": ["//li[@class='item']/text()"]}
```

### css_one
Extract a single element using CSS selector.

```json
{"_fn": "css_one", "_args": [".product-title"]}
```

### css
Extract multiple elements using CSS selector.

```json
{"_fn": "css", "_args": [".product-item"]}
```

### amount_from_string
Convert text containing numbers to numeric value.

```json
{"_fn": "amount_from_string"}
```

Input: `"$1,234.56"` → Output: `1234.56`

### length
Count items in an array.

```json
{"_fn": "length"}
```

### join
Join array elements into a string.

```json
{"_fn": "join", "_args": [", "]}
```

### split
Split string into array.

```json
{"_fn": "split", "_args": [","]}
```

### trim
Remove whitespace from string.

```json
{"_fn": "trim"}
```

### regex
Extract using regular expression.

```json
{"_fn": "regex", "_args": ["\\d+"]}
```

### select_nth
Select nth element from array (0-indexed).

```json
{"_fn": "select_nth", "_args": [0]}
```

## Examples

### Product Page Parser

```python
payload = {
    "source": "universal",
    "url": "https://example.com/product",
    "parse": True,
    "parsing_instructions": {
        "title": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//h1[@class='product-title']/text()"]},
                {"_fn": "trim"}
            ]
        },
        "price": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//span[@class='price']/text()"]},
                {"_fn": "amount_from_string"}
            ]
        },
        "rating": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//div[@class='rating']/@data-score"]},
                {"_fn": "amount_from_string"}
            ]
        },
        "description": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//div[@class='description']/text()"]}
            ]
        },
        "images": {
            "_fns": [
                {"_fn": "xpath", "_args": ["//div[@class='gallery']//img/@src"]}
            ]
        },
        "features": {
            "_fns": [
                {"_fn": "xpath", "_args": ["//ul[@class='features']/li/text()"]}
            ]
        }
    }
}
```

### Search Results Parser

```python
payload = {
    "source": "universal",
    "url": "https://example.com/search?q=laptop",
    "parse": True,
    "parsing_instructions": {
        "total_results": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//span[@class='result-count']/text()"]},
                {"_fn": "regex", "_args": ["\\d+"]},
                {"_fn": "amount_from_string"}
            ]
        },
        "products": {
            "_fns": [
                {"_fn": "xpath", "_args": ["//div[@class='product-card']"]},
                {
                    "_fn": "foreach",
                    "_args": {
                        "name": {"_fns": [{"_fn": "xpath_one", "_args": [".//h2/text()"]}]},
                        "price": {"_fns": [{"_fn": "xpath_one", "_args": [".//span[@class='price']/text()"]}, {"_fn": "amount_from_string"}]},
                        "link": {"_fns": [{"_fn": "xpath_one", "_args": [".//a/@href"]}]}
                    }
                }
            ]
        }
    }
}
```

### News Article Parser

```python
payload = {
    "source": "universal",
    "url": "https://news-site.com/article",
    "parse": True,
    "parsing_instructions": {
        "headline": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//h1/text()"]}
            ]
        },
        "author": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//span[@class='author']/text()"]}
            ]
        },
        "date": {
            "_fns": [
                {"_fn": "xpath_one", "_args": ["//time/@datetime"]}
            ]
        },
        "content": {
            "_fns": [
                {"_fn": "xpath", "_args": ["//article//p/text()"]},
                {"_fn": "join", "_args": ["\n\n"]}
            ]
        },
        "tags": {
            "_fns": [
                {"_fn": "xpath", "_args": ["//a[@class='tag']/text()"]}
            ]
        }
    }
}
```

## Parser Presets

Save parsers for reuse across requests.

### Creating a Preset

Use the Oxylabs dashboard or API to save parsing instructions as a preset.

### Using a Preset

```python
payload = {
    "source": "universal",
    "url": "https://example.com/product",
    "parse": True,
    "parser_preset": "my-product-parser"
}
```

### Generating Presets via API

```python
import requests

# Generate parsing instructions from a description
payload = {
    "urls": ["https://example.com/product1", "https://example.com/product2"],
    "prompt": "Extract product title, price, rating, and availability"
}

response = requests.post(
    "https://data.oxylabs.io/v1/parsers/generate-instructions/prompt",
    auth=("USERNAME", "PASSWORD"),
    json=payload
)

instructions = response.json()
```

## Status Codes

| Code | Meaning | Charged |
|------|---------|---------|
| `12000` | Successful parse | Yes |
| `12005` | Parsed with warnings | Yes |
| `12002` | Parse error | No |
| `12006` | Unexpected error | No |
| `12007` | Unexpected error | No |

### Handling Parse Results

```python
result = response.json()

for item in result["results"]:
    content = item["content"]

    if isinstance(content, dict) and "parse_status_code" in content:
        if content["parse_status_code"] == 12000:
            # Successfully parsed
            data = content
        elif content["parse_status_code"] == 12005:
            # Parsed with warnings - check for missing fields
            data = content
        else:
            # Parse error - fall back to raw HTML
            raw_html = item.get("content")
```

## Debugging Tips

1. **Test XPath in browser**: Use browser DevTools (Ctrl+Shift+I → Console) with `$x("//your/xpath")` to test expressions.

2. **Start simple**: Begin with basic XPath, then add transformations.

3. **Check raw HTML**: Request without parsing first to see actual HTML structure.

4. **Use render**: If content loads via JavaScript, add `"render": "html"`.

5. **Handle missing fields**: XPath returns empty string if not found - use fallbacks in your code.
