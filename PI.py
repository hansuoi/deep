# 性格分析を行う文書を読み込む
def read_file(path):
    with open(path, mode='rt', encoding='utf-8') as f:
        profile_text = f.read()

    return profile_text


# 性格分析を行う
def do_Personality_Insights(profile_text, lang):
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
    from ibm_watson import PersonalityInsightsV3

    # ./APIkey.txtの1行目に、API鍵が記述されているので、それを読み込む
    with open('C:/Users/User/prog/python/persona/APIkey.txt', mode='rt', encoding='utf-8') as api:
        APIkey = api.read()

    authenticator = IAMAuthenticator(APIkey)

    service = PersonalityInsightsV3(
      version="2017-10-13",
      authenticator = authenticator)

    # 性格分析結果をprofileに格納
    profile = service.profile(
        profile_text,
        accept = 'application/json',
        content_type = 'text/plain;charset=utf-8',
        content_language = lang,
        accept_language = 'ja',
        raw_scores = True).get_result()

    return profile


# 性格分析結果をstr型にしつつ整形する
def do_dump(profile):
    import json

    dumped_profile = json.dumps(profile, indent=4, ensure_ascii=False)

    return dumped_profile


# Big5とそのファセットについて、百分率値のベクトルを得る
def get_vector(profile):
    import re

    #keys =   [key   for key   in re.findall('"trait_id": "([^"]*)'  , profile)]
    vector = [value for value in re.findall('"percentile": ([^,]*),', profile)]
    labels = [label for label in re.findall('"name": "([^"]*)'      , profile)]

    return vector, labels


# percentile値の変化を出力
def print_percentile(v1, v2, keys):
    for i in range(len(v1)):
        print('{}:\n    {} -> {}'.format(keys[i], v1[i], v2[i]))


# 性格の変化を計算し、出力
def print_sub(v1, v2):
    import numpy as np

    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)

    sub = v2 - v1
    print('性格値の変化:\n    {}'.format(sub), end='\n\n')



# from PI import get_percentile_sub as gps
def get_percentile_sub(path1, path2, lang):
    import numpy as np

    profile_text1 = read_file(path1)
    profile1 = do_Personality_Insights(profile_text1, lang)
    profile1 = do_dump(profile1)
    v1, labels = get_vector(profile1)

    profile_text2 = read_file(path2)
    profile2 = do_Personality_Insights(profile_text2, lang)
    profile2 = do_dump(profile2)
    v2, labels2 = get_vector(profile2)

    v1 = np.array(v1, dtype=float)
    v2 = np.array(v2, dtype=float)
    sub = v2 - v1

    return sub



def for_powershell():
    print('path1   = ', end='')
    path1 = input()
    print('path2   = ', end='')
    path2 = input()
    print('\n=====option=====')
    print('入力ファイルの言語は？   (ja/en): ', end='')
    lang  = input()
    print('percentile値を出力する？ (y/n)  : ', end='')
    Is_print_percentile = input()

    profile_text1 = read_file(path1)
    profile1 = do_Personality_Insights(profile_text1, lang)
    profile1 = do_dump(profile1)
    v1, labels = get_vector(profile1)

    profile_text2 = read_file(path2)
    profile2 = do_Personality_Insights(profile_text2, lang)
    profile2 = do_dump(profile2)
    v2, labels2 = get_vector(profile2)

    print('\n')
    if Is_print_percentile == 'y':
        print_percentile(v1, v2, labels)
        print()
    print_sub(v1, v2)



if __name__ == '__main__':
    for_powershell()
