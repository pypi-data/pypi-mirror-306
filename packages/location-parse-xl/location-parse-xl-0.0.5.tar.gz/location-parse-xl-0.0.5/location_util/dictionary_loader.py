import os
import re
import json
import math

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
GRAND_DIR_PATH = os.path.dirname(DIR_PATH)

__all__ = ['china_location_change_loader', 'china_location_loader',
           'world_location_loader']


def read_file_by_line(file_path, line_num=None,
                      skip_empty_line=True, strip=True,
                      auto_loads_json=True):
    """ 读取一个文件的前 N 行，按列表返回，
    文件中按行组织，要求 utf-8 格式编码的自然语言文本。
    若每行元素为 json 格式可自动加载。

    Args:
        file_path(str): 文件路径
        line_num(int): 读取文件中的行数，若不指定则全部按行读出
        skip_empty_line(boolean): 是否跳过空行
        strip: 将每一行的内容字符串做 strip() 操作
        auto_loads_json(bool): 是否自动将每行使用 json 加载，默认是

    Returns:
        list: line_num 行的内容列表

    """
    content_list = list()
    count = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        line = f.readline()
        while True:
            if line == '':  # 整行全空，说明到文件底
                break
            if line_num is not None:
                if count >= line_num:
                    break

            if line.strip() == '':
                if skip_empty_line:
                    count += 1
                    line = f.readline()
                else:
                    try:
                        if auto_loads_json:
                            cur_obj = json.loads(line.strip())
                            content_list.append(cur_obj)
                        else:
                            if strip:
                                content_list.append(line.strip())
                            else:
                                content_list.append(line)
                    except:
                        if strip:
                            content_list.append(line.strip())
                        else:
                            content_list.append(line)

                    count += 1
                    line = f.readline()
                    continue
            else:
                try:
                    if auto_loads_json:
                        cur_obj = json.loads(line.strip())
                        content_list.append(cur_obj)
                    else:
                        if strip:
                            content_list.append(line.strip())
                        else:
                            content_list.append(line)
                except:
                    if strip:
                        content_list.append(line.strip())
                    else:
                        content_list.append(line)

                count += 1
                line = f.readline()
                continue

    return content_list

def china_location_loader(detail=False):
    """ 加载中国地名词典 china_location.txt

    Args:
        detail(bool): 若为 True，则返回 省、市、县区、乡镇街道、村社区 五级信息；
            若为 False，则返回 省、市、县区 三级信息

    """
    with open(os.path.join(GRAND_DIR_PATH, 'location_util/china_location.txt'),
              'r', encoding='utf-8') as f:
        location_jio = f.readlines()

    cur_province = None
    cur_city = None
    cur_county = None
    cur_town = None
    cur_village = None
    location_dict = {}

    for item in location_jio:
        if not item.startswith('\t'):  # 省
            if len(item.strip().split('\t')) != 3:
                continue

            province, admin_code, alias_name = item.strip().split('\t')
            cur_province = province
            location_dict.update(
                {cur_province: {'_full_name': province,
                                '_alias': alias_name,
                                '_admin_code': admin_code}})

        elif item.startswith('\t\t\t\t'):  # 村、社区
            if not detail:
                continue
            cur_village = item.strip()
            location_dict[cur_province][cur_city][cur_county][cur_town].update(
                {cur_village: None})

        elif item.startswith('\t\t\t'):  # 乡镇、街道
            if not detail:
                continue
            cur_town = item.strip()
            location_dict[cur_province][cur_city][cur_county].update(
                {cur_town: dict()})

        elif item.startswith('\t\t'):  # 县、区
            if len(item.strip().split('\t')) != 3:
                continue
            county, admin_code, alias_name = item.strip().split('\t')
            cur_county = county
            location_dict[cur_province][cur_city].update(
                {cur_county: {'_full_name': county,
                              '_alias': alias_name,
                              '_admin_code': admin_code}})

        else:  # 市
            if len(item.strip().split('\t')) != 3:
                continue
            city, admin_code, alias_name = item.strip().split('\t')
            cur_city = city
            if '/' in alias_name:
                alias_name_list = alias_name.split('/')
                location_dict[cur_province].update(
                    {cur_city: {'_full_name': city,
                                '_alias': alias_name_list,
                                '_admin_code': admin_code}})
            else:
                location_dict[cur_province].update(
                    {cur_city: {'_full_name': city,
                                '_alias': [alias_name],
                                '_admin_code': admin_code}})

    return location_dict


def china_location_change_loader():
    """ 加载中国地名变更词典 china_location_change.txt
    整理了 2018 年至今国内政府批复修改的县级以上的地名变化。仅添加了地名的撤销变更，
    而对未撤销地名的新增地名，如深圳市光明区，不做记录，因为不影响工具的使用。

    Returns:
        dict: 返回 省、市、县区 三级的变更地址，以及变更日期和批准部门；
            '国批' 表示国务院批准，'民批' 表示国务院民政部批准，
            '省批'表示省级政府或民政部批准。

    """
    location_change_jio = read_file_by_line(
        os.path.join(GRAND_DIR_PATH, 'location_util/china_location_change.txt'),
        auto_loads_json=False)

    location_change_list = []
    for line in location_change_jio:
        location_change_dict = dict()
        line_seg = line.split('=>')
        orig_line_seg = line_seg[0].split('\t')
        new_line_seg = line_seg[1].split('\t')

        if len(orig_line_seg) == 8:  # 县一级
            location_change_dict.update(
                {'date': orig_line_seg[0], 'department': orig_line_seg[1],
                 'old_loc': [orig_line_seg[2: 4], orig_line_seg[4: 6], orig_line_seg[6: 8]],
                 'new_loc': new_line_seg})

        elif len(orig_line_seg) == 6:  # 市一级，主要是 襄樊市 => 襄阳市
            assert len(new_line_seg) == 2, 'error with line `{}`'.format(line)

            location_change_dict.update(
                {'date': orig_line_seg[0], 'department': orig_line_seg[1],
                 'old_loc': [orig_line_seg[2: 4], orig_line_seg[4: 6], [None, None]],
                 'new_loc': [new_line_seg[0], new_line_seg[1], None]})

        location_change_list.append(location_change_dict)

    return location_change_list


def world_location_loader():
    """ 加载世界地名词典 world_location.txt """
    content = read_file_by_line(
        os.path.join(GRAND_DIR_PATH, 'location_util/world_location.txt'),
        auto_loads_json=False)

    result = {}
    cur_continent = None

    for line in content:
        if '洲:' in line:
            cur_continent = line.replace(':', '')
            result.update({cur_continent: dict()})
            continue

        item_tup = line.split('\t')
        item_length = len(item_tup)
        if item_length == 3:
            result[cur_continent].update(
                {item_tup[0]: {'full_name': item_tup[1],
                               'capital': item_tup[2]}})

        if item_length == 4:
            result[cur_continent].update(
                {item_tup[0]: {'full_name': item_tup[1],
                               'capital': item_tup[2],
                               'main_city': item_tup[3].split('/')}})
        else:
            pass

    return result
