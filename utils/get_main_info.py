import time
from tqdm import tqdm
import pandas as pd
from .tools import _parse_webpage, _get_info_table_1, _get_info_table_2, _get_info_table_3, _get_info_table_4, _get_info_table_5


def _get_info_single_(link, verbose=False):
    """获取单个页面的信息：分支、描述、再部署时间、部署费用、阻挡数、攻击间隔、"""
    _start_time_0 = time.time()

    page = _parse_webpage(link)

    _end_time_0 = time.time()
    if verbose:
        print(f"soup time: {_end_time_0 - _start_time_0}")

    _start_time_1 = time.time()
    table1 = page.find_all("table", class_="wikitable logo")[0]
    table2 = page.find_all(
        "table", class_="wikitable logo char-extra-attr-table")[0]
    table3 = page.find_all(
        "table", class_="wikitable logo char-base-attr-table")[0]
    table4 = page.find_all("table", class_="wikitable nomobile logo")[
        0]  # 攻击范围
    # id为mw-normal-catlinks的div
    div5 = page.find_all("div", id="mw-normal-catlinks")[0]

    archetype, traits = _get_info_table_1(table1)
    redeploy_time, dp_cost, block, attack_interval = _get_info_table_2(table2)
    max_hp, atk, def_, res = _get_info_table_3(table3)
    range_amount = _get_info_table_4(table4)
    class_ = _get_info_table_5(div5)

    _end_time_1 = time.time()
    if verbose:
        print(f"table time: {_end_time_1 - _start_time_1}")

    info_single = [archetype, traits, redeploy_time, dp_cost, block, attack_interval,
                   max_hp, atk, def_, res, range_amount, class_]
    return info_single


def get_info(df, verbose=False):
    """遍历所有数据，获取信息，存入info中（replace=True）"""
    all_info_title = ["分支", "描述",
                      "再部署时间", "部署费用", "阻挡数", "攻击间隔",
                      "生命上限", "攻击", "防御", "法术抗性",
                      "攻击范围",
                      "职业"]
    info = pd.DataFrame(columns=all_info_title)
    for i in tqdm(range(len(df))):
        if verbose:
            print(
                f"current operator: {df.iloc[[i]]['name'].values[0].strip()}")
        row = df.iloc[[i]]
        link = row["link"].values[0].strip()
        info_single = _get_info_single_(
            link)
        info_title = ["分支", "描述",
                      "再部署时间", "部署费用", "阻挡数", "攻击间隔",
                      "生命上限", "攻击", "防御", "法术抗性",
                      "攻击范围",
                      "职业"]
        for j in range(len(info_title)):
            info.loc[i, info_title[j]] = info_single[j]
    return info
