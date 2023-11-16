import requests
from bs4 import BeautifulSoup
import json


def get_url(base_url):
    urls = {"pages":[],"authors_pages":set()}
    link_url = base_url
    while True:
        response = requests.get(link_url)
        soup = BeautifulSoup(response.text, "html.parser")
        content_author = soup.select("div.col-md-8 div.quote span a")
        for elem in  content_author:
            author_link = base_url +elem["href"]
            urls["authors_pages"].add(author_link)

        content_page = soup.select("nav ul.pager li.next a")
        if content_page:
            next_page_link = content_page[0]
            link_url = base_url + next_page_link['href']
            urls["pages"].append(link_url)
        else:
            break
    return urls

def spider(urls):
    quotes = []
    authors = []
    for page in urls["pages"]:
        response = requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.select("div.col-md-8 div.quote")
        for elem in content:
            result = {}
            author = elem.select("small.author")
            if author:
                result["author"] = author[0].text
            else:
                result["author"] = "Unknown"

            quote = elem.select("span.text")
            if quote:
                result["quote"] = quote[0].text

            tags = elem.select("div.tags a.tag")
            result["tags"] = [tag.text for tag in tags]
            quotes.append(result)
    for author in urls["authors_pages"]:
        result = {}
        response = requests.get(author)
        soup = BeautifulSoup(response.text, 'html.parser')
        result["fullname"] = soup.select("div.author-details h3.author-title")[0].text
        result["born_date"]= soup.select("div.author-details span.author-born-date")[0].text
        result["born_location"]=soup.select("div.author-details span.author-born-location")[0].text
        result["description"]=soup.select("div.author-details div.author-description")[0].text
        authors.append(result)
    return quotes,authors


urls = get_url("http://quotes.toscrape.com/")
quouts,authors = spider(urls)
with open("quotes.json", "w",encoding="utf-8") as json_file:
    json.dump(quouts, json_file, indent=4,ensure_ascii=False)
with open("authors.json", "w",encoding="utf-8") as json_file:
    json.dump(authors, json_file, indent=4,ensure_ascii=False)