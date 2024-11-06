import re
import collections
from location_util.dictionary_loader import china_location_loader, china_location_change_loader
from functools import lru_cache


class LocationParser(object):

    def __init__(self):
        self.administrative_map_dict = {}
        self.town_village = False
        self.town_village_dict = {}

    def _mapping(self, china_loc, china_change_loc):
        # 整理行政区划码映射表
        self.administrative_map_dict = {}

        for prov in china_loc:
            if prov.startswith('_'):
                continue
            if china_loc[prov]['_alias'] in self.municipalities_cities:
                pass
            else:
                self.administrative_map_dict[china_loc[prov]['_admin_code']] = [
                    china_loc[prov]['_admin_code'],
                    [prov, china_loc[prov]['_alias']],
                    [None, None],
                    [None, None], True]  # True 表示数据为最新地名，反之为旧地名

            for city in china_loc[prov]:
                if city.startswith('_'):
                    continue

                for alias_name in china_loc[prov][city]['_alias']:
                    self.administrative_map_dict[china_loc[prov][city]['_admin_code']] = [
                        china_loc[prov][city]['_admin_code'],
                        [prov, china_loc[prov]['_alias']],
                        [city, alias_name],
                        [None, None], True]

                    for district in china_loc[prov][city]:
                        if district.startswith('_'):
                            continue
                        self.administrative_map_dict[china_loc[prov][city][district]['_admin_code']] = [
                            china_loc[prov][city][district]['_admin_code'],
                            [prov, china_loc[prov]['_alias']],
                            [city, alias_name],
                            ['经济技术开发区' if district.endswith('经济技术开发区') else district,
                             china_loc[prov][city][district]['_alias']],
                            True]

                        if self.town_village:  # 补充 self.town_village_list
                            key_name = prov + city + district
                            self.town_village_dict.setdefault(key_name, china_loc[prov][city][district])

        # 将旧有的地名融入 self.administrative_map_dict，并建立映射表
        self.old2new_loc_map = {}

        for item in china_change_loc:
            self.administrative_map_dict['000000'] = [
                '000000', item['old_loc'][0], item['old_loc'][1], item['old_loc'][2], False]
            self.old2new_loc_map.update(
                {''.join([i[0] for i in item['old_loc'] if i[0] is not None]): item['new_loc']})

    @lru_cache(maxsize=None)
    def _prepare(self):
        self.municipalities_cities = {'北京', '上海', '天津', '重庆', '香港', '澳门'}
        self.loc_alias_string = '【loc_alias】'
        self.exception_suffix_pattern = re.compile('(【loc_alias】(路|大街|街))')

        # 添加中国区划词典
        china_loc = china_location_loader(detail=self.town_village)
        china_change_loc = china_location_change_loader()
        self._mapping(china_loc, china_change_loc)

        self.loc_level_key_list = ['省', '市', '县']
        if self.town_village:
            self.loc_level_key_list.extend(['乡', '村'])
        self.loc_level_key_dict = dict([(loc_level, None) for loc_level in self.loc_level_key_list])

    def get_candidates(self, location_text):
        """ 从地址中获取所有可能涉及到的候选地址 """
        candidate_admin_list = []  # 候选列表
        for admin_code, admin_item in self.administrative_map_dict.items():  # 修改为字典遍历
            count = 0  # 匹配个数
            offset_list = [[-1, -1], [-1, -1], [-1, -1]]

            for idx, name_item in enumerate(admin_item[1:4]):
                match_flag = False
                for alias_idx, name in enumerate(name_item):  # 别名与全名任意匹配一个
                    if name is not None and name in location_text:
                        if alias_idx == 1 and not self._process_exception_alias(name, location_text):
                            continue
                        match_flag = True
                        offset_list[idx][0] = location_text.index(name)
                        offset_list[idx][1] = alias_idx
                        break

                if match_flag:
                    count += 1
                    if idx == 1 and offset_list[idx - 1][0] >= 0 and offset_list[idx][0] - offset_list[idx - 1][0] == 1:
                        count = 0
                        break
                    if idx == 2 and (
                            offset_list[idx - 1][0] >= 0 and offset_list[idx][0] - offset_list[idx - 1][0] == 1 or
                            offset_list[idx - 2][0] >= 0 and offset_list[idx][0] - offset_list[idx - 2][0] == 1):
                        count = 0
                        break

            if count > 0:
                if admin_item[1][1] in self.municipalities_cities and admin_item[1][1] in location_text:
                    count -= 1
                if len(admin_item) == 5:
                    admin_item.extend([count, offset_list])
                    candidate_admin_list.append(admin_item)
                elif len(admin_item) == 7:
                    admin_item[-2] = count
                    admin_item[-1] = offset_list
                    candidate_admin_list.append(admin_item)
                else:
                    raise ValueError('length of admin_item is wrong!')

        return candidate_admin_list

    def _process_exception_alias(self, name, location_text):
        # 处理一些异常的简称，如 “上海市嘉定区太原路99号” 中的 太原 这个简称
        location_text = location_text.replace(name, self.loc_alias_string)
        matched_res = self.exception_suffix_pattern.search(location_text)
        return matched_res is None

    def __call__(self, location_text, town_village=False, change2new=True):
        self.town_village = town_village
        if not self.administrative_map_dict or (self.town_village and not self.town_village_dict):
            self._prepare()

        # 获取文本中的省、市、县三级行政区划
        candidate_admin_list = self.get_candidates(location_text)

        if not candidate_admin_list:
            result = {'province': None, 'city': None, 'district': None, 'detail': location_text,
                      'full_location': location_text, 'orig_location': location_text}
            if self.town_village:
                result.update({'town': None, 'village': None})
            return self._get_flag_and_result(result)

        # 去除那些同一个 offset 匹配了多个别名的内容
        non_same_offset_list = []
        for item in candidate_admin_list:
            offset_list = [i[0] for i in item[-1] if i[0] > -1]
            if len(offset_list) != len(set(offset_list)):  # 说明有重复匹配项
                the_same_offset = collections.Counter(offset_list).most_common()[0][0]
                the_same_offset_loc = [i for i in item[-1] if i[0] == the_same_offset]  # 长度必然为 2
                if the_same_offset_loc[0][1] == 0 and the_same_offset_loc[1][1] == 1:
                    # 此时说明地址同一个位置的词汇匹配到了不同的全名和别名，
                    # 其中第一个为高级别的 地名，为省、市，第二个为低级别的，市、县。
                    # 若匹配到高级别的全名和低级别的别名，则将该 item 丢弃，否则保留
                    pass
                else:
                    non_same_offset_list.append(item)
            else:
                non_same_offset_list.append(item)
        candidate_admin_list = non_same_offset_list

        # 找出文本中匹配数量最多的
        max_matched_num = max(item[-2] for item in candidate_admin_list)
        candidate_admin_list = [item for item in candidate_admin_list if item[-2] == max_matched_num]

        # 对于有些新旧地名简称相同，且省市县不按靠前的位置依次排开的，删除旧地名
        if len(candidate_admin_list) == 2:
            if [i[0] for i in candidate_admin_list[0][-1]] == [i[0] for i in candidate_admin_list[1][-1]]:
                candidate_admin_list = [item for item in candidate_admin_list if item[4] is True]
            elif [i[1] for i in candidate_admin_list[0][1:4]] == [i[1] for i in candidate_admin_list[1][1:4]]:
                candidate_admin_list = [item for item in candidate_admin_list if item[4] is True]

        if len(candidate_admin_list) == 1:
            result = self._get_final_res(candidate_admin_list[0], location_text, [], town_village=town_village,
                                         change2new=change2new)
            return self._get_flag_and_result(result)

        # 找出匹配位置最靠前的
        candidate_admin_list = sorted(candidate_admin_list, key=lambda i: sum(j[0] for j in i[-1]))

        # 对于有些 地市名 和 县级名简称相同的，需要进行过滤，根据被匹配的 offset 进行确定。
        new_candidate_admin_list = []
        for item in candidate_admin_list:
            if item[1][1] in self.municipalities_cities:
                new_candidate_admin_list.append(item)
            else:
                if -1 not in [item[-1][0][0], item[-1][1][0], item[-1][2][0]]:
                    # 省、市、县全都匹配到
                    if (item[-1][0][0] < item[-1][1][0]) and (item[-1][1][0] < item[-1][2][0]):
                        # 必须按照 省、市、县的顺序进行匹配
                        new_candidate_admin_list.append(item)
                else:
                    new_candidate_admin_list.append(item)
        candidate_admin_list = new_candidate_admin_list

        if not candidate_admin_list:
            result = {'province': None, 'city': None, 'district': None, 'detail': location_text,
                      'full_location': location_text, 'orig_location': location_text}
            return self._get_flag_and_result(result)

        min_matched_offset = sum(j[0] for j in candidate_admin_list[0][-1])
        candidate_admin_list = [item for item in candidate_admin_list if
                                sum(j[0] for j in item[-1]) == min_matched_offset]

        # 优先匹配包含全名的，其次匹配别名
        full_alias_list = [min(j[1] for j in item[-1] if j[1] > -1) for item in candidate_admin_list]
        full_alias_min = min(full_alias_list)
        candidate_admin_list = [item for val, item in zip(full_alias_list, candidate_admin_list) if
                                val == full_alias_min]

        # 若全部都匹配别名，则别名获取级别应当越高越好
        alias_matched_num_list = [
            len([i[0] for i in item[-1] if i[0] > -1]) for item in candidate_admin_list]
        max_alias_matched_num = max(alias_matched_num_list)
        if full_alias_min == 1 and max_alias_matched_num == 1:
            candidate_admin_list = sorted(candidate_admin_list,
                                          key=lambda item: [idx for idx, i in enumerate(item[-1]) if i[0] != -1][0])

        # 去除重复地名
        new_candidate_admin_list = []
        for item in candidate_admin_list:
            if item[0] == '000000':
                loc_key = ''.join(
                    [item[1][0] if item[1][0] is not None else '', item[2][0] if item[2][0] is not None else '',
                     item[3][0] if item[3][0] is not None else ''])
                if loc_key in self.old2new_loc_map:
                    new_loc = self.old2new_loc_map[loc_key]
                    has_new_loc_flag = any(
                        new_loc[0] == _item[1][0] and new_loc[1] == _item[2][0] and new_loc[2] == _item[3][0] for _item
                        in candidate_admin_list if _item[0] != '000000')
                    if not has_new_loc_flag:
                        new_candidate_admin_list.append(item)
                else:
                    new_candidate_admin_list.append(item)
            else:
                new_candidate_admin_list.append(item)

        candidate_admin_list = new_candidate_admin_list

        # 县级存在重复名称，计算候选列表中可能重复的县名
        county_dup_list = [item[3][item[-1][-1][1]] for item in candidate_admin_list]
        county_dup_list = [item[0] for item in collections.Counter(county_dup_list).most_common() if item[1] > 1]

        final_admin = candidate_admin_list[0]  # 是所求结果

        result = self._get_final_res(final_admin, location_text, county_dup_list, town_village=town_village,
                                     change2new=change2new)
        return self._get_flag_and_result(result)

    def _get_final_res(self, final_admin, location_text, county_dup_list, town_village=True, change2new=True):
        detail_idx = 0
        final_prov = None
        final_city = None
        final_county = None

        for admin_idx, i in enumerate(final_admin[-1]):
            if i[0] != -1:
                detail_idx = i[0] + len(final_admin[admin_idx + 1][i[1]])
                if admin_idx >= 0 and final_admin[admin_idx + 1][i[1]] not in county_dup_list:
                    final_prov = final_admin[1][0]
                if admin_idx >= 1 and final_admin[admin_idx + 1][i[1]] not in county_dup_list:
                    final_city = final_admin[2][0]
                if admin_idx >= 2 and final_admin[admin_idx + 1][i[1]] not in county_dup_list:
                    final_county = final_admin[3][0]
                else:
                    final_county = final_admin[3][i[1]]

        if change2new:
            tmp_key = ''.join([final_prov if final_prov else '', final_city if final_city else '',
                               final_county if final_county else ''])
            if tmp_key in self.old2new_loc_map:
                final_prov, final_city, final_county = self.old2new_loc_map[tmp_key]

        detail_part = location_text[detail_idx:]
        if detail_part and detail_part[0] in '县':
            detail_part = detail_part[1:]

        if final_city is not None and '直辖' in final_city:
            final_city = None
        if final_county is not None and '直辖' in final_county:
            final_county = None

        admin_part = ''
        if final_prov is not None:
            admin_part = final_prov
        if final_city is not None:
            match_temp_flag = any(temp_city in final_city for temp_city in self.municipalities_cities)
            if not match_temp_flag:
                admin_part += final_city
        if final_county is not None:
            admin_part += final_county

        result = {'province': final_prov, 'city': final_city, 'district': final_county, 'detail': detail_part,
                  'full_location': admin_part + detail_part, 'orig_location': location_text}

        if town_village:
            result = self._get_town_village(result)
        return result

    def _get_town_village(self, result):
        town = None
        village = None

        prov = result['province'] if result['province'] is not None else ''
        city = result['city'] if result['city'] is not None else '省直辖行政区划'
        district = result['district'] if result['district'] is not None else '市直辖行政区划'
        key_name = ''.join([prov, city, district])

        if key_name not in self.town_village_dict:
            result.update({'town': town, 'village': village})
            return result

        town_list = list(self.town_village_dict[key_name].keys())
        for _town in town_list:
            if _town in result['detail']:
                town = _town
                break

        if town is not None:
            village_list = list(self.town_village_dict[key_name][town].keys())
            for _village in village_list:
                if _village in result['detail']:
                    village = _village
                    break

        result.update({'town': town, 'village': village})
        return result

    def _get_flag_and_result(self, result):
        for key in result.keys():
            if result[key] is None:
                result[key] = ''
        return (True, result) if result['province'] or result['city'] or result['district'] else (False, result)
