**ScrapeNinja** that implements a web scraping service with an attractive GUI. This project lets a user enter a URL, choose a scraping mode (static using requests/BeautifulSoup or dynamic using Selenium), view the scraped results (page title and links), and save the output in either JSON or CSV format.


## ScrapeNinja Overview

**ScrapeNinja** is designed to provide a simple yet functional web scraping tool. Its key features include:

- **Dual Scraping Modes:**  
  - **Static Mode:** Uses the [requests](https://docs.python-requests.org/) library and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to scrape data from a URL.
  - **Dynamic Mode:** Uses [Selenium](https://www.selenium.dev/documentation/) to handle websites that load content dynamically (ensure you have the proper web driver installed).

- **Attractive GUI:**  
  Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/), the interface is modern and user-friendly.

- **Data Output Options:**  
  After scraping, users can view the results in the UI and save them as JSON (containing the page title and all links) or as CSV (with each row representing a link).

This project is aimed at potential clients such as e-commerce companies, market researchers, or real estate agencies that need to extract structured data from various websites.

---

## Installation & Dependencies

Before running the code, make sure you have the following Python libraries installed:

```bash
pip install PyQt5 requests beautifulsoup4
```

For dynamic scraping, install Selenium:

```bash
pip install selenium
```

*Note:*  
If you plan to use dynamic scraping, download and install the appropriate [ChromeDriver](https://sites.google.com/chromium.org/driver/) (or another driver for your preferred browser) and ensure it is in your system’s PATH.

---


## How to Run the Application

1. **Install Dependencies:**  
   Run the installation commands mentioned above.

2. **Save the Code:**  
   Save the provided source code in a file, for example, `scrapeninja.py`.

3. **Run the Script:**  
   Open a terminal, navigate to the directory where `scrapeninja.py` is saved, and execute:
   ```bash
   python app.py
   ```

4. **Use the Application:**  
   - **Enter a URL** to scrape.
   - **Select the scraping mode** (Static or Dynamic).
   - **Choose the desired output format** (JSON or CSV).
   - Click **Scrape** to fetch and display the data.
   - Click **Save Results** to export the data to a file.

---
