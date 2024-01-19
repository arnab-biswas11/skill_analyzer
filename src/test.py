import requests
from bs4 import BeautifulSoup

url1 = "https://www.seek.com.au/job/73035592"
url2 = "https://www.seek.com.au/pyspark-jobs?page=1"

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


# job_ids = [element.get('data-job-id') for element in elements]
# for job_id in job_ids:
#     print(f'Job ID: {job_id}')

# divs = soup.find_all('div', class_='_1wkzzau0 szurmz0 szurmz7')                
# divs = soup.find_all('nav', class_='_1wkzzau0 _1wkzzau1')
# page_num_range = divs[2].get_text()
# print(page_num_range)
# page_num_range = str(page_num_range)
# page_num_range = re.search(r"\d+", page_num_range).group(0)
# for div in divs:
#     print(div.get_text())