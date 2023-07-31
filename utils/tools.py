import requests
from bs4 import BeautifulSoup


def _parse_webpage(link):
    r = requests.get(link)
    r.encoding = "utf-8"
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    return soup
# region tables


def _get_info_table_1(table):
    """获得信息“分支” “描述” """
    # 找到第二个tr，获取其中第一个td中的文本，存为“分支”；第二个td中的所有文本（可能会有部分文本在span内），存为“描述”
    tr = table.find_all("tr")[1]
    td = tr.find_all("td")
    archetype = td[0].text.split("\n")[0]
    traits = td[1].text.split("\n")[0]
    return archetype, traits


def _get_info_table_2(table):
    """获得信息“再部署时间” “部署费用” “阻挡数” “攻击间隔” """
    # 获取4个td中的文本，存为所需信息
    td = table.find_all("td")
    redeploy_time = td[0].text.split("\n")[0]
    dp_cost = td[1].text.split("\n")[0]
    block = td[2].text.split("\n")[0]
    attack_interval = td[3].text.split("\n")[0]
    return redeploy_time, dp_cost, block, attack_interval


def _get_info_table_3(table):
    """
    获得信息“生命上限” “攻击” “防御” “法术抗性”
    其中每一类信息有5种值，我们以后缀表示：_0_1, _0_max, _1_max, _2_max, trust_extra_status
    """
    # 我们用列表来储存这些信息
    max_hp = []
    atk = []
    def_ = []
    res = []
    all_info = [max_hp, atk, def_, res]
    # 找到所有tr，跳过第一个，从剩下的4个tr中获取信息
    # 剩下的每个tr里的td储存了信息，获取它们（如果为空，就用0代替）
    tr = table.find_all("tr")
    for i in range(1, 5):
        td = tr[i].find_all("td")
        for j in range(5):
            text = td[j].text.split("\n")[0]
            if text == "":
                text = "0"
            all_info[i-1].append(text)
    return max_hp, atk, def_, res


def _get_info_table_4(table):
    """获取信息“攻击范围”，返回一个列表"""
    range_amount = []
    # 第二个tr中有3或者2个td，每个td中<use>的数量就是攻击范围
    tr = table.find_all("tr")[1]
    tds = tr.find_all("td")
    for td in tds:
        range_amount.append(len(td.find_all("use")))
    return range_amount

# endregion


def change_column(df, column: str, c: int):
    """
    将df中的column列向前/向后移动c列
    df: 要修改的DataFrame
    column: 要修改的列名
    line: 要修改的列名的位置
    return: 修改后的df
    """
    df.insert(c, column, df.pop(column))
    return df
