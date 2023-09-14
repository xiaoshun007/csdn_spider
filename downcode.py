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
            
    introduce_filename = 'output.txt'  # 指定文件名
    with open(introduce_filename, 'w') as file:
        file.write(title)
    print(f'Saved content to {introduce_filename} successfully.')
            
    # 创建一个新的.zip文件
    zip_filename = 'archive_' + filename + ".zip"

    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        # 添加output.txt文件到压缩文件中
        zip_file.write(introduce_filename)

        # 添加另一个文件到压缩文件中
        file_to_add = filename  # 替换为你要添加的文件名
        zip_file.write(file_to_add)

    print(f'Successfully created {zip_filename} with the files.')
    
    # 删除introduce_filename和filename文件
    os.remove(introduce_filename)
    os.remove(filename)                
    
        
def extract_content(string):
    # 使用split()方法和切片操作提取满足条件的内容
    content = string.split("'")[1]
    
    # 打印提取的内容
    return content
    

def download(page):
    url = 'https://www.downcode.com/sort/j_7_218_' + str(page) + '.html'
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
        if i < 4:
            continue
        
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
