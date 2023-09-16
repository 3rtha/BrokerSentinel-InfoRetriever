import os
import json
from bs4 import BeautifulSoup

# Folder path containing the All stored - HTML files
folder_path = r'C:\Users\PycharmProjects\WiKiFx\HTML_Folder'

# List all files in the folder
file_names = os.listdir(folder_path)
print(file_names)

data_list = []  # list to store dictionaries

for file_name in file_names:
    if file_name.endswith('.html'):
        file_path = os.path.join(folder_path, file_name)
        
        with open(file_path, 'r', encoding='utf-8') as html_file:
            content = html_file.read()

        soup = BeautifulSoup(content, 'lxml')
        tags = soup.find_all('div', class_='dealer-box')

        for division in tags:
            data_dict = {}  # new dictionary for each division

            # Extract data from various tags and add to the dictionary
            data_dict["Broker_name"] = division.find('h1', class_='text').text
            data_dict["Country"] = division.find('div', class_= 'dealer-label-top').p.text
            data_dict["AgeOfBusiness"] = division.find('span', class_ = 'label-text').text
            data_dict["LicenseStatus"] = division.find('div', class_ = 'dealer-label-list-box').find_all('p', class_='dealer-label-list')[1].text
            dealer_label_list_elements = division.find('div', class_='dealer-label-list-box').find_all('p', class_='dealer-label-list')

            # Check if there are enough elements in the list
            if len(dealer_label_list_elements) >= 4:
               scope_of_business_element = dealer_label_list_elements[2]
               platform_status_element = dealer_label_list_elements[3]
            else:
                 scope_of_business_element = None
                 platform_status_element = None
            # Check if both elements exist
            if scope_of_business_element and platform_status_element:
               scope_of_business_text = scope_of_business_element.text
               platform_status_text = platform_status_element.text
    
            # Check if MT4/5 is in the scope of business text
               if "MT4/5" in scope_of_business_text:
                  data_dict["Scope of Business"] = "N/A"
                  data_dict["PlatformStatus"] = scope_of_business_text
               else:
                  data_dict["Scope of Business"] = scope_of_business_text
        
                 # Check if MT4/5 is in platform status text
                  if "MT4/5" in platform_status_text:
                      data_dict["PlatformStatus"] = platform_status_text
                  else:
                      data_dict["PlatformStatus"] = "N/A"
            else:
               if platform_status_element:
                  scope_of_business_text = scope_of_business_element.text
        
               # Check if MT4/5 is not in the scope of business text
                  if "MT4/5" not in scope_of_business_text:
                      data_dict["Scope of Business"] = scope_of_business_text
                      data_dict["PlatformStatus"] = "N/A"
                  else:
                      data_dict["Scope of Business"] = "N/A"
                      data_dict["PlatformStatus"] = scope_of_business_text
               else:
                 # No elements found
                  data_dict["Scope of Business"] = "N/A"
                  data_dict["PlatformStatus"] = "N/A"

            #Website Link to store
            data_dict["Website_link"] = division.find('span', class_ = 'dealer-label-list-ul-a').text
            
            data_dict["Rating"] = division.find('span', class_ = 'score-star-text').text
            #Extract all the phone number
            contact_numbers = []
            contact_info = division.find('section', class_='dealer-information')
            contact_info2_elements = division.find_all('div', class_='sheet')

            if contact_info:
               Numbers = contact_info.find_all('section', class_='infoitemtop')
               contact_numbers = [number.find('p', class_='val').text for number in Numbers]

            if contact_info2_elements:
               contact_info2 = contact_info2_elements[2].find_all('section', class_='infoitemtop')[0]
               phone_number2 = contact_info2.find('p', class_='val').text
               contact_numbers.append(phone_number2)

            data_dict["ContactNumbers"] = contact_numbers if contact_numbers else ["N/A"]

            # additional information -- Company Name
            company_name1 = division.find('section', class_='dealer-information information')
            company_name2 = division.find('div', class_='content')

            if company_name1:
               Full_name = company_name1.find_all('section', class_='infoitemtop')[0].find('p', class_='val').text
               data_dict["Company_Name"] = Full_name

            if company_name2:
               company_sheets = company_name2.find_all('div', class_='sheet')

               if company_sheets:
                 columns = company_sheets[0].find_all('div', class_='column')

                 if columns:
                    Full_name2 = columns[0].find_all('section', class_='infoitemtop')[0].find('p', class_='val').text
                    data_dict["Company_Name"] = Full_name2

            # Listing all the warnings from the authorities!

            Risk = division.find('section', class_='dealer-risk')

            if Risk:
               risk_list = Risk.find_all('ul', class_='content')

               if len(risk_list) >= 1:
                  first_ul = risk_list[0]
                  first_li_items = first_ul.find_all('li', class_='li')

                  risk_statement = ""

                  for li_item in first_li_items:
                    risk_statement += li_item.text

                  if len(risk_list) >= 2:
                     second_ul = risk_list[1]
                     second_li_items = second_ul.find_all('li', class_='li')

                     for li_item in second_li_items:
                        risk_statement += li_item.text

                  if risk_statement:
                       data_dict["Warning"] = risk_statement
                  else:
                       data_dict["Warning"] = "N/A"

            else:
                 data_dict["Warning"] = "N/A"

            # All License, risk, Regulatory, business, software index ratings
            data_dict["OverallScore"] = division.find('span', class_ = 'score-num-1').text + "/10" 

            Dealer_index = division.find('div', class_='dealer-r')

            if Dealer_index:
               Short_text = Dealer_index.find('div', class_='score-r')

               if Short_text:
                  score_index = Short_text.find_all('tr', class_='score-r-ul')[0].find('td', class_='score-r-ul-2 span').text
                  data_dict["License_Index"] = score_index + "/10"
                  
                  # Business Index
                  business_score = Short_text.find_all('tr', class_='score-r-ul')[1].find('td', class_='score-r-ul-2 span').text 
                  if business_score:
                     data_dict["Business_Index"] = business_score + "/10"
                  else:
                     data_dict["Business_Index"] =  "0.00/10"
                  
                  # Risk Mangement Index

                  Risk_mangement_score = Short_text.find_all('tr', class_='score-r-ul')[2].find('td', class_='score-r-ul-2 span').text 

                  if Risk_mangement_score:
                     data_dict["Risk_Management_Index"] = Risk_mangement_score + "/10"
                  else:
                     data_dict["Risk_Management_Index"] = "0.00/10"
                  
                  # Software Index

                  software_score = Short_text.find_all('tr', class_='score-r-ul')[3].find('td', class_='score-r-ul-2 span').text

                  if software_score:
                     data_dict["Software_Index"] = software_score + "/10"
                  else:
                     data_dict["Software_Index"] = "0.00/10"
                     
                  # Regulatory Index

                  Regulatory_score =  Short_text.find_all('tr', class_='score-r-ul')[4].find('td', class_='score-r-ul-2 span').text 

                  if Regulatory_score:
                     data_dict["Regulatory_Index"] = Regulatory_score + "/10"
                  else:
                     data_dict["Regulatory_Index"] =  "0.00/10"

            else:
               data_dict["License_Index"] = "0.00/10"

            # Email Addresses
            
            Email_address = []
            Email_info = division.find('section', class_='dealer-information othercontact')
            if Email_info:
              Email_more = Email_info.find_all('li', class_='valline')
              for Emails in Email_more:
                Email_address.append((Emails).text)
            else:
                try:
                      Email_info2_elements = division.find('div', class_='content')
                      Email_info2 = Email_info2_elements.find('div', class_='item').find_all('li', class_='valline')
                      for Emails in Email_info2:
                          Email_address.append((Emails).text)
                except AttributeError:
                  pass

            if Email_address:
               data_dict["Email_address"] = ','.join(Email_address)
            else:
               data_dict["Email_address"] = "N/A"
            
            
            

        data_list.append(data_dict)  # Add the dictionary to the list

# Save the list of dictionaries as a JSON file
output_file = 'extracted_data.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, indent=4)

print(f"Extracted data saved to {output_file}")
