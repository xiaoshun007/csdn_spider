import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile

def get_code(url, title):
    response = requests.get(url)
    html_content = response.text
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    # 查找class属性为linenums的ol标签
    pre = soup.find('pre', class_='prettyprint linenums')
    file_name = title + '.txt'
    with open(file_name, 'w') as file:
        file.write(pre.text)
    print(f'Saved content to {file_name} successfully.')
    
    # 创建一个新的.zip文件
    zip_filename = 'archive_' + file_name + ".zip"

    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        # 添加output.txt文件到压缩文件中
        zip_file.write(file_name)

    print(f'Successfully created {zip_filename} with the files.')
    
    # 删除filename文件
    os.remove(file_name)
    
    
def get_url(page):
    url = 'https://www.dotcpp.com/wp/project_code/page/' + str(page)
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    divs_with_name_class = soup.find_all('article', class_='excerpt')
    i = 0
    for div in divs_with_name_class:
        link = div.find('a')
        url = link['href']
        i = i + 1
        print(str(i) + ": " + url)
        
        try:
            get_code(url, link.text)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue        
          
        
if __name__ == '__main__':
    for num in range(1, 4):
        print("Downloading " + str(num) + "content......")
        get_url(num)
    