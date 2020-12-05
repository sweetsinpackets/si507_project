import json
import requests
from bs4 import BeautifulSoup
import datetime
from class_definition import shooting_record
import class_definition
import pandas as pd
import sqlite3

DB_CACHE_FILE = "database_cache.db"
CACHE_FILENAME = "cache.json"
# use request header to avoid being blocked
REQUEST_HEADER = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
PROXY = {
    "http":"socks5://127.0.0.1:10808",
    "https":"socks5://127.0.0.1:10808"
}
COLUMN_NAME = ("Incident_ID", "Incident_Date", "State", "City_or_County", "Address", "Killed", "Injured")


# generate cache key of crawl request
# format: $(base_url)\+$(today)
def crawl_request_cache_key(url:str):
    today = datetime.date.today()
    return url + "+" + str(today.year) + "-" + str(today.month)

# generate cache key of API request
# format: $(base_url)\+(($(param_key)\?$(param_value))\+)*$(today)
def api_request_cache_key(url:str, params:dict=None):
    params_str = ""
    if params:
        for (key, value) in params.items():
            params_str += key + "?" + value + "+"
    today = datetime.date.today()
    return url + "+" + params_str


# webpage request with cache
def web_request(url:str, header=REQUEST_HEADER):
    try:
        with open(CACHE_FILENAME, 'r') as cache_file:
            cache_contents = cache_file.read()
            cache_dict = json.loads(cache_contents)
    except:
        cache_dict = {}
    
    key = crawl_request_cache_key(url)

    if key in cache_dict.keys():
        print("Found in website cache, reading...")
        return cache_dict[key]
    else:
        print("No cache found for webpage, need to fetch from Internet, which may take several seconds to several minutes...")
        resp = requests.get(url, headers=header, timeout=10, proxies=PROXY)
        content = resp.text.encode(resp.encoding).decode('utf-8', 'ignore')
        cache_dict[key] = content
        dumped_json_cache = json.dumps(cache_dict)
        with open(CACHE_FILENAME,"w") as fw:
            fw.write(dumped_json_cache)
        return content


# API request with cache
def api_request(url:str, header=None):
    try:
        with open(CACHE_FILENAME, 'r') as cache_file:
            cache_contents = cache_file.read()
            cache_dict = json.loads(cache_contents)
    except:
        cache_dict = {}
    
    key = api_request_cache_key(url, params=header)

    if key in cache_dict.keys():
        print("Reading API cache...")
        return cache_dict[key]
    else:
        print("No API cached result, need to fetch...")
        resp = requests.get(url, params=header)
        content = resp.text.encode(resp.encoding).decode('utf-8', 'ignore')
        cache_dict[key] = content
        dumped_json_cache = json.dumps(cache_dict)
        with open(CACHE_FILENAME,"w") as fw:
            fw.write(dumped_json_cache)
        return content






# recursively scrape all pages under a base_url
# used to script shooting cases
# if there is not "next page", then end the recursion
# return a pandas dataframe
def multiple_scrape(url:str) -> pd.core.frame.DataFrame:
    html = web_request(url)
    soup = BeautifulSoup(html, "html.parser")

    res = pd.DataFrame(columns=COLUMN_NAME)

    temp_list = []
    # find all records and pack into shooting_record
    for tr in soup.find("table").find("tbody").findAll('tr'):
        row = class_definition.transform([i.text for i in tr.findAll("td")])
        temp_list.append(row)
    res = res.append(temp_list, ignore_index=True)

    next_page = soup.find("li", class_="pager-next")
    rest = []
    if next_page:
        href = "https://www.gunviolencearchive.org/" + next_page.find("a").get("href")
        rest = multiple_scrape(href)
    return res.append(rest, ignore_index=True)


# here's an alternative, abandoned because costing too slow
def multiple_scrape_in_class(url:str) -> list:
    html = web_request(url)
    soup = BeautifulSoup(html, "html.parser")

    res = []

    # find all records and pack into shooting_record
    for tr in soup.find("table").find("tbody").findAll('tr'):
        tds = [i.text for i in tr.findAll("td")]
        record = shooting_record(init_list=tds)
        res.append(record)

    next_page = soup.find("li", class_="pager-next")
    rest = []
    if next_page:
        href = "https://www.gunviolencearchive.org/" + next_page.find("a").get("href")
        rest = multiple_scrape_in_class(href)
    return res + rest

# crawl the main pages, return a dict {name:link}
def crawl_main_page(main_page_url:str)->dict:
    html = web_request(main_page_url)
    soup = BeautifulSoup(html, "html.parser")
    res = {}
    for li in soup.find("div", class_="reports-list").find("div", class_="columns-container").findAll("li"):
        a = li.find("a")
        key = a.get_text()
        value = "https://www.gunviolencearchive.org" + a.get("href")
        res[key] = value

    return res


################# SQL ##################

# the top interface for multiple page crawling, using SQL cache
def crawl_report_page(url:str) -> pd.core.frame.DataFrame:
    conn = sqlite3.connect(DB_CACHE_FILE)

    key = crawl_request_cache_key(url)
    
    # judge if exists
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_list = [i[0] for i in cur.fetchall()]

    if key in table_list:
        print("Reading from SQL cache...")
        df = pd.read_sql("SELECT * FROM \"" + key + "\"", conn)
    else:
        print("No SQL records found, looking for webpage cache...")
        df = multiple_scrape(url)
        df.to_sql(key, conn)

    conn.close()
    return df

