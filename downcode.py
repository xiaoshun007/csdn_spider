import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile

def getZip(url, title):
    response = requests.get(url)
    html_content = response.text

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser', from_encoding='gb2312')

    # 查找包含特定图片名称的img标签
    li_list = soup.find_all('li', class_='one_4')

    # 遍历img标签，输出超链接的内容
    for li in li_list:
        link = li.find('a')
        if link:
            file_url = extract_content(link['href'])
            filename = title + '.zip'
            response = requests.get(file_url)
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'Saved {filename} successfully.')
            break
    
        
def extract_content(string):
    # 使用split()方法和切片操作提取满足条件的内容
    content = string.split("'")[1]
    
    # 打印提取的内容
    return content
    

def download(page):
    url = 'https://www.downcode.com/sort/j_7_89_' + str(page) + '.html'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser', from_encoding='gb2312')
    divs_with_name_class = soup.find_all('div', class_='j_text_sort_a')
    i = 0
    for div in divs_with_name_class:
        link = div.find('a')
        url = extract_content(link['href'])
        i = i + 1
        print(str(i) + ": " + url)
        
        try:
            text = link.get_text().encode('iso-8859-1').decode('gbk')
            print(text)
            getZip(url, text)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue   
        

if __name__ == '__main__':
    for num in range(1, 22):
        print("Downloading " + str(num) + "content......")
        download(num)