import requests
from bs4 import BeautifulSoup

db = {}


def scrapping(term):
  
  count = 0
  temp = []

  request = requests.get(f"https://stackoverflow.com/jobs?r=true&q={term}")
  soup = BeautifulSoup(request.text, "html.parser")
  div = soup.find_all("div", {"class":"grid"})
  for d in div:
    count+=1
    title = d.find("h2", {"class" : "mb4 fc-black-800 fs-body3"})
    link = d.find("a", {"class" : "s-link stretched-link"})
    name = d.find("h3", {"class" : "fc-black-700 fs-body1 mb4"})
    if title and link and name:
      dic = {
        "title" : title.text[1:],
        "link" : f"https://stackoverflow.com{link.attrs['href']}",
        "name" : name.text[1:name.text.index("\r")]
      }
      temp.append(dic)
  
  request = requests.get(f"https://weworkremotely.com/remote-jobs/search?term={term}")
  soup = BeautifulSoup(request.text, "html.parser")
  div = soup.find_all("li", {"class":"feature"})
  for d in div:
    count+=1
    title = d.find("span", {"class" : "title"})
    link = d.find_all("a")
    try:
      link = link[1]
    except:
      link = link[0]
    name = d.find("span", {"class" : "company"})
    if title and link and name:
      dic = {
        "title" : title.text,
        "link" : f"https://weworkremotely.com{link.attrs['href']}",
        "name" : name.text
      }
      temp.append(dic)
  
  request = requests.get(f"https://remoteok.io/remote-dev+{term}-jobs")
  soup = BeautifulSoup(request.text, "html.parser")
  td = soup.find_all("td", {"class":"company position company_and_position"})
  for t in td:
    count+=1
    title = t.find("h2")
    link = t.find("a", {"class" : "preventLink"})
    name = t.find("h3")
    if title and link and name:
      dic = {
        "title" : title.text,
        "link" : f"https://remoteok.io{link.attrs['href']}",
        "name" : name.text
      }
      temp.append(dic)
  
  db[term] = temp  
  return db, count
