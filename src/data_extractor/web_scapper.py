import requests
from bs4 import BeautifulSoup
import re

url1 = "https://www.seek.com.au/"
url2 = "https://www.seek.com.au/job/"


class web_scrap:
    def __init__(self, url_page=url1, url_job=url2, job_title="", prev_url="", next_url="", curr_pagenum=1, prev_pagenum=1, next_pagenum=1) -> None:
        self.url_page = url_page
        self.url_job = url_job
        self.job_title = job_title
        self.prev_url = prev_url
        self.next_url = next_url
        self.curr_pagenum = curr_pagenum
        self.prev_pagenum = prev_pagenum
        self.next_pagenum = next_pagenum

    
    def extract_page_limit(self) -> str:
        self.url_page = self.url_page + self.job_title.replace(" ","-") + "-jobs?page=" + str(self.curr_pagenum)

        response = requests.get(self.url_page)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # gather page number range
            divs = soup.find_all('nav', class_='_1wkzzau0 _1wkzzau1')
            page_num_range = divs[2].get_text()

            page_num_range = str(page_num_range)
            page_num_range = re.search(r"\d+", page_num_range).group(0)
            # re.findall(r'\d+', str(page_num_range))




        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code}")
            
        return page_num_range
