from .tools import _parse_webpage
import pandas as pd


def _get_info_date_div(div):
    """获取该页面下的干员名称和上线时间"""
    names = []
    rarities = []
    dates = []
    # 找到tbody，信息在里面的tr中
    tbody = div.find_all("tbody")[0]
    # 将每个tr中的前3个td的内容分别存为干员名称、稀有度、上线时间
    tr = tbody.find_all("tr")
    for i in range(1, len(tr)):
        td = tr[i].find_all("td")
        name = td[0].text.split("\n")[0]
        rarity = td[1].text.split("\n")[0]
        date = td[2].text.split("\n")[0]
        names.append(name)
        rarities.append(rarity)
        dates.append(date)
    return names, rarities, dates


def get_date_info(link):
    date_info_title = ["name", "稀有度", "上线时间（国服）"]
    date_info = pd.DataFrame(columns=date_info_title)

    page = _parse_webpage(link)
    div = page.find_all(
        "div", class_="mw-parser-output")[0]
    names, rarities, dates = _get_info_date_div(div)
    date_info["name"] = names
    date_info["稀有度"] = rarities
    date_info["上线时间（国服）"] = dates
    return date_info
