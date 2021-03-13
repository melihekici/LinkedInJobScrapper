from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import selenium
from selenium.webdriver.chrome.options import Options
from time import sleep
import urllib
import requests
from bs4 import BeautifulSoup

class LinkedInScrapper:

    def __init__(self, searchTerm, jobLocation):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.searchTerm = searchTerm
        self.jobLocation = jobLocation
    
    def __seeAllJobs(self):
        url = "https://www.linkedin.com/jobs/search?keywords={}&location={}".format('%20'.join(self.searchTerm.split(' ')), self.jobLocation)
        self.driver.get(url)
        sleep(3)
        
        scroll_pause_time = 1 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = self.driver.execute_script("return window.screen.height;")   # get the screen height of the web
        i=1

        while True:
            # scroll one screen height each time
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            sleep(scroll_pause_time)
            try:
                more_button = self.driver.find_element_by_xpath("(//button[contains(@data-tracking-control-name,'show-more')])[1]")
                more_button.click()
                sleep(scroll_pause_time)
            except:
                pass

            i += 1
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break
    
    def __findJobUrls(self):
        response = self.driver.page_source
        self.driver.close()
        jobs_list = response.split(r"https://tr.linkedin.com/jobs/view/")
        jobs_list = jobs_list[1::]
        job_urls = []
        count = 0
        for job in jobs_list:
            job_urls.append(r"https://tr.linkedin.com/jobs/view/"+job.split(';')[0])
            count+=1

        return job_urls

    def __readJobUrl(self, job_url):
        response = requests.get(job_url).content
        soup = BeautifulSoup(response, features="html.parser")
        return soup

    def __modifyText(self, soup):
        new_text = soup.find_all(text=True)
        try:
            new_text = new_text[new_text.index('Bu iş ilanını rapor et')+1::]
            new_text = new_text[:new_text.index('Daha fazla göster')]
        except:
            pass
        new_text = ' '.join(new_text).lower()
        new_text = new_text.replace('\xa0', ' ')
        new_text = new_text.replace('"', ' ')
        new_text = new_text.replace(" or ", " ")
        new_text = new_text.replace(".", " ")
        new_text = new_text.replace(",", " ")
        return new_text

    def __addToDict(self, new_text, dictionary):
        for key in dictionary.keys():
            for key2 in dictionary[key][0]:
                if(key2 in new_text):
                    dictionary[key][1] += 1
                    break

    def scrapSkills(self, dictionary, counter_label):
        self.__seeAllJobs()
        self.job_urls = self.__findJobUrls()
        
        count=0
        for url in self.job_urls:
            counter_label.configure(text="{}/{}".format(count+1,len(self.job_urls)))
            text = self.__readJobUrl(url)
            new_text = self.__modifyText(text)
            self.__addToDict(new_text, dictionary)
            count +=1
        
        return dictionary, len(self.job_urls)
        


    
