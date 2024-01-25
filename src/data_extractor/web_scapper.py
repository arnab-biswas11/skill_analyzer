import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

global_url_page = "https://www.seek.com.au/"
global_url_job = "https://www.seek.com.au/job/"


class web_scrap:
    def __init__(self, 
                 url_page=global_url_page, 
                 url_job=global_url_job, 
                 job_title="", 
                 curr_pagenum=1,
                 job_number=1) -> None:
        self.url_page = url_page
        self.url_job = url_job
        self.job_title = job_title
        self.curr_pagenum = curr_pagenum
        self.job_number = job_number
    
    def request_page_by_num(self):

        self.url_page = global_url_page + self.job_title.replace(" ","-") + "-jobs?page=" + str(self.curr_pagenum)
        print(self.url_page)
        

        response = requests.get(self.url_page)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code} for job title {self.job_title} and page {self.curr_pagenum}" )


    def request_page_by_job(self):

        self.url_job = global_url_job + str(self.job_number)
        print(self.url_job)

        response = requests.get(self.url_job)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:

            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup

        else:
            print(f"Failed to retrieve the page. Status code: {response.status_code} for job title {self.job_title} and page {self.curr_pagenum}" )

    def extract_jobs(self):

        result = None
        n_job = 0
        job_details = {}
        job_details['title'] = self.job_title
        job_details['pagination'] = []
        

        while(result is None):
            soup = self.request_page_by_num()

            try:

                search_text = 'No matching search results'
                result = soup.find(text=search_text)

                if result is None:
                    job_details['pagination'].append(self.curr_pagenum) 

                    div_elements  = soup.find_all('div', class_='_1wkzzau0 a1msqi4y a1msqi4w')
                    hrefs = [div.find('a')['href'] for div in div_elements if div.find('a')]
                    num_jobs_page = len(hrefs)

                    for href in hrefs:
                        parsed_url = urlparse(href)
                        self.job_number = parsed_url.path.split('/')[-1]

                        soup = self.request_page_by_job()

                        divs_header = soup.find_all('div', class_='_1wkzzau0 a1msqi6q a1msqi6v')
                        divs_subheader = soup.find_all('div', class_='_1wkzzau0 a1msqi6u')
                        divs_body = soup.find_all('div', class_='_1wkzzau0 _1pehz540')

                        role = divs_header[0].get_text()
                        company = divs_header[1].get_text()
                        desc = divs_body[0].get_text()

                        pay = ""

                        # print(self.job_number)
                        # print(len(divs))

                        try: 
                            pay = divs_subheader[3].get_text()

                        except Exception as e:
                            print(e, 'here is it!!!!!!!!!!!!')

                        job_spec = {
                            'url': self.url_job, 
                            'pagenum': self.curr_pagenum,
                            'header': {
                                'role': role,
                                'company': company,
                                'location': divs_subheader[0].get_text(),
                                'category': divs_subheader[1].get_text(),
                                'work_type': divs_subheader[2].get_text(),
                                'pay': pay if pay!="Your application will include the following questions:" else "",
                                'job_desc': desc}}

                        job_details['job_id_' + str(self.job_number)] = job_spec
                        
                        yield job_spec, num_jobs_page, self.curr_pagenum

                        n_job += 1

                    self.curr_pagenum += 1 

            except Exception as e:
                print(e)
 
# print(web_scrap(job_title="pyspark").extract_jobs())
