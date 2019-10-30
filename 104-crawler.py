import csv
import time
import codecs
import requests
from bs4 import BeautifulSoup

def fetch(url):

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    articles = soup.find_all('article', 'job-list-item')

    posts = []
    for article in articles:
        meta = article.find('div', 'b-block__left').find('a')
        posts.append({
            'title': meta.getText().strip(),
            'link': 'https:' + meta.get('href'),
        })
    return posts

def fetch_jobs_details(target_url):

    res = requests.get(target_url)
    soup = BeautifulSoup(res.text,'lxml')

    job = {}
    job['職位名稱'] = soup.find_all('meta')[4]['content'].rstrip(' - 104人力銀行')
    job['工作內容'] = soup.find('p').text.replace('\r','')
    job['職務類別'] = soup.find('dd','cate').text.strip().split()[0]
    job['工作待遇'] = soup.find('dd','salary').text.strip().split()[0]
    job['工作地點'] = soup.find('dd','addr').text.strip().split()[0]
    job['擅長工具'] = soup.select('.info')[1].find_all('dd')[-3].text
    job['工作技能'] = soup.select('.info')[1].find_all('dd')[-2].text
    job['其它條件'] = soup.select('.info')[1].find_all('dd')[-1].text.replace('\r','')

    return job

def get_job_detail(resp):

    job_content_list = []

    for res in resp:
        job_content = fetch_jobs_details(res['link'])
        job_content_list.append(job_content)

    if job_content_list:
        return job_content_list
    
def export_file(dict_data):

    csv_file = "104jobs.txt"
    csv_columns = ['職位名稱','工作內容','職務類別','工作待遇','工作地點','擅長工具','工作技能','其它條件']

    try:
        with open(csv_file, 'w', encoding='UTF-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)

    except IOError:
        print("I/O error")

if __name__ == '__main__':

    job_content_list = []
    key_url = 'https://www.104.com.tw/jobs/search/?ro=0&keyword=語意分析' # target url

    start = time.time()
    for i in range(1,11):
        jobs_page_url = key_url + '&order=1&asc=0&page='+str(i)+'&mode=s'
        resp = fetch(jobs_page_url)

        try:
            job_content  = get_job_detail(resp)
            job_content_list.extend(job_content)
            
        except:
            pass
            
    export_file(job_content_list)
    
    print('印出總筆數：' , len(job_content_list))
    print('花費: %f 秒' % (time.time() - start))