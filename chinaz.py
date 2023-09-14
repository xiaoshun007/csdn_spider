import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import zipfile

def get_last_li_content(soup):
    # 查找class为el-pager的ul标签
    ul = soup.find('ul', class_='el-pager')

    # 查找ul中的最后一个li标签
    last_li = ul.find_all('li')[-1] if ul else None

    # 提取最后一个li标签的内容
    if last_li:
        last_li_content = last_li.get_text()
        return last_li_content

    return None

def get_url(page):
    url = 'https://down.chinaz.com/search/mysql_code_' + str(page) + ".htm"
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    divs_with_name_class = soup.find_all('div', class_='name')
    i = 0
    for div in divs_with_name_class:
        link = div.find('a')
        url = urljoin("https://down.chinaz.com", link['href'])
        i = i + 1
        print(str(i) + ": " + url)
        
        try:
            download(url)
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

def download(url):
    response = requests.get(url)
    html_content = response.text

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找功能介绍
    introduce_div_class = 'introduce'  # 替换为你要解析的div的id或class等标识符
    introduce_div = soup.find('div', attrs={'class': introduce_div_class})  # 根据id查找div，可根据class等属性自行更改

    # 提取div的文本内容
    div_text = '\n'.join(introduce_div.stripped_strings)

    # 打印提取的文本内容
    # print(div_text)
    # 将内容保存到.txt文件
    introduce_filename = 'output.txt'  # 指定文件名
    with open(introduce_filename, 'w') as file:
        file.write(div_text)
    print(f'Saved content to {introduce_filename} successfully.')

    # 查找特定div的超链接内容
    div_class = 'download-list'  # 替换为你要解析的div的id或class等标识符
    div = soup.find('div', attrs={'class': div_class})  # 根据id查找div，可根据class等属性自行更改

    # 遍历超链接并保存附件内容到本地
    links = div.find_all('a')
    for link in links:
        file_url = urljoin("https://down.chinaz.com", link['href'])
        filename = link.text + '.zip'  # 添加.zip后缀
        response = requests.get(file_url)
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f'Saved {filename} successfully.')
        break  # 提前结束循环，只保存第一个满足条件的超链接附件
        
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

    # 若想保存到特定目录，可以使用以下代码将文件保存到指定目录中
    # folder = 'path/to/folder'  # 替换为你的目录路径
    # os.makedirs(folder, exist_ok=True)
    # with open(os.path.join(folder, filename), 'wb') as file:
    #     file.write(response.content)
    
if __name__ == '__main__':
    # mysql下载到14页 
    url = 'https://down.chinaz.com/search/mysql_code_1.htm'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    
    last_li_content = get_last_li_content(soup)
    if last_li_content:
        for num in range(1, int(last_li_content)+1):
            print("Downloading " + str(num) + "content......")
            get_url(num)
    else:
        print("No last li content found.")