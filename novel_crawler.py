import argparse
import os
import requests
from bs4 import BeautifulSoup
import html2text
import random
import json
from datetime import datetime
import re
from upload_picture import PictureUploader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

html_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>
<body>
{article}
</body>
</html>
"""
date_published = ""
class MarkdownHeader:
    def __init__(self, title, date, authors, tags, summary):
        self.title = title
        self.date = date
        self.authors = authors  # authors现在是一个包含多个属性的结构体
        self.tags = tags
        self.summary = summary
        

    def to_markdown(self):
        tags_formatted = ', '.join([f'"{tag}"' for tag in self.tags])
        # 格式化authors信息，假设authors是一个字典
        authors_formatted = f'name: "{self.authors.get("name")}"\n' \
                            f'  title: "{self.authors.get("title")}"\n' \
                            f'  url: "{self.authors.get("url")}"\n' \
                            f'  image_url: "{self.authors.get("image_url")}"'
        return f"""---
title: "{self.title}"
publishdate: {self.date}
authors: 
  {authors_formatted}
tags: [{tags_formatted}]
summary: >-
  {self.summary}
---
 """

class MarkdownFooter:
    def __init__(self, authors, docUrl):
        self.authors = authors
        self.docUrl = docUrl

    def to_markdown(self):
        return f"""
:::tip 版权说明
本文由程序自动从互联网获取，如有侵权请联系删除，版权属于原作者。

作者：{self.authors}

链接：{self.docUrl}
::: 
"""
        


USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"
]


class NovelCrawler():
    def __init__(self, url, output_folder, config_path='./novel_config.json'):
        self.url = url
        self.output_folder = output_folder
        self.config = self.load_config(config_path, url)
        self.headers = {
            'user-agent': random.choice(USER_AGENT_LIST)
        }
        self.html_str = html_str
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"{output_folder} does not exist, automatically create...")

    def load_config(self, config_path, url):
        with open(config_path, 'r') as file:
            config = json.load(file)
        # Extract the domain name from the URL to match with the config
        domain = url.split('/')[2].split('.')[-2]
        print("domain: "  + domain)
        if domain in config:
            return config[domain]
        else:
            raise ValueError(f"No configuration found for {domain}")

### TODO：空值处理

    def fetch_novel_info(self, soup):
        author_info = {}
        book_info_title = self.config.get('book_info_title', {})
        
        
        # 获取作者名称
        name_selector = selectors.get('name')
        print("name_selector: " + name_selector)
        if name_selector:
            name_tag = soup.select_one(name_selector)
            print( name_tag)
            if name_tag:
                author_info['name'] = name_tag.text.strip() if name_tag.name != 'meta' else name_tag['content']
                
        # 获取作者职称
        title_selector = selectors.get('title')
        print("title_selector: " + title_selector)
        if title_selector:
            title_tag = soup.select_one(title_selector)
            
            if title_tag and title_tag.text.strip() != "":
                author_info['title'] = title_tag.text.strip() if title_tag.name != 'meta' else title_tag['content']
            else:
                author_info['title'] = "此处留白"
        
        # 获取作者个人页面的URL
        url_selector = selectors.get('url')
        if url_selector:
            url_tag = soup.select_one(url_selector)
            if url_tag:
                author_info['url'] = url_tag['content'] if url_tag.name == 'meta' else url_tag['href']
                if author_info['url'].startswith('/'):
                    author_info['url'] = self.url.split("/")[0] + "//" + self.url.split("/")[2] + author_info['url']
                    #print("author_info['url']:" + author_info['url'])
            
        # 获取作者头像的URL
       
        image_url_selector = selectors.get('image_url')
        print("Image URL Selector:", image_url_selector)
        if image_url_selector:
            image_url_tag = soup.select_one(image_url_selector)
            #print("Image URL Tag:", image_url_tag)
            
            author_info['image_url'] = image_url_tag['content'] if image_url_tag.name == 'meta' else image_url_tag['src']
            print( author_info['image_url'] )
            #if image_url_tag and image_url_tag.has_attr('src'):
            #    author_info['image_url'] = image_url_tag['src']
            #else:
            #    print("No 'src' attribute found in the selected tag.")
              
            
        
        return author_info
    
    ###: 代码块处理
        # 1. 获取代码块
        # 2. 获取代码块的语言
        # 3. 格式化代码块
        # 4. 替换原来的代码块
        #TODO: 识别数学公式并放入$$()$$中

        image_tags = soup.find_all('img')
        
        uploader = PictureUploader(config_path='uploader_config.ini')
        for img in image_tags:
            
            src = img.get('src') if img.get('src') else img.get('data-original-src')
            
            if  src.startswith("//"):
              src = "https:" + src 
            #print(src)
            src = uploader.upload_picture(pic_url=src.split("#")[0]) if (src.startswith("http")) else src
            alt = img.get('alt', '')
            markdown_image = f"![{alt}]({src})\n\n"
            img.replace_with(BeautifulSoup(markdown_image, 'html.parser'))

    def send_request_d(self, url):
        # 设置Selenium使用的浏览器和对应的WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        # 打开目标网页
        driver.get(url)
        # 等待页面加载完成，这里简单使用time.sleep，实际项目中可能需要更复杂的等待条件
        time.sleep(5)  # 根据实际页面加载时间调整等待时间
        # 获取页面的源代码
        html = driver.page_source
        # 关闭浏览器
        driver.quit()
        return html
    def send_request(self, url):
        response = requests.get(url=url, headers=self.headers)
        response.encoding = "utf-8"
        if response.status_code == 200:
            html = response.text
            return html
        else:
            print("Failed to send request:", response.status_code)
            return None
    def fetch_chapter_content(self, url):
        html = self.send_request_d(url)
        soup = BeautifulSoup(html, 'lxml')
        title_tag = self.config.get('titleTag', {})
        content_tag = self.config.get('contentTag', {})
        title = soup.find(title_tag)
        print(title)
        text  = soup.find(content_tag)
        print(text)
    def fetch_novel_content(self, html):
        # 使用BeautifulSoup解析Selenium获取的页面源代码
        soup = BeautifulSoup(html, 'lxml')
        
        novel_info = self.fetch_novel_info(soup)
        print(novel_info)
        chapter_url_list = soup.find_all(self.config.get('linkListTag', {}))
        for chapter_url in chapter_url_list:
            self.fetch_chapter_content(chapter_url)

        article_selector = self.config.get('article_selector', {})
       
        content = soup.find(article_selector.get("item"), class_=article_selector.get("class"))
       
        html = self.html_str.format(article=content.prettify())
        
        self.write_content(html, title,  date_published)

    def write_content(self, content, name,  date_published):
        if not os.path.exists(self.output_folder + '/HTML'):
            os.makedirs(self.output_folder + '/HTML')
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder )
        
        html_path = os.path.join(self.output_folder, "HTML", name + ".html")
        
        name= date_published+"-" + name 
    
        md_path = os.path.join(self.output_folder, name + ".md")
        
        #print("md_path: " + md_path)

        with open(html_path, 'w', encoding="utf-8") as f:
            f.write(content)
            print(f"create {name}.html in {self.output_folder} successfully")

        html_text = open(html_path, 'r', encoding='utf-8').read()
        markdown_text = html2text.html2text(html_text, bodywidth=0)
        markdown_text = markdown_header + markdown_text + markdown_footer
        #print(markdown_text)
        with open(md_path, 'w', encoding='utf-8') as file:
            file.write(markdown_text)
            print(f"create {name}.md in {self.output_folder} successfully")

    def change_title(self, title):
        return title

    def start(self):
        if(self.url.startswith("https://www.piaotian.com")):
            html = self.send_request_d(self.url)
        else:
            html = self.send_request(self.url)
        if html:
            self.fetch_novel_content(html)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Article Crawler")
    parser.add_argument("-u", "--url", required=True, help="URL of the article to crawl")
    parser.add_argument("-o", "--output", required=True, help="Output folder for the crawled article")
    parser.add_argument("-c", "--config", default="config.json", help="Path to the configuration file")
    args = parser.parse_args()
    args.url = "https://www.piaotia.com/html/15/15012/"

    crawler = NovelCrawler(url=args.url, output_folder=args.output, config_path=args.config)
    crawler.start()