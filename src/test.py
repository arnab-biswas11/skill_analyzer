import requests
from bs4 import BeautifulSoup

url1 = "https://www.seek.com.au/job/73035592"
url2 = "https://www.seek.com.au/data-analyst-jobs?page=25"

# Send a GET request to the URL
response = requests.get(url1)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # div_selector = "span._1wkzzau0.a1msqi4y.a1msqir"

    # # Find the div using the specified selector
    # target_div = soup.select_one(div_selector)

    # # Check if the div is found
    # if target_div:
    #     # Extract and print the text content of the div
    #     extracted_text = target_div.get_text(strip=True)
    #     print(extracted_text)
    # else:
    #     print("The specified div was not found on the page.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

# print(soup.prettify())
# print(target_div.get_text(strip=True))

# divs = soup.find_all('div', class_='_1wkzzau0 a1msqi6u')
# for div in divs:
#     print(div.get_text())    

# divs = soup.find_all('div', class_='_1wkzzau0 a1msqi6q')
# for div in divs:
#     print(div.get_text())    

# divs = soup.find_all('div', class_='_1wkzzau0 _1pehz540')
# for div in divs:
#     print(div.get_text())    



# Send a GET request to the URL
response = requests.get(url2)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

divs = soup.find_all('nav', class_='_1wkzzau0 _1wkzzau1')
for div in divs:
    print(div.get_text())    