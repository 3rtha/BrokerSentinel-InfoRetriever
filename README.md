# BrokerSentinel-InfoRetriever

## Overview

BrokerSentinel is a comprehensive web scraping and data analysis tool designed to empower traders and investors in the dynamic forex and cryptocurrency markets. It assists in gathering essential information about forex brokers and crypto traders from across the internet, helping users make informed decisions, reduce risks, and promote transparency.

## Features

- **Broker Database:** Compile a curated list of brokers from the MetaTrader platform and online sources.
- **Web Scraping:** Fetch HTML content from WikiFX broker profiles using their domain names and download the HTML pages locally.
- **Data Extraction:** Extract and structure essential data fields from the downloaded HTML Page content.
- **JSON Storage:** Store the organized data in JSON format for further analysis.

## Why BrokerSentinel?

The forex and cryptocurrency markets are complex and ever-changing. BrokerSentinel serves as your guardian in this landscape, ensuring broker credibility, reducing risks, and providing transparent insights into trading firms.

## Usage

1. Clone this repository to your local machine.

```bash
git clone https://github.com/3rtha/BrokerSentinel.git
```
2. Utilize the Python script to download the HTML pages of brokers by employing their domain names.
  ```
 Download_Brokers_WikiFX_HTML_Page.py
```
3. From the downloaded HTML Pages of the brokers - extract the data fields such as Broker_name, Email, Country, AgeofBusiness, LicenseStatus, Scope of business, Platform Status, Website_link, Rating, Contact_Number, Company Name, Warning, OverallScore, License Index, Business_index, Risk_Manegement_Index, Software_index, Regulatory_index, Email_address
 ```
HTML_Data_Extractor.py
 ```
4. Sample Data Looks Like :
   ```
   {
        "Broker_name": "CryptoRocket  ",
        "Country": " Saint Vincent and the Grenadines",
        "AgeOfBusiness": "2-5 years",
        "LicenseStatus": "Suspicious Regulatory License",
        "Scope of Business": "N/A",
        "PlatformStatus": "MT4/5 White Label",
        "Website_link": "https://www.cryptorocket.com/",
        "Rating": "Danger",
        "ContactNumbers": [
            "N/A"
        ],
        "Company_Name": "CryptoRocket Limited",
        "Warning": "It has been verified that this broker currently has no valid regulation. Please be aware of the risk!",
        "OverallScore": "1.48",
        "License_Index": "0.00",
        "Business_Index": "6.77",
        "Risk_Management_Index": "0.00",
        "Software_Index": "4.00",
        "Regulatory_Index": "0.00",
        "Email_address": "N/A"
    },
   ```
5. Analyzing Broker Distribution by Country and Its Relationship with Ratings
   ```
   Countrywise_Rating_Stats.py
   ```
## Contributing
We welcome contributions from the community. If you have ideas for improvement or find any issues, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
WikiFX for providing valuable broker information.
Our open-source community for their support and contributions.

