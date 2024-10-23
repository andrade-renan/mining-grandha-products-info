# Grandha Products Scraper

> _Note:_ This README was generated with ChatGPT

## Overview

This Python script is designed to scrape product information from Grandha's online store. It navigates through multiple pages, extracting details such as product reference, name, line, price, general description, barcode, usage mode, composition, and the product link.

## Features

- **Automated Pagination Handling:** The script iterates through 12 pages of the product listing.
- **Data Extraction:** Retrieves comprehensive details for each product listed on the website.
- **Resilience:** Includes error handling for network requests and gracefully handles missing data.
- **Data Storage:** Collects all the data into a CSV file for easy analysis and storage.

## Prerequisites

To run this script, you need Python installed on your system along with the following Python libraries:

- `requests` for making HTTP requests.
- `BeautifulSoup` from `bs4` for parsing HTML content.
- `lxml` for XPath selections and parsing.
- `pandas` for organizing the data into a structured format and saving it to CSV.

## Installation

First, ensure you have Python installed. Then, install the required Python libraries using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. **Set Up the URL**: Modify the `base_url` variable if needed to point to the correct section of the Grandha store.
2. **Run the Script**: Execute the script by running:

```bash
python grandha_scraper.py
```

3. **Check Output**: After execution, the script will save the product data to a CSV file named `Produtos da Grandha.csv` in the 'data' directory.

## CSV File Format

The output CSV file will contain the following columns:

- `REF`: Product reference ID.
- `Nome do Produto`: Name of the product.
- `Linha`: Product line.
- `Valor`: Price of the product.
- `Descrição Geral`: General description of the product.
- `Código de Barras`: Barcode of the product.
- `Modo de Uso`: How to use the product.
- `Composição`: Product composition.
- `Link do Produto`: URL link to the product page.

## Error Handling

The script includes basic error handling for HTTP request failures and will output errors to the console.

## License

This project is open-source and available under the MIT License.

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request with your features or fixes.
