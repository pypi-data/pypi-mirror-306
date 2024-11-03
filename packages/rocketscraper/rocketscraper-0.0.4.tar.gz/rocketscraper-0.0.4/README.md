# Rocket Scraper API Python SDK

[![](https://img.shields.io/pypi/v/rocketscraper)](https://pypi.org/project/rocketscraper)

Python SDK for the [Rocket Scraper API](https://rocketscraper.com). For more information, visit the [GitHub repository](https://github.com/rocketscraper/rocketscraper-sdk-python).

## Requirements

- [Python](https://www.python.org/) version 3.7 or above

## Installation

```bash
pip install rocketscraper
```

## Usage

To use the SDK, you need to create a new instance of the `RocketClient` class and pass your API key as an argument.

### Setup

```python
from rocketscraper import RocketClient

rocket_client = RocketClient('YOUR_API_KEY')  # Simplified constructor
```

### Scrape

The `scrape` method allows you to scrape data from a website using a schema. The method returns the scraped data in the format specified in the schema.

```python
from rocketscraper import RocketClient

try:
    client = RocketClient('YOUR_API_KEY')
    
    # Define a comprehensive product schema
    schema = {
        "productDetails": {
            "name": "string",
            "brand": "string",
            "currentPrice": "number",
            "originalPrice": "number",
            "discount": "number",
            "availability": "boolean",
            "rating": "number",
            "reviewCount": "integer"
        },
        "specifications": [{
            "name": "string",
            "value": "string"
        }],
        "shipping": {
            "freeShipping": "boolean",
            "estimatedDays": "integer"
        }
    }
    
    # Add a detailed task description for better accuracy (optional)
    task_description = """
    Extract product information with the following guidelines:
    1. For prices, use the main displayed price (ignore bulk discounts)
    2. Calculate discount percentage from original and current price
    3. Include all technical specifications found on the page
    4. Extract shipping details from both product and shipping sections
    """
    
    result = client.scrape(
        url='https://marketplace.example.com/products/wireless-earbuds',
        schema=schema,
        task_description=task_description
    )
    print(result)

except Exception as e:
    print(f"Error: {e}")
```

#### Example Output

```python
{
    "productDetails": {
        "name": "Premium Wireless Earbuds Pro X",
        "brand": "AudioTech",
        "currentPrice": 149.99,
        "originalPrice": 199.99,
        "discount": 25.0,
        "availability": true,
        "rating": 4.5,
        "reviewCount": 328
    },
    "specifications": [
        {
            "name": "Battery Life",
            "value": "Up to 8 hours (single charge)"
        },
        {
            "name": "Connectivity",
            "value": "Bluetooth 5.2"
        },
        {
            "name": "Water Resistance",
            "value": "IPX4"
        }
    ],
    "shipping": {
        "freeShipping": true,
        "estimatedDays": 3
    }
}
```

### Error Handling

The SDK will raise exceptions for various error cases. It's recommended to wrap your API calls in try-catch blocks to handle potential errors gracefully.

Common error scenarios:
- Invalid API key
- Invalid URL
- Invalid schema format

## Documentation

For more information on how to use the Rocket Scraper API, visit the [Rocket Scraper API documentation](https://docs.rocketscraper.com).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/rocketscraper/rocketscraper-sdk-python/blob/main/LICENSE) file for more details.
