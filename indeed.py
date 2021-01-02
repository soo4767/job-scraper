import requests
from bs4 import BeautifulSoup

LIMIT=50
URL=f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_pages():
  resul = requests.get(URL)

  soup = BeautifulSoup(resul.text, 'html.parser')

  pagnation = soup.find("ul",{"class":"pagination-list"})

  links=pagnation.find_all("a")

  pages=[]

  for link in links[0:-1] :
    pages.append(int(link.string))
    

  max_page=pages[-1]

  return max_page
  
def extract_job(html):
  title=html.find("h2",{"class":"title"}).find("a")["title"]
  company=html.find("span",{"class":"company"}).string
  location=html.find("div",{"class":"recJobLoc"})["data-rc-loc"]
  id=html["data-jk"];

  link=f"https://www.indeed.com/viewjob?jk={id}"
  if company is None:
    company=html.find("span",{"class":"company"}).find("a").string
    
  company=company.strip()
  return {'title':title,'company':company,'location':location,'link':link}

def extract_jobs(last_page):
  
  jobs=[]
  for page in range(last_page):
    print(f"Scrapping indeed: page: {page}")
    result=requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, 'html.parser')
    results=soup.find_all("div",{"class":"jobsearch-SerpJobCard"})
    for result in results :
      job=extract_job(result)
      jobs.append(job)
  return jobs


def get_jobs():
  last_pages=extract_pages()
  jobs=extract_jobs(last_pages)
  
  return jobs
