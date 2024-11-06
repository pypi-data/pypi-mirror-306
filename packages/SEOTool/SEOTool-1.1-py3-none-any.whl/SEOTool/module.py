import requests
from urllib import parse
from fake_useragent import UserAgent
from lxml import html
from time import sleep
from random import uniform

class SEOTool:

    print("SEO小助手Ver1.1 by Tr0nTan\n本脚本无任何反爬手段，大量搜索推荐使用代理隧道\n效率取决于代理和网络")

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
        '''
        该辅助函数用以创建，更新session object\n
        仅创建session无需传参\n
        若需更新请传入旧session
        '''
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
        '''
        该辅助函数用以发送请求\n
        若直接使用请输入session object & 目标url
        '''
        response = None
        try:
            response = session_object.get(url, timeout=3)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            pass
        finally:
            return response

    def baidu_rank_checker(self, search_word: str, targeturl: str) -> tuple:
        '''
        该函数用以查询目标url的百度排名\n
        使用示例：\n
        result = baidu_rank_checker(search_word = '牛战士', targeturl = 'https://www.zhihu.com/question/286807184/answer/3296579670')
        '''
        baidu_url = f'http://www.baidu.com/s?wd={parse.quote(search_word)}&rn={50}'
        title_pattern = f'<title>{search_word}_百度搜索</title>'
        mu_pattern = f'mu="{targeturl}"'
        session = self.session_init()
        while True:
            sleep(uniform(0,1))
            response = self.request_sender(session, baidu_url)
            # 响应检测
            if response:
                # 标题检测
                if title_pattern in response.text:
                    pass
                else:
                    session = self.session_init(old_session=session)
                    continue
                # 目标链接检测
                if mu_pattern in response.text:
                    pass
                else:
                    return (targeturl,'前50无匹配')
                # tree生成
                try:
                    tree = html.fromstring(response.text)
                except:
                    session = self.session_init(old_session=session)
                    continue
                # 排名列表
                try:
                    ranklist = tree.xpath("//div[@id='content_left' and @tabindex='0']")[0].getchildren()
                except:
                    session = self.session_init(old_session=session)
                    continue
                # 遍历排行列表
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
        '''
        该函数用以查询目标url的百度收录\n
        使用示例：\n
        result = baidu_index_checker(targeturl = 'https://www.zhihu.com/question/286807184/answer/3296579670')
        '''
        baidu_url = f'http://www.baidu.com/s?wd={targeturl}&rn={10}'
        title_pattern = f'<title>{targeturl}_百度搜索</title>'
        mu_pattern = f'mu="{targeturl}"'
        session = self.session_init()
        while True:
            sleep(uniform(0,1))
            response = self.request_sender(session, baidu_url)
            # 响应检测
            if response:
                # 标题检测
                if title_pattern in response.text:
                    pass
                else:
                    session = self.session_init(old_session=session)
                    continue
                # 目标链接检测
                if mu_pattern in response.text:
                    return True
                else:
                    return False
            else:
                session = self.session_init(old_session=session)

    def baidu_rs_collector(self, search_word: str) -> tuple:
        '''
        该函数用以查询搜索词的百度相关搜索\n
        使用示例：\n
        result = baidu_rs_collector(search_word = '牛战士')
        '''
        baidu_url = f'http://www.baidu.com/s?wd={parse.quote(search_word)}&rn={10}'
        title_pattern = f'<title>{search_word}_百度搜索</title>'
        session = self.session_init()
        while True:
            sleep(uniform(0,1))
            response = self.request_sender(session, baidu_url)
            if response:
                # 标题检测
                if title_pattern in response.text:
                    pass
                else:
                    session = self.session_init(old_session=session)
                    continue
                # 相关搜索检测
                if '相关搜索' in response.text:
                    pass
                else:
                    return (search_word, 'NO_RS')
                # tree生成
                try:
                    tree = html.fromstring(response.text)
                except:
                    session = self.session_init(old_session=session)
                    print('tree')
                    continue
                # 相关搜索收集
                try:
                    rs = tree.xpath("//a[@class='rs-link_2DE3Q c-line-clamp1 c-color-link']/@title")
                except:
                    rs=[]
                return (search_word, rs)
            else:
                session = self.session_init(old_session=session)
