import requests
from bs4 import BeautifulSoup
import time
import re
import zipfile

def main():
    for page in range(31):
        url = f"https://www.sourcecodester.com/python?page={page}"
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='views-row')

        for div in divs:
            node_content = div.find('div', class_='node-content')
            if node_content is None:
                continue
            
            link = node_content.find('a')
            if link is None:
                continue
                
            link_text = link.text
            download_file_name = link_text.replace('\n', '')
            link_text = link.text.replace(' ', '+').replace('\n', '')
            print("链接文本：", link_text)
            
            article = div.find('article', recursive=False)
            node_id = article.get('data-history-node-id')
            print("node_id：", node_id)
            
            download_url = f"https://www.sourcecodester.com/download-code?nid={node_id}&title={link_text}"
            # 访问 download_url
            response_download = requests.get(download_url)
            # 使用 BeautifulSoup 解析响应内容
            soup_download = BeautifulSoup(response_download.text, 'html.parser')
            
            # 查找内容为 "direct link" 的超链接
            direct_link = soup_download.find('a', text='direct link')
            
            if direct_link:
                direct_link_url = direct_link['href']
                direct_link_url = "https://www.sourcecodester.com" + direct_link_url
                print("直链地址：", direct_link_url)
                
                # 直接访问直链地址并保存到本地文件
                response_direct_link = requests.get(direct_link_url)
                
                # 保存文件到本地
                with open(f"{download_file_name}.zip", 'wb') as file:
                    file.write(response_direct_link.content)
                
    
if __name__ == "__main__":
    main()
