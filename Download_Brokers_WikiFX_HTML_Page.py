from ctypes.wintypes import SERVICE_STATUS_HANDLE
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException
import time
import os
import subprocess
from bs4 import BeautifulSoup
import requests
import unicodedata
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# The chrome driver located
PATH = "C:/Users/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"

# Directory to store all the HTML files
OUTPUT_DIRECTORY = "C:\\Users\\PycharmProjects\\WiKiFx\\HTML_Folder_MT5"

chrome_options = Options()

# Set the path to the Chrome binary (you need to replace this with the correct path)
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_service = Service(PATH)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Opening the list of Brokers domains file
with open(r"C:\\Users\\PycharmProjects\\WiKiFx\\domains.txt", "r") as domain_file:
    domains_with_www = [line.strip() for line in domain_file]

# Remove the "www." prefix from each domain
domains = [domain.replace("www.", "") for domain in domains_with_www]

# Lists to store domain names where the class name was found and not found
## Lists to store domain names where the class name was found and not found
domains_found = []
domains_not_found = []

for domain in domains:
    # Case 1: Search with TLD
    search_url_with_tld = f"https://www.wikifx.com/en/search.html?keyword={domain}&SearchPosition=1"
    search_url_without_tld = f"https://www.wikifx.com/en/search.html?keyword={domain.split('.')[0]}&SearchPosition=1"

    # Check with TLD
    driver.get(search_url_with_tld)
    time.sleep(5)

    try:
        # Wait for the element to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "summary_desc_JAzKE")))
        elements = driver.find_elements(By.CLASS_NAME, "summary_desc_JAzKE")

        if elements:
            for element in elements:
                element_text = element.text
                print("Element Text:", element_text)

                if domain in element_text:
                    print(f"Found '{domain}' in the element text (With TLD)")

                    # Scroll the element into view
                    driver.execute_script("arguments[0].scrollIntoView();", element)

                    # Click on the element using JavaScript
                    driver.execute_script("arguments[0].click();", element)

                    time.sleep(13)

                    # Get the current window handle (main tab)
                    main_window_handle = driver.current_window_handle

                    # Switch to the new tab
                    new_window_handle = driver.window_handles[-1]
                    driver.switch_to.window(new_window_handle)
                    page_url = driver.current_url
                    response = requests.get(page_url)
                    if response.status_code == 200:
                        page_content = response.text
                        file_name = os.path.join(OUTPUT_DIRECTORY, f"{domain}.html")
                        with open(file_name, "w", encoding="utf-8") as file:
                            file.write(page_content)
                        print(f"Downloaded HTML content saved to {file_name}")
                        domains_found.append(domain)
                        with open("domains_found.txt", "w") as found_file:
                            for domain in domains_found:
                                found_file.write(domain + "\n")

                    else:
                        print(f"Failed to download the page. Status code: {response.status_code}")

                    driver.close()

                    # Switch back to the main tab
                    driver.switch_to.window(driver.window_handles[0])
                    main_window_handle = driver.current_window_handle

                    break  # No need to continue checking other elements if a match is found

            else:
                print(f"'{domain}' not found in any matching elements (With TLD)")

                # Check without TLD
                driver.get(search_url_without_tld)
                time.sleep(5)

                try:
                    # Wait for the element to be clickable
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "summary_desc_JAzKE")))
                    elements = driver.find_elements(By.CLASS_NAME, "summary_desc_JAzKE")

                    for element in elements:
                        element_text = element.text
                        print("Element Text (Without TLD):", element_text)
                        # checking if the domain is present in the element text
                        if domain in element_text:
                            print(f"Found '{domain}' in the element text (Without TLD)")

                            # Scroll the element into view
                            driver.execute_script("arguments[0].scrollIntoView();", element)

                            # Click on the element using JavaScript
                            driver.execute_script("arguments[0].click();", element)

                            time.sleep(13)

                            # Get the current window handle (main tab)
                            main_window_handle = driver.current_window_handle

                            # Switch to the new tab
                            new_window_handle = driver.window_handles[-1]
                            driver.switch_to.window(new_window_handle)
                            page_url = driver.current_url
                            response = requests.get(page_url)
                            if response.status_code == 200:
                                page_content = response.text
                                file_name = os.path.join(OUTPUT_DIRECTORY, f"{domain}.html")
                                with open(file_name, "w", encoding="utf-8") as file:
                                    file.write(page_content)
                                print(f"Downloaded HTML content saved to {file_name}")
                                domains_found.append(domain)
                                with open("domains_found.txt", "w") as found_file:
                                    for domain in domains_found:
                                        found_file.write(domain + "\n")
                            else:
                                print(f"Failed to download the page. Status code: {response.status_code}")
                                domains_not_found.append(domain)
                                with open("domains_not_found.txt", "w") as not_found_file:
                                    for domain in domains_not_found:
                                        not_found_file.write(domain + "\n")

                            driver.close()

                            # Switch back to the main tab
                            driver.switch_to.window(driver.window_handles[0])
                            main_window_handle = driver.current_window_handle

                            break  # No need to continue checking other elements if a match is found

                    else:
                        print(f"'{domain}' not found in any matching elements (Without TLD)")
                        domains_not_found.append(domain)
                        with open("domains_not_found.txt", "w") as not_found_file:
                            for domain in domains_not_found:
                                not_found_file.write(domain + "\n")

                except (TimeoutException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException) as e:
                    print(f"An exception occurred for {domain} (Without TLD): {e}")
                    domains_not_found.append(domain)
                    with open("domains_not_found.txt", "w") as not_found_file:
                        for domain in domains_not_found:
                            not_found_file.write(domain + "\n")

                except Exception as e:
                    print(f"An unexpected error occurred for {domain} (Without TLD): {e}")
                    with open("domains_not_found.txt", "w") as not_found_file:
                        for domain in domains_not_found:
                           not_found_file.write(domain + "\n")
        else:
            with open("domains_not_found.txt", "w") as not_found_file:
              for domain in domains_not_found:
               not_found_file.write(domain + "\n")


    except InvalidSessionIdException as session_exception:
        print(f"Invalid session ID exception occurred: {session_exception}")
        # Close the current WebDriver session and create a new one
        driver.quit()
        time.sleep(2)  # Wait for a couple of seconds before opening a new browser
        chrome_service = Service(PATH)
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        continue  # Move on to the next domain


    except Exception as e:
        print(f"An unexpected error occurred for {domain} (With TLD): {e}")
        with open("domains_not_found.txt", "w") as not_found_file:
            for domain in domains_not_found:
                not_found_file.write(domain + "\n")

# Close the browser window
driver.quit()
