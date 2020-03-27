import urllib3
from bs4 import BeautifulSoup
import requests
import os
import csv
import unicodedata
import pandas as pd

def get_links(tag, suffix):
    url = 'https://medium.com/tag/' + tag
    urls = [url + '/' + s for s in suffix]
    links = []
    for url in urls:
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        articles = soup.findAll('div', {"class": "postArticle-readMore"})
        for i in articles:
            links.append(i.a.get('href'))
    return links

def get_article(links,tag):
    print("Logging.. NUMBER OF ARTICLES :: " , len(links))
    articles = []
    count =0
    for link in links:
        try:
            article = {}
            data = requests.get(link)
            soup = BeautifulSoup(data.content, 'html.parser')
            title = soup.findAll('title')[0]
            title = title.get_text()
            author = soup.findAll('meta', {"name": "author"})[0]
            author = author.get('content')
            article['author'] = unicodedata.normalize('NFKD', author)
            article['link'] = link
            article['title'] = unicodedata.normalize('NFKD', title)
            article['tag'] = tag
            paras = soup.findAll('p')
            text = ''
            nxt_line = '\n'
            for para in paras:
                text += unicodedata.normalize('NFKD',para.get_text()) + nxt_line
            # so that , can be treated as a character.
            article['text'] = '"' + text + '"'
            articles.append(article)
            count= count+1
            print("Logging.. PROCESSED ARTICLE :: " , count)
        except KeyboardInterrupt:
            print('Exiting')
            os._exit(status = 0)
        except:
            print("Something went wrong with " + str(link)) 
            continue
    return articles

def save_articles(articles, csv_file,  is_write = True):
    csv_columns = ['author', 'link', 'title', 'text','tag']
    if is_write:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',')
            writer.writeheader()
            for data in articles:
                writer.writerow(data)
            csvfile.close()
    else:
        with open(csv_file, 'a+') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns,  delimiter=',')
            for data in articles:
                writer.writerow(data)
            csvfile.close()

def main():
    is_write = False
    tags = input('Write tags in space separated format.\n')
    tags = tags.split(',')
    file_name = '../../data/'+'database_2.csv'
    suffixes = ['', 'latest','archive/2000', 'archive/2001', 'archive/2002', 'archive/2003', 'archive/2004', 'archive/2005', 'archive/2006', 'archive/2007', 'archive/2008', 'archive/2009','archive/2010', 'archive/2011', 'archive/2012', 'archive/2013', 'archive/2014', 'archive/2015', 'archive/2016', 'archive/2017', 'archive/2018']
    for tag in tags:
        print("Logging.. PROCCESSING TAG :: "+tag)
        links = get_links(tag, suffixes)
        print("Logging.. RECEIVED LINKS FOR :: "+tag)
        articles = get_article(links,tag)
        save_articles(articles, file_name, is_write)
        is_write = False
        print("Logging.. COMPLETED :: "+tag)
    # To remove duplicates
    print("Logging.. Finished all tags now reading")
    articles = pd.read_csv(file_name, file_name, delimiter=',')
    print("Logging.. Read, now dropping duplicates")
    articles = articles.drop_duplicates()
    print("Logging.. Done , now saving")
    articles.to_csv(file_name, sep=',', index=False)
    
if __name__ == '__main__':
    main()