# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/10/29 10:58
# 文件名称： hao6v.py
# 项目描述： 电影资源网站API：https://www.6v123.com/
# 开发工具： PyCharm
import random
import re
import urllib
import asyncio
from random import choice
from copy import deepcopy
from parsel import Selector
from urllib.parse import urljoin
from xiaoqiangclub.config.constants import UA
from xiaoqiangclub.config.log_config import log
from xiaoqiangclub.utils.decorators import retry
from typing import (Tuple, List, Dict, Union, Optional)
from xiaoqiangclub.utils.network_utils import get_response_async

MAX_CONCURRENCY = 5  # 最大并发量

# 旧版hao6v网站链接
OLD_URLS = ["https://www.hao6v.me", "https://www.6v520.com", "https://www.6v520.net", "https://www.hao6v.tv/"]
# 旧版hao6v网站链接（不支持的域名）
OLD_URLS_NONSUPPORT = ["https://www.6vgood.net/", "https://www.6vhao.net", "https://www.6vdyy.com"]
# 新版hao6v网站链接
NEW_URLS = ["https://www.xb6v.com/", "https://www.66s6.net/", "https://www.66s6.cc/", "https://www.66ss.org/"]

HEADERS = {"User-Agent": choice(UA)}
RETRY_TIMES = 1  # 重试次数
RESPONSE_ENCODING = "gbk"  # 网络响应返回的默认编码，网站上标示的是gb2312，但是使用gb2312会出现一些字符乱码的问题


@retry(max_retries=RETRY_TIMES)
async def today_recommendations() -> Tuple[List[dict]]:
    """
    获取hao6v老版本主页的今日推荐内容

    :return: 今日推荐电影和电视剧推荐
    """
    url = choice(OLD_URLS)  # 随机选择一个URL

    def extract_recommendations(ul):
        """从ul元素中提取推荐内容"""
        return [
            {
                "title": li.css("font::text").get(),  # 标题
                "cover_img": li.css("img::attr(src)").get(),  # 封面图片链接
                "detail_url": url + li.css("a::attr(href)").get()  # 详情页链接

            }
            for li in ul.css("li")
        ]

    selector = await get_response_async(url, headers=HEADERS, return_parsel_selector=True,
                                        default_encoding=RESPONSE_ENCODING)
    today_rec_movies = extract_recommendations(selector.css("ul.pic")[0])  # 今日推荐
    tv_rec = extract_recommendations(selector.css("ul.pic")[1])  # 电视剧推荐

    return today_rec_movies, tv_rec


@retry(max_retries=RETRY_TIMES)
async def download_ranking_list(mode: int = 0, only_red: bool = False) -> List[dict]:
    """
    下载排行榜
    :param mode: 0：周下载排行榜；1：月下载排行榜；2：总下载排行榜
    :param only_red: 只获取排行榜中的标红资源，默认为False
    :return:
    """
    ranking_list = list()  # 排行榜数据

    if mode in [0, 1]:
        url = random.choice(OLD_URLS).rstrip('/') + '/dy/'
        selector = await get_response_async(url=url, headers=HEADERS, return_parsel_selector=True,
                                            default_encoding=RESPONSE_ENCODING)
        if mode == 0:
            lis = selector.xpath('//div[@class="col5"]/div[1]//li')
        else:
            lis = selector.xpath('//div[@class="col5"]/div[2]//li')

    elif mode == 2:
        url = random.choice(OLD_URLS)
        selector = await get_response_async(url=url, headers=HEADERS, return_parsel_selector=True,
                                            default_encoding=RESPONSE_ENCODING)
        # 查找包含 "下载排行榜" 的h3标签的兄弟节点ul
        lis = selector.xpath(r"//h3[contains(text(), '下载排行榜')]/following-sibling::ul[1]/li")
    else:
        raise ValueError("mode 参数错误！只能取值：0、1、2")

    for li in lis:
        movie_data = dict()  # 影视数据

        color = li.css('font::attr(color)').get()
        if only_red and not color:
            continue

        if color:
            movie_data['title'] = li.css('font::text').get().strip()  # 标题
            movie_data['red'] = True  # 是否标红
        else:
            movie_data['title'] = li.css('a::text').get().strip()
            movie_data['red'] = False

        movie_data['detail_url'] = random.choice(OLD_URLS).rstrip('/') + li.css('a::attr(href)').get()
        if mode != 2:
            movie_data['update_date'] = li.css('span::text').get().lstrip('[').rstrip(']').strip()

        ranking_list.append(movie_data)

    return ranking_list


@retry(max_retries=RETRY_TIMES)
async def __get_comments(url: str = None, selector: Selector = None,
                         sem: asyncio.Semaphore = None) -> List[str]:
    """
    获取评论
    :param url: 评分和评论的链接
    :param selector: Selector对象
    :param sem: asyncio.Semaphore对象，用于限制最大并发量
    :return:
    """
    if not url and not selector:
        raise ValueError("url 和 selector 参数不能同时为空")

    if url:
        selector = await get_response_async(url, headers=HEADERS, return_parsel_selector=True, follow_redirects=True,
                                            default_encoding=RESPONSE_ENCODING, sem=sem)

    comments = []
    comments_tds = selector.xpath('//table[@width="96%"]//tr/td[@colspan="2"]')
    for td in comments_tds:
        cs = td.xpath('.//text()').getall()
        # 去除空格和空行
        comment = [i.strip() for i in cs if i.strip()]
        # 用空格连接
        comment = ' '.join(comment)
        # 去除：网友 匿名 的原文：
        comment = comment.replace('网友 匿名 的原文：', '')
        comments.append(comment.strip())

    return comments


@retry(max_retries=RETRY_TIMES)
async def __get_score_and_comments_data(url: str, sem: asyncio.Semaphore = None) -> Dict[str, Union[str, List[str]]]:
    """
    获取评分和评论
    满分 5 颗星
    :param url: 评分和评论的链接
    :param sem: asyncio.Semaphore对象，用于限制最大并发量
    :return:
    """
    selector = await get_response_async(url, headers=HEADERS, return_parsel_selector=True,
                                        default_encoding=RESPONSE_ENCODING, sem=sem)
    stars = selector.css('span.star-rating li::attr(class)').get().strip('current-rating')  # 评分
    # 评分人数：id="fennum"
    num_of_votes = selector.css('#fennum::text').get().strip()

    comments = await __get_comments(selector=selector, sem=sem)

    # 判断是否有下一页
    next_pages = selector.xpath("//a[contains(text(), '下一页')]/preceding-sibling::a/@href").getall()

    if next_pages:
        # 创建异步任务列表
        tasks = []
        for next_page in next_pages:
            tasks.append(asyncio.create_task(__get_comments(url=random.choice(OLD_URLS).rstrip('/') + next_page,
                                                            sem=sem)))
        log.info(f'开始并发获取共 {len(tasks)} 页的评论数据，并发数为：{sem._value}，请耐心等待...')
        next_pages_data = await asyncio.gather(*tasks)
        for data in next_pages_data:
            # 去除空格和空行
            data = [i.strip() for i in data if i.strip()]
            comments.extend(data)

    return {
        "得分": stars,  # 几个星，最高5颗星
        "评分人数": num_of_votes,
        "评论": comments
    }


@retry(max_retries=RETRY_TIMES)
async def __get_m3u8_link(title: str, play_url: str, sem: asyncio.Semaphore = None) -> Optional[Dict[str, str]]:
    """
    获取 m3u8 链接
    :param title: 影视标题
    :param play_url: 播放页面的播放链接
    :param sem: asyncio.Semaphore对象，用于控制并发请求的数量，默认为 None，不控制并发数量
    :return:
    """
    selector = await get_response_async(play_url, headers=HEADERS, return_parsel_selector=True, timeout=10, sem=sem)

    if not selector:
        return None

    iframe = selector.css('iframe::attr(src)').get()
    if iframe:
        m3u8 = iframe
    else:
        # 使用正则提取m3u8链接
        matches = re.findall(r'source:\s*"(https?://[^"]+\.m3u8)"', selector.get())
        if not matches:
            return None

        m3u8 = matches[0]

    return {"title": title, "m3u8_link": m3u8}


@retry(max_retries=RETRY_TIMES)
async def get_online_watching_links(online_url: str,
                                    max_concurrency: int = MAX_CONCURRENCY) -> List[List[Dict[str, str]]]:
    """
    获取在线观看的链接
    :param online_url: 在线观看页面的在线播放链接
    :return:
    """
    sem = asyncio.Semaphore(max_concurrency)
    selector = await get_response_async(online_url, headers=HEADERS, return_parsel_selector=True, sem=sem)

    # 获取所有播放地址
    divs = selector.xpath("//h3[contains(text(),'播放地址')]/..")
    m3u8_list = []

    for div in divs[:2]:  # 只获取前两个，它每页有4个播放地址，前2个是无需插件的地址
        tasks = []
        for a in div.xpath('.//a'):
            title = a.attrib['title']
            link = a.attrib['href']
            link = random.choice(NEW_URLS).rstrip('/') + link
            tasks.append(__get_m3u8_link(title, link, sem=sem))

        log.info(f'开始并发获取 {len(tasks)} 个播放地址，并发数为：{max_concurrency}，请耐心等待...')
        task_ret = await asyncio.gather(*tasks)
        # 将包含None的元素过滤掉
        task_ret = ([i for i in task_ret if i])
        if task_ret:
            m3u8_list.append(task_ret)

    return m3u8_list


@retry(max_retries=RETRY_TIMES)
async def __get_detail_url_links(selector: Selector, title: str) -> Dict[str, Union[str, List[Dict[str, str]]]]:
    """
    获取详情页中的链接
    :param selector: 详情页的Selector对象
    :param title: 影视标题
    :return:
    """
    tds = selector.xpath('//td[@bgcolor="#ffffbb"]')
    magnet_data = dict()
    magnet_links = []
    for td in tds:
        keywords = td.xpath('./text()').get()
        if '在线观看' in keywords:
            magnet_data['online_watching_page'] = td.xpath('./a/@href').get()  # 在线观看页面
            continue

        title_text = td.xpath('./a/text()').get()
        magnet_link = td.xpath('./a/@href').get()
        magnet_links.append({
            "title": f"[{title}]{title_text}",  # 标题
            "magnet_link": magnet_link  # 磁链
        })
    magnet_data["magnet_links"] = magnet_links
    return magnet_data


@retry(max_retries=RETRY_TIMES)
async def get_detail_url_data(detail_url: str, only_magnets: bool = False,
                              get_score_and_comments: bool = False,
                              max_concurrency: int = MAX_CONCURRENCY) -> Dict[str, Union[str, List[str]]]:
    """
    获取详情页数据
    :param detail_url: 详情页链接
    :param only_magnets: 是否只获取磁链，默认为 False：获取所有信息，True：只获取磁链，get_score_and_comments参数不生效
    :param get_score_and_comments: 是否获取评分和评论，默认为 False，不获取
    :param max_concurrency: 最大并发量，默认为5
    :return:
    """
    sem = asyncio.Semaphore(max_concurrency)
    movie_info = dict()  # 存储电影信息

    selector = await get_response_async(detail_url, headers=HEADERS, return_parsel_selector=True,
                                        default_encoding=RESPONSE_ENCODING, sem=sem)
    title = selector.css("div.box h1::text").get()  # 标题

    magnet_data = await __get_detail_url_links(selector, title)  # 提取页面的链接
    if only_magnets:
        return magnet_data.get("magnet_links", [])

    movie_info["title"] = title
    movie_info.update(magnet_data)  # 磁链
    # 查找包含 '◎简　　介' 的 <p> 标签
    target_p = selector.xpath("//p[contains(text(), '◎简　　介')]")

    cover_img = []  # 封面图片
    screenshots = []  # 截图

    if target_p:
        # 查找目标 <p> 标签之前的所有 <p> 标签中的 <img> 标签
        for p in selector.xpath("//p[contains(text(), '◎简　　介')]/preceding::p//img"):
            cover_img.append(p.xpath("@src").get())

        # 查找目标 <p> 标签之后的所有 <p> 标签中的 <img> 标签
        for p in selector.xpath("//p[contains(text(), '◎简　　介')]/following::p//img"):
            screenshots.append(p.xpath("@src").get())

    movie_info.update({"cover_img": cover_img} if cover_img else {})
    movie_info.update({"screenshots": screenshots} if screenshots else {})

    # css获取id="endText"下的所有文本
    content = selector.xpath("//div[@id='endText']//text()").getall()
    # 去除空白字符
    content = [i.strip() for i in content if i.strip()]
    # 重新整理/分割
    content = "#".join(content).split('#【下载地址】')[0].split('内容介绍：#◎')[-1].split('#◎')
    # 将\u3000\u3000替换为空格
    content = [i.replace('\u3000', '') for i in content]
    # 去除#，但保留包含“主演”的行
    content = [i.replace('#', '') if '主演' not in i else i for i in content]

    # 提取字段
    fields = ["译名", "片名", "年代", "产地", "类别", "语言", "字幕", "上映日期", "IMDb评分",
              "豆瓣评分", "集数", "片长", "导演", "编剧", "主演", "简介"]
    for text in content:
        for field in fields:
            if field in text:
                text = text.replace(field, '').strip()
                if field == '主演':
                    test = text.split('#')
                else:
                    test = text.split('/')
                text = [i.strip() for i in test]
                movie_info[field] = text

    if get_score_and_comments:
        # 评分和评论：<iframe name="ifc" id="ifc"
        score_and_comments_url = random.choice(OLD_URLS).rstrip('/') + selector.css('#ifc::attr(src)').get()
        score_and_comments_data = await __get_score_and_comments_data(score_and_comments_url, sem=sem)
        movie_info.update(score_and_comments_data)

    return movie_info


@retry(max_retries=RETRY_TIMES)
async def get_list_page_data(url: str, only_red: bool = True, get_page_num: int = 1, get_all: bool = False,
                             sem: asyncio.Semaphore = None) -> List[dict]:
    """
    获取hao6v列表展示页面的数据，例如（最近更新电影）：https://www.6v520.net/dy/index.html
    :param url: 列表页链接
    :param only_red:只获取标红的电影，默认为True
    :param get_page_num:获取的页数，默认为1，即获取当前页
    :param get_all:是否获取所有页面，默认为True，注意：获取所有页面时，get_page_num参数无效
    :param sem: 异步请求的信号量，默认为None，即不限制并发量
    :return:
    """
    selector = await get_response_async(url, headers=HEADERS, return_parsel_selector=True,
                                        default_encoding=RESPONSE_ENCODING, sem=sem)

    lis = selector.css('ul.list li')
    movies = list()
    for li in lis:
        m = dict()

        color = li.css('font::attr(color)').get()
        if only_red and not color:
            continue

        if color:
            m['title'] = li.css('font::text').get().strip()  # 标题
            m['red'] = True  # 是否标红
        else:
            m['title'] = li.css('a::text').get().strip()
            m['red'] = False

        m['detail_url'] = random.choice(OLD_URLS).rstrip('/') + li.css('a::attr(href)').get()
        m['update_date'] = li.css('span::text').get().lstrip('[').rstrip(']').strip()

        if not only_red:
            m["red"]: bool(color)  # 是否标红资源

        movies.append(m)
    if get_all or get_page_num > 1:
        # 判断是否有下一页
        total_pages = selector.xpath(
            "//div[@class='listpage'][last()]/b/text()").get()  # getall() ['1/587', '25', '14668'] 可以获取到总页数，每页数量，总数量
        total_pages = int(total_pages.split('/')[-1])

        if total_pages > 1:
            pages = min(total_pages, int(get_page_num)) + 1
            if get_all:
                pages = total_pages + 1

            if pages > 2:
                tasks = []
                for i in range(2, pages):
                    # 创建下一页的url，例如:https://www.6v520.net/dy/index_2.html
                    next_page_url = url.rstrip('/') + f'/index_{i}.html'
                    # 并发任务
                    tasks.append(get_list_page_data(next_page_url, only_red, sem=sem))

                log.info(f'开始并发获取共 {len(tasks)} 页的列表页面数据，并发数为：{sem._value}，请耐心等待...')
                next_page_movies = await asyncio.gather(*tasks)
                for next_page_movie in next_page_movies:
                    movies.extend(next_page_movie)

    return movies


async def get_all_movies(only_red: bool = True, get_page_num: int = 1, get_all: bool = True,
                         max_concurrency: int = MAX_CONCURRENCY) -> List[dict]:
    """
    获取hao6v的所有电影数据
    :param only_red: 只获取标红的电影，默认为True
    :param get_page_num: 获取的页数，默认为1，即获取第一页：https://www.6v520.net/dy/
    :param get_all: 是否获取所有页面，默认为True，注意：获取所有页面时，get_page_num参数无效
    :param max_concurrency: 最大并发数，默认为5
    :return:
    """
    sem = asyncio.Semaphore(max_concurrency)
    url = random.choice(OLD_URLS).rstrip('/') + '/dy/'
    return await get_list_page_data(url, only_red=only_red, get_page_num=get_page_num, get_all=get_all, sem=sem)


async def get_all_anime(only_red: bool = True, get_page_num: int = 1, get_all: bool = True,
                        max_concurrency: int = MAX_CONCURRENCY) -> List[dict]:
    """
    获取hao6v的所有动漫数据
    :param only_red: 只获取标红的电影，默认为True
    :param get_page_num: 获取的页数，默认为1，即获取第一页：https://www.6v520.net/dy/
    :param get_all: 是否获取所有页面，默认为True，注意：获取所有页面时，get_page_num参数无效
    :param max_concurrency: 最大并发数，默认为5
    :return:
    """
    sem = asyncio.Semaphore(max_concurrency)
    url = random.choice(OLD_URLS).rstrip('/') + '/zydy/'
    return await get_list_page_data(url, only_red=only_red, get_page_num=get_page_num, get_all=get_all, sem=sem)


async def get_chinese_tv(only_red: bool = True, get_page_num: int = 1, get_all: bool = True,
                         max_concurrency: int = MAX_CONCURRENCY) -> List[dict]:
    """
    获取hao6v的国产电视剧数据：https://www.6v520.net/dlz/
    :param only_red: 只获取标红的电影，默认为True
    :param get_page_num: 获取的页数，默认为1，即获取第一页：https://www.6v520.net/dy/
    :param get_all: 是否获取所有页面，默认为True，注意：获取所有页面时，get_page_num参数无效
    :param max_concurrency: 最大并发数，默认为5
    :return:
    """
    sem = asyncio.Semaphore(max_concurrency)
    url = random.choice(OLD_URLS).rstrip('/') + '/dlz/'
    return await get_list_page_data(url, only_red=only_red, get_page_num=get_page_num, get_all=get_all, sem=sem)


async def get_mandarin_chinese_movies(only_red: bool = True, get_page_num: int = 1, get_all: bool = True,
                                      max_concurrency: int = MAX_CONCURRENCY) -> List[dict]:
    """
    获取hao6v的所有国语片数据：https://www.6v520.net/gydy/
    :param only_red: 只获取标红的电影，默认为True
    :param get_page_num: 获取的页数，默认为1，即获取第一页：https://www.6v520.net/dy/
    :param get_all: 是否获取所有页面，默认为True，注意：获取所有页面时，get_page_num参数无效
    :param max_concurrency: 最大并发数，默认为5
    :return:
    """
    sem = asyncio.Semaphore(max_concurrency)
    url = random.choice(OLD_URLS).rstrip('/') + '/gydy/'
    return await get_list_page_data(url, only_red=only_red, get_page_num=get_page_num, get_all=get_all, sem=sem)


async def get_latest_movies(only_red: bool = True) -> List[dict]:
    """
    获取hao6v的最新电影数据（50部）
    :param only_red:只获取标红的电影，默认为True
    :return:
    """
    url = random.choice(OLD_URLS).rstrip('/') + '/gvod/zx.html'
    return await get_list_page_data(url, only_red)


async def get_latest_tv(only_red: bool = True) -> List[dict]:
    """
    获取hao6v的最新电视剧数据（50部）
    :param only_red:只获取标红的电影，默认为True
    :return:
    """
    url = random.choice(OLD_URLS).rstrip('/') + '/gvod/dsj.html'
    return await get_list_page_data(url, only_red)


@retry(max_retries=RETRY_TIMES)
async def __parse_search_page(url: str = None, selector: Selector = None, only_detail_links: bool = False,
                              sem: asyncio.Semaphore = None):
    """
    从搜索结果网页中解析出资源详情页链接
    :param url: 搜索结果页链接
    :param selector: 搜索结果网页的 Selector 对象
    :param only_detail_links: 是否只返回详情页链接，默认为 False，返回所有链接
    :param sem: asyncio.Semaphore对象，用于控制并发请求的数量，默认为 None，不控制并发数量
    :return:
    """
    if not url and not selector:
        raise ValueError("url 和 selector 参数不能同时为空")
    if url:
        selector = await get_response_async(url, headers=HEADERS, return_parsel_selector=True, follow_redirects=True,
                                            default_encoding=RESPONSE_ENCODING, sem=sem)

    # 使用 parsel 提取链接
    page_results = []  # 存储当前页面数据
    tables = selector.xpath('//div[@class="box"]//table[@width="100%"]')[2:]
    for table in tables:
        detail_url = random.choice(OLD_URLS).rstrip('/') + table.xpath(
            './/div[@align="center"]//td[1]/font/span/a/@href').get()
        if only_detail_links:
            page_results.append(detail_url)
            continue

        movie_info = dict()  # 存储单个影视信息
        movie_info['detail_url'] = detail_url
        movie_info['title'] = table.xpath('.//div[@align="center"]//td[1]/font/span/a/text()').get()  # 标题
        movie_info['class_type'] = table.xpath('.//div[@align="center"]//td[1]/font/a/text()').get()  # 类别
        movie_info['发布时间'] = table.xpath('.//div[@align="center"]//td[2]//text()').get().lstrip(
            '发布时间：').strip()  # 发布时间
        content = table.xpath('.//td[@bgcolor="#EBF3FA"]//text()').getall()
        # 去除空格和空白行
        content = [i.strip() for i in content if i.strip()]
        # 将\u3000\u3000替换为空格
        content = [i.replace('\u3000', '') for i in content]
        # 去除◎
        content = [i.replace('◎', '') for i in content]

        # 提取字段
        fields = ["译名", "片名", "中 文 名", "英 文 名", "出品人", "年代", "国家", "产地", "类别", "语言", "字幕",
                  "上映日期", "IMDb评分", "豆瓣评分", "集数", "片长", "导演", "编剧", "主演", "简介", "出品人",
                  "出品"]
        for text in content:
            for field in fields:
                if field in text:
                    text = text.replace(field, '').strip()
                    text = [i.strip() for i in text.split('/')]
                    movie_info[field] = text

        page_results.append(movie_info)

    return page_results


async def search_movie(search_query: str, only_detail_links: bool = True,
                       max_concurrency: int = MAX_CONCURRENCY) -> Optional[List]:
    """
    搜索电影
    :param search_query: 搜索关键字，长度大于2小于10
    :param only_detail_links: 是否只获取详情页的链接，默认为 True
    :param max_concurrency:最大并发数，默认为5
    :return: [资源1详情, 资源2详情, ...]
    """
    sem = asyncio.Semaphore(max_concurrency)

    # 搜索关键字，长度大于2小于10
    search_query = search_query.strip()
    if len(search_query) < 2 or len(search_query) > 10:
        raise ValueError('搜索关键字长度必须大于2小于10。')

    while_urls = deepcopy(OLD_URLS)
    for i in range(len(OLD_URLS)):
        # 随机选择一个URL
        base_url = random.choice(while_urls)
        while_urls.remove(base_url)
        base_url = base_url.lstrip('/') + '/'

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded",
            "dnt": "1",
            "origin": base_url,
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": base_url,
            "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "cross-site",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
        }
        keyboard = urllib.parse.quote(search_query.encode('gb2312'))

        data_str = f"show=title%2Csmalltext&tempid=1&keyboard={keyboard}&tbname=article&x={random.randint(10, 20)}&y={random.randint(10, 20)}"
        headers['Content-Length'] = str(len(data_str))
        url = base_url + 'e/search/index.php'

        response = await get_response_async(url, headers=headers, data=data_str, follow_redirects=True,
                                            default_encoding=RESPONSE_ENCODING, sem=sem)

        if not response:
            if i == len(OLD_URLS) - 1:
                log.error(f"请求 {url} 失败，请检查网络连接或稍后再试。")
                return None

            log.warning(f"请求 {url} 失败，尝试下一个URL...")
            continue

        check_strings = ["没有搜索到相关的内容", "系统限制的搜索关键字只能在"]
        if any(string in response.text for string in check_strings):
            log.warning(f"没有搜索到 {search_query} 相关的资源！")
            return None

        selector = Selector(response.text)
        search_results = await __parse_search_page(selector=selector, only_detail_links=only_detail_links,
                                                   sem=sem)  # 解析当前页面数据

        # 判断是否有下一页
        next_pages = selector.xpath("//a[contains(text(), '下一页')]/preceding-sibling::a/@href").getall()

        if next_pages:
            # 创建异步任务列表
            tasks = []
            for next_page in next_pages:
                tasks.append(asyncio.create_task(
                    __parse_search_page(url=base_url.rstrip('/') + next_page, only_detail_links=only_detail_links,
                                        sem=sem)))
            log.info(f'开始并发获取共 {len(tasks)} 页的搜索数据，并发数为：{max_concurrency}，请耐心等待...')
            next_pages_data = await asyncio.gather(*tasks)
            for data in next_pages_data:
                search_results.extend(data)

        return search_results
