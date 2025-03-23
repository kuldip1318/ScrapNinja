import sys
import json
import csv
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt

# Optional: Selenium for dynamic scraping
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
except ImportError:
    webdriver = None

class ScrapeNinja(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScrapeNinja")
        self.initUI()
        self.scraped_data = None

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()

        # URL Input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)
        
        # Scraping Mode Selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Mode:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Static (requests+BeautifulSoup)", "Dynamic (Selenium)"])
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.mode_combo)
        layout.addLayout(mode_layout)
        
        # Output Format Selection
        format_layout = QHBoxLayout()
        format_label = QLabel("Output Format:")
        self.format_combo = QComboBox()
        self.format_combo.addItems(["JSON", "CSV"])
        format_layout.addWidget(format_label)
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        
        # Scrape Button
        self.scrape_button = QPushButton("Scrape")
        self.scrape_button.clicked.connect(self.scrape)
        layout.addWidget(self.scrape_button)
        
        # Text Area to Display Results
        self.result_text = QTextEdit()
        layout.addWidget(self.result_text)
        
        # Save Results Button
        self.save_button = QPushButton("Save Results")
        self.save_button.clicked.connect(self.save_results)
        layout.addWidget(self.save_button)
        
        central_widget.setLayout(layout)
    
    def scrape(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a URL.")
            return
        
        mode = self.mode_combo.currentText()
        try:
            if "Static" in mode:
                data = self.static_scrape(url)
            else:
                data = self.dynamic_scrape(url)
            
            self.scraped_data = data
            display_text = json.dumps(data, indent=4)
            self.result_text.setPlainText(display_text)
        except Exception as e:
            QMessageBox.critical(self, "Scraping Error", f"An error occurred:\n{str(e)}")
    
    def static_scrape(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string if soup.title else "No Title Found"
        links = []
        for a in soup.find_all('a'):
            text = a.get_text(strip=True)
            href = a.get('href')
            if href:
                links.append({"text": text, "href": href})
        
        return {"url": url, "title": title, "links": links}
    
    def dynamic_scrape(self, url):
        if webdriver is None:
            raise Exception("Selenium is not installed. Please install it to use dynamic mode.")
        
        options = ChromeOptions()
        options.add_argument("--headless")
        # Ensure the appropriate webdriver is installed and in your PATH.
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "No Title Found"
        links = []
        for a in soup.find_all('a'):
            text = a.get_text(strip=True)
            href = a.get('href')
            if href:
                links.append({"text": text, "href": href})
        
        return {"url": url, "title": title, "links": links}
    
    def save_results(self):
        if not self.scraped_data:
            QMessageBox.warning(self, "No Data", "No scraped data to save. Please run a scrape first.")
            return
        
        output_format = self.format_combo.currentText()
        options = QFileDialog.Options()
        file_filter = "JSON Files (*.json)" if output_format == "JSON" else "CSV Files (*.csv)"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_filter, options=options)
        if file_path:
            try:
                if output_format == "JSON":
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(self.scraped_data, f, ensure_ascii=False, indent=4)
                else:
                    # Save only the links data as CSV
                    with open(file_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(["Text", "Href"])
                        for link in self.scraped_data.get("links", []):
                            writer.writerow([link.get("text"), link.get("href")])
                QMessageBox.information(self, "Success", f"Results saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Save Error", f"An error occurred while saving:\n{str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScrapeNinja()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
