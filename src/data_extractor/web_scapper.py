import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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

    
    def request_page(self):

        self.url_page = url1 + self.job_title.replace(" ","-") + "-jobs?page=" + str(self.curr_pagenum)

        response = requests.get(self.url_page)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code} for job title {self.job_title} and page {self.curr_pagenum}" )


    def extract_jobs(self):

        result = None
        job_details = {}
        job_details['title'] = self.job_title
        job_details['pagination'] = []
        

        while(result is None):
            soup = self.request_page()

            try:

                search_text = 'No matching search results'
                result = soup.find(text=search_text)

                if result is None:
                    job_details['pagination'].append(self.curr_pagenum) 

                    div_elements  = soup.find_all('div', class_='_1wkzzau0 a1msqi4y a1msqi4w')
                    hrefs = [div.find('a')['href'] for div in div_elements if div.find('a')]

                    for href in hrefs:
                        parsed_url = urlparse(href)
                        job_number = parsed_url.path.split('/')[-1]

                        job_details['job_id_' + str(job_number)] = {'url': url2 + str(job_number), 'pagenum': self.curr_pagenum}

                    self.curr_pagenum += 1 

            except Exception as e:
                print(e)
 
        return job_details

print(web_scrap(job_title="pyspark").extract_jobs())
