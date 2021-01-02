import requests
from bs4 import BeautifulSoup

URL=f"https://stackoverflow.com/jobs?q=python&pg="




def get_last_page():
  result=requests.get(URL)
  soup = BeautifulSoup(result.text,"html.parser")
  pages=soup.find("div",{"class":"s-pagination"}).find_all("a")
  last_page=pages[-2].find("span").string
  return int(last_page)

def extract_job(html):
  title=html.find("div",{"class":"grid--cell fl1"}).find("a")["title"]
  l=html.find("div",{"class":"grid--cell fl1"}).find("a")["href"]
  link=f"https://stackoverflow.com{l}"
  company, location=html.find("div",{"class":"grid--cell fl1"}).find("h3",{"class":"fc-black-700 fs-body1 mb4"}).find_all("span",recursive=False)
  company=company.get_text(strip=True)
  location=location.get_text(strip=True)
  

  return {'title':title,'company':company,'location':location,'link':link}


def extract_jobs(last_page):
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping SO: Page: {page+1}")
    result=requests.get(f"{URL}{page+1}")
    soup = BeautifulSoup(result.text,"html.parser")
    results=soup.find_all("div",{"class":"-job"})
    for result in results:
      job=extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs=extract_jobs(last_page)
  return []