import csv
import requests
from bs4 import BeautifulSoup

reviews = open('dataset.csv', 'a', encoding='utf8')
reviews_writer = csv.writer(reviews, delimiter=',', lineterminator='\n', quoting=csv.QUOTE_NONNUMERIC)

def get_employee_status(job_title):
    if ('(Current Employee)' in job_title):
        return 'Current'
    else:
        return 'Former'

def format_job_title(job_title):
    aux = job_title.replace('–', '')
    aux = aux.replace('   ', '')
    if '(Former Employee)' in aux:
        job_title_formatted = aux.replace('(Former Employee)', '')
        return job_title_formatted
    else:
        job_title_formatted = aux.replace('(Current Employee)', '')
        return job_title_formatted

def generate_dataset(job_title, location, review_date, review_text):
    for i in range(len(job_title)-1):
        employee_status = get_employee_status(job_title[i].text)
        job_title_formatted = format_job_title(job_title[i].text)
        reviews_writer.writerow([job_title_formatted, str(employee_status), location[i].text, review_date[i].text, review_text[i].text, 0])

def get_reviews(url, count_reviews):
    for i in range(0,count_reviews+20,20):
        formatted_url = url + "&start=" + str(i)
        req = requests.get(formatted_url)
        if (req.status_code == 200):
            content = req.content
            soup = BeautifulSoup(content, 'html.parser')
            job_title = soup.findAll("span", class_='cmp-reviewer-job-title')
            location = soup.findAll("span", class_='cmp-reviewer-job-location')
            review_date = soup.findAll("span", class_='cmp-review-date-created')
            review_text = soup.findAll("span", class_='cmp-review-text')
            generate_dataset(job_title, location, review_date, review_text)

with open('indeed_links_scraping.csv') as links_dataset:
    csv_reader = csv.reader(links_dataset, delimiter=',')
    for line in csv_reader:
        get_reviews(line[0], int(line[1]))
            