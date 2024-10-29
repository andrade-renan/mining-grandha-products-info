# Grandha Product Scraper

> _Note:_ This README was generated with ChatGPT

This project is a scraper to collect information and images of products listed on the Grandha website. The script accesses product pages, extracts detailed data and images, and organizes this information into a CSV file and image subfolders.

## Features

- **Data Extraction**: Collects detailed information on each product, including name, reference, line, price, description, barcode, usage instructions, composition, and product link.
- **Image Extraction**: Downloads all product images and stores them in subfolders organized by the product name.
- **Data Structure**: The data is saved in a CSV file in the `data/` directory, while images are stored in subfolders within `data/images`.

## Requirements

- Python 3.10+
- Required libraries:
  - `requests`
  - `pandas`
  - `beautifulsoup4`
  - `lxml`

### Install Dependencies

Install dependencies by running:

```bash
pip install -r requirements.txt
```

> **Note**: Create a `requirements.txt` file with the following content:
>
> ```
> requests
> pandas
> beautifulsoup4
> lxml
> ```

## Project Structure

```plaintext
grandha_product_scraper/
├── data/
│   ├── images/
│   │   └── Product_Name/
│   └── Produtos_da_Grandha.csv
├── grandha_combined_scraper.py
└── README.md
```

> _Note:_ There are other files, but they were used for study and prototype.

## Usage

1. Place the `grandha_combined_scraper.py` script in your local environment.
2. In the terminal, run the script:

   ```bash
   python grandha_combined_scraper.py
   ```

3. The script will:

   - Go through all specified product pages.
   - Extract data for each product and save it in the `data/Produtos_da_Grandha.csv` file.
   - Create a subfolder for each product in `data/images/` where it will save the respective images.

4. Check the CSV file and downloaded images in the `data/` directory.

## Notes

- Ensure a stable internet connection, as the script relies on HTTP requests to access data.
- Script execution may take some time, depending on the number of products and your internet speed.
