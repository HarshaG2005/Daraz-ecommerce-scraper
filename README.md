# Daraz-ecommerce-scraper
# 🛒 Daraz Laptop Price Scraper

A robust Python web scraper that automatically collects laptop listings from Daraz.lk, extracts pricing data, and exports results to CSV format. Built with Selenium for reliable data extraction across paginated results.

## 🚀 Features

- **Smart Pagination**: Automatically navigates through all product pages
- **Comprehensive Data Extraction**: Captures title, current price, original price, discounts, seller ratings, and seller information
- **Brand Intelligence**: Automatically identifies laptop brands from product titles using keyword matching
- **Robust Error Handling**: Gracefully handles missing elements and network issues
- **Anti-Detection**: Includes warmup periods and intelligent wait strategies
- **Export Ready**: Saves data to CSV with UTF-8 encoding for easy analysis

## 📊 Data Collected

| Field | Description |
|-------|-------------|
| `title` | Complete product title |
| `current_price` | Current selling price |
| `original_price` | Original price (if discounted) |
| `discount` | Discount percentage |
| `seller_rating` | Seller rating and review count |
| `seller` | Seller name |
| `brand` | Auto-detected brand (HP, Dell, Lenovo, etc.) |

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/daraz-laptop-scraper.git
cd daraz-laptop-scraper

# Install required packages
pip install selenium

# Download ChromeDriver and ensure it's in your PATH
# Or use webdriver-manager for automatic management:
pip install webdriver-manager
```

## 💻 Usage

```python
python scraper.py
```

The scraper will:
1. 🔍 Collect all laptop listing URLs (price > 50,000 LKR, sorted by price)
2. 📄 Extract detailed information from each listing
3. 💾 Save results to `daraz.csv`

## 🎯 Supported Brands

The scraper automatically detects these laptop brands:
- **HP** (Pavilion, Envy, Spectre, EliteBook, ProBook, Omen)
- **Dell** (Inspiron, XPS, Alienware, Vostro, Latitude)
- **Lenovo** (ThinkPad, IdeaPad, Yoga, Legion)
- **Asus** (VivoBook, ZenBook, TUF, ROG)
- **Apple** (MacBook, Mac)
- **MSI, Acer, Razer** and more

## ⚙️ Configuration

Modify the starting URL to change search criteria:

```python
current_url = "https://www.daraz.lk/laptops/?page=1&price=50000-&sort=priceasc"
#                                                    ^^^^^ Min price
#                                                              ^^^^^^^^ Sort order
```

## 📈 Sample Output

```csv
title,current_price,original_price,discount,seller_rating,seller,brand
"HP Pavilion 15-eh1001AU Laptop",Rs. 145000,Rs. 160000,-9%,4.2 (150),TechStore,HP
"Dell Inspiron 15 3000",Rs. 125000,,,4.5 (89),CompuWorld,Dell
```

## 🚦 Rate Limiting & Ethics

- Built-in delays between requests to respect server resources
- Follows robots.txt guidelines
- Only scrapes publicly available product information
- **Note**: Always check website terms of service before scraping

## 🛡️ Error Handling

- **Timeout Protection**: Handles slow-loading pages
- **Missing Elements**: Gracefully handles optional fields
- **Network Issues**: Continues scraping despite connection problems
- **Anti-Bot Measures**: Includes warmup and human-like behavior

## 🔧 Technical Details

- **Framework**: Selenium WebDriver with Chrome
- **Wait Strategy**: Explicit waits with expected conditions
- **Pagination**: Automatic detection of disabled "Next" buttons
- **Data Processing**: Brand inference using keyword matching algorithms

## 📝 Requirements

- Python 3.7+
- Selenium 4.0+
- Chrome/Chromium browser
- ChromeDriver (matching your Chrome version)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for educational and research purposes. Users are responsible for complying with Daraz.lk's terms of service and applicable laws. The author is not responsible for any misuse of this software.

## 📄 License

MIT License - feel free to use this code for your own projects!

---

**Built with ❤️ for data analysis and market research**
