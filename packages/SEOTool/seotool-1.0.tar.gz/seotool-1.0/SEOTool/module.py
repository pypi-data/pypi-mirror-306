import requests, re
from urllib import parse
from fake_useragent import UserAgent
from lxml import html
from time import sleep
from random import uniform

class SEOTool:
    '''
    200: 收录\n
    201: 前50无匹配\n
    202: 无收录\n
    '''
    print("SEO小助手Ver1.0 by Tr0nTan\n本脚本无任何反爬手段，大量搜索推荐使用代理隧道\n效率取决于代理和网络")

    def __init__(self, proxyUrl: str = None):
        # 创建User-Agent
        self.ua = UserAgent(browsers=['chrome','edge','firefox'],os=['windows'],platforms=['pc'])
        # 创建代理
        if proxyUrl:
            self.proxies = {
                "http": proxyUrl,
                "https": proxyUrl
            }
        else:
            self.proxies=None
    
    def session_init(self, old_session: requests.session = None) -> requests.session:
        if old_session:
            old_session.close()
        new_session = requests.session()
        if self.proxies:
            new_session.proxies.update(self.proxies)
        new_session.headers.update({
            'Host': 'www.baidu.com',
            'User-Agent': self.ua.random
        })
        return new_session

    def request_sender(self, session_object: requests.session, url: str) -> requests.Response:
        response = None
        try:
            response = session_object.get(url, timeout=3)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            pass
        finally:
            return response

    def baidu_rank_checker(self, search_word: str, targeturl: str) -> tuple:
        baidu_url = f'http://www.baidu.com/s?wd={parse.quote(search_word)}&rn={50}'
        title_pattern = f'<title>{search_word}_百度搜索</title>'
        mu_pattern = f'mu="{targeturl}"'
        session = self.session_init()
        count = 0
        while True:
            sleep(count*2 + uniform(0,1))
            response = self.request_sender(session, baidu_url)
            if response:
                # 标题检测
                if title_pattern in response.text:
                    pass
                else:
                    session = self.session_init(old_session=session)
                    count += 1
                    print('标题', search_word)
                    continue
                # 目标链接存在检测
                if mu_pattern in response.text:
                    pass
                else:
                    return (targeturl,'201')
                # tree生成
                try:
                    tree = html.fromstring(response.text)
                except:
                    session = self.session_init(old_session=session)
                    count += 1
                    print('tree')
                    continue
                # 排名列表
                try:
                    ranklist = tree.xpath("//div[@id='content_left' and @tabindex='0']")[0].getchildren()
                except:
                    session = self.session_init(old_session=session)
                    count += 1
                    print('排名列表')
                    continue
                for item in ranklist:
                    try:
                        url = item.attrib['mu']
                    except:
                        pass
                    if url == targeturl:
                        return (targeturl,item.attrib['id'])
            else:
                session = self.session_init(old_session=session)
    
    def baidu_index_checker(self, targeturl: str) -> bool:
        baidu_url = f'http://www.baidu.com/s?wd={targeturl}&rn={10}'
        title_pattern = f'<title>{targeturl}_百度搜索</title>'
        mu_pattern = f'mu="{targeturl}"'
        session = self.session_init()
        count = 0
        while True:
            sleep(count*2 + uniform(0,1))
            response = self.request_sender(session, baidu_url)
            if response:
                if title_pattern in response.text:
                    pass
                else:
                    session = self.session_init(old_session=session)
                    count += 1
                    continue
                if mu_pattern in response.text:
                    return True
                else:
                    return False
            else:
                session = self.session_init(old_session=session)

    def baidu_rs_collecter(self, search_word: str) -> tuple:
        all_rs_texts=[]
        baidu_url = f'http://www.baidu.com/s?wd={parse.quote(search_word)}&rn={10}'
        title_pattern = f'<title>{search_word}_百度搜索</title>'
        session = self.session_init()
        while True:
            response = self.request_sender(session, baidu_url)
            if response:
                if title_pattern in response.text:
                    pass
                else:
                    session = self.session_init(old_session=session)
                    continue
        try:
            searchtitle = soup.find('title').get_text()
            if keyword not in searchtitle:
                return ('402', keyword)
        except:
            return ('401', keyword)
        
        table = soup.find_all('a', class_= re.compile("rs-link"))
        if table != []:
            for i in table: 
                all_rs_texts.append(i.get_text())
            return (keyword, all_rs_texts)
        else:
            return ('405', keyword)