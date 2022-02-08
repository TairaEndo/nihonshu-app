import os, json

# %%
import pandas as pd
import numpy as np
import sympy


def recommend(taste, flavor, taste_flavor, taste_popularity, flavor_popularity):
    df = pd.read_csv("./data/日本酒_重み付け数値.csv", encoding="UTF-8")

    a1 = int(taste)  # 味(a1)　　濃い=1 淡い=2
    a2 = int(flavor)  # 香り(a2)　高い=1 控えめ=2

    list = [["左の項目がとても重要", 5], ["左の項目が重要", 3], ["同じくらい重要", 1],
            ["右の項目が若干重要", 0.33], ["右の項目がとても重要", 0.2]]

    # 番号に変換して表示
    # for i in range(len(list)):
    #     print("%s：%s" % (i, list[i][0]))

    # 味：香り
    put1 = int(taste_flavor)
    x = float(list[put1][1])

    # 味：人気度
    put2 = int(taste_popularity)
    y = float(list[put2][1])

    # 香り：人気度
    put3 = int(flavor_popularity)
    z = float(list[put3][1])

    # 一対比較表②
    eval_mat_0 = np.array([[1, x, y],
                           [1 / x, 1, z],
                           [1 / y, 1 / z, 1]])

    # それぞれの幾何平均
    t1 = sympy.root(x * y, 3)
    t2 = sympy.root((1 / x) * z, 3)
    t3 = sympy.root((1 / y) * (1 / z), 3)
    t_sum = (t1 + t2 + t3)

    # それぞれの重要度
    j1 = t1 / t_sum
    j2 = t2 / t_sum
    j3 = t3 / t_sum

    if a1 == 1 and a2 == 1:  # 第1象限

        # 第1象限のデータだけ抽出
        df1 = df.iloc[0:9]

        df1['recommend_value'] = df1['taste'] * j1 + df1['flavor'] * j2 + df1['popularity'] * j3

        # 並べ替え
        df1s = df1.sort_values('recommend_value', ascending=False)

        # 上位3つをおすすめとして表示
        return df1s[['name', 'category', 'brewery', 'place']].head(3).to_dict(orient='records')

    if a1 == 1 and a2 == 2:  # 第2象限
        df2 = df.iloc[10:13]
        df2['recommend_value'] = df2['taste'] * j1 + df2['flavor'] * j2 + df2['popularity'] * j3
        df2s = df2.sort_values('recommend_value', ascending=False)
        return df2s[['name', 'category', 'brewery', 'place']].head(3).to_dict(orient='records')

    if a1 == 2 and a2 == 1:  # 第3象限
        df3 = df.iloc[14:18]
        df3['recommend_value'] = df3['taste'] * j1 + df3['flavor'] * j2 + df3['popularity'] * j3
        df3s = df3.sort_values('recommend_value', ascending=False)
        return df3s[['name', 'category', 'brewery', 'place']].head(3).to_dict(orient='records')

    else:  # 第4象限
        df4s = df.iloc[19]
        return [df4s[['name', 'category', 'brewery', 'place']].to_dict()]  # .head(1).to_dict(orient='records')
