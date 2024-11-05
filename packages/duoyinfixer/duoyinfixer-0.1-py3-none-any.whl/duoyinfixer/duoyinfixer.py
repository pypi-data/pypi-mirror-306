def _load():
    import json
    with open('duoyinfixer/rescources/homophones_set.json', 'r', encoding='utf-8') as file:
        homophones_set = json.load(file)
    with open('duoyinfixer/rescources/monosyllabi_character_one_sound_2_one_character.json', 'r', encoding='utf-8') as file:
        monosyllabi_character = json.load(file)
    return homophones_set, monosyllabi_character

from pypinyin import pinyin

def use_pypinyin(input_zh_char):
    
    res = pinyin(input_zh_char, v_to_u=True)
    res = [re[0] for re in res]
    return res

import re

def fixer(input : str):
    homophones_set, monosyllabi_character = _load()
    # 使用正则表达式将输入字符串按标点拆分为列表
    input_list = re.split(r'([,，。！？；：\.\?!;:])', input)
    # 去掉空字符串
    input_list = [item for item in input_list if item]

    # todo 使用hash 加快一下速度
    def check(sen):
        result = []
        for index, char in enumerate(sen):
            if char in homophones_set:
                result.append(index)
        
        return result

    output_result = []
    for sen in input_list:
        sen_check = check(sen)
        if sen_check:
            sen_pinyin = use_pypinyin(sen)
            sen_list = list(sen)
            for index in sen_check:
                duoyin_pinyin = sen_pinyin[index]
                danyinzi = monosyllabi_character.get(duoyin_pinyin, None)
                if danyinzi : sen_list[index] = danyinzi
            sen = ''.join(sen_list)
        
        output_result.append(sen)
    output_result = ''.join(output_result)
    return output_result

if __name__ == "__main__":
    input = "我好想睡觉啊，睡醒之后就去玩游戏！"
    OUT = fixer(input)
    print(OUT)