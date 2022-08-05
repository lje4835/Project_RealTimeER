import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
import pymysql

# 실시간 병상정보 API 가져오기
url1 = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEmrrmRltmUsefulSckbdInfoInqire'
# 병원 경도, 위도 API 가져오기
url2 = 'http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire'
# 시도군구 csv 가져오기
sido = pd.read_csv('sido_sgg.csv')


# 실시간 병상정보 데이터 수집
raw_datas = []
for idx in range(len(sido)):
    params ={'serviceKey' : 'NCZ+NI8mrfXKXXrBb77GRgsWoPCFIa4jtsTfyyKEJ1PndLHBrAgPPymdrlBC2h3vwatIJMrrbacHcjb9o3JsjA==', 'STAGE1' : sido.iloc[idx].values[0], 'STAGE2' : sido.iloc[idx].values[1]}
    response = requests.get(url1, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)

    def get_data(name): # get_data 함수 정의하기
        all = []
        items = soup.find_all('item') # <item> 으로 구획짓기
        for idx1 in range(len(items)):
            if items[idx1].find(name) != None:
                one = items[idx1].find(name).string
            else:
                one = "없음"
            all.append(one)
        return all

    def get_date(name):
        all = []
        items = soup.find_all('item')
        for idx1 in range(len(items)):
            if items[idx1].find(name) != None:
                one = items[idx1].find(name).string
                new_one = one[:4] + '-' + one[4:6] + '-' + one[6:8] + ' ' + one[8:10] + ':' + one[10:12] + ':' + one[12:]
            else:
                new_one = "없음"
            all.append(new_one)
        return all

    all_rows = []
    items = soup.find_all('item')
    for idx2 in range(len(items)):
        row = [sido.iloc[idx].values[0], sido.iloc[idx].values[1], get_date('hvidate')[idx2], get_data('dutyname')[idx2], get_data('dutytel3')[idx2], int(get_data('hvec')[idx2]), int(get_data('hvoc')[idx2]), get_data('hvctayn')[idx2], get_data('hvmriayn')[idx2], get_data('hvventiayn')[idx2], int(get_data('hvicc')[idx2]), int(get_data('hvccc')[idx2])]
        all_rows.append(row)

    for idx3 in range(len(all_rows)):
        raw_datas.append(all_rows[idx3])

all_datas = []
for v in raw_datas:
    if v not in all_datas:
        all_datas.append(v)

hp_list = ['의료법인 양진의료재단 평택성모병원', '(의)영문의료재단 다보스병원', '의료법인 나사렛의료재단 나사렛국제병원', '가톨릭대학교 인천성모병원', '의료법인행촌의료재단 해남종합병원', '의료법인행복나눔의료재단 장성병원', '전라북도 남원의료원', '의료법인 중앙의료재단 중앙병원', '학교법인 춘해병원', '의료법인 인당의료재단 부민병원', '경상북도 포항의료원', '영남대학교의과대학부속 영천병원', '의료법인영제의료재단 영남제일병원', '근로복지공단 창원병원', '의료법인 성념의료재단맑은샘병원', '의료법인 동해동인병원', '의료법인 성심의료재단 양구성심병원']
for data in all_datas:
    if data[3] in hp_list:
        all_datas.remove(data)

new_datas = []
id = 0
for i in range(len(all_datas)):
    id += 1
    all_datas[i].append(id)
    new_datas.append(all_datas[i])

# print(new_datas)
# print(len(new_datas))

# id, 시도, 시군구, 입력일시, 기관명, 기관코드, 응급실 직통전화번호, 응급실 가용병상, 수술실 가용병상,
# CT 가용여부, MRI 가용여부, 인공호흡기 가용여부, 일반중환자실 가용병상, 흉부중환자실 가용병상


# # 병원 위치 데이터 수집
# raw_datas_region = []
# for idx in range(len(new_datas)):
#     params ={'serviceKey' : 'NCZ+NI8mrfXKXXrBb77GRgsWoPCFIa4jtsTfyyKEJ1PndLHBrAgPPymdrlBC2h3vwatIJMrrbacHcjb9o3JsjA==', 'QN' : new_datas[idx][3]}
#     response = requests.get(url2, params=params)
#     soup = BeautifulSoup(response.text, "html.parser")
#     # print(soup)
    
#     row = [new_datas[idx][3], get_data('dutyaddr')[0], float(get_data('wgs84lat')[0]), float(get_data('wgs84lon')[0]), new_datas[idx][-1]]
#     raw_datas_region.append(row)

# all_datas_region = []
# for v in raw_datas_region:
#     if v not in all_datas_region:
#         all_datas_region.append(v)

# print(all_datas_region)
# print(len(all_datas_region))

# 기관코드, 기관명, 주소, 위도, 경도
# print(len(all_datas_region))

#if len(new_datas) == len(all_datas_region) :
#    print("데이터 수집 성공!")


# machine learning data 가져오기
df = pd.read_csv('heart.csv')
df = df.drop_duplicates().reset_index(drop=True).reset_index()
df['index'] = df['index'] + 1
df = df.drop(columns=['exng', 'oldpeak', 'slp', 'caa', 'thall'])

# print(df)


# 실시간 병상 정보 API 스케줄링하여 DB 저장하기
# DB_FILENAME = 'Project.db'
# DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='jieun4835', db='project1', charset='utf8')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS LOC_table;")
cur.execute("DROP TABLE IF EXISTS ER_table;")

sql = """CREATE TABLE IF NOT EXISTS ER_table(
    Sido VARCHAR(50),
    Sigungu VARCHAR(50),
    Datetime DATETIME,
    Hpname VARCHAR(200), 
    Ercall VARCHAR(50),
    Erwards INT,
    Orwards INT,
    Ct VARCHAR(10),
    Mri VARCHAR(10),
    Vent VARCHAR(10),
    Icuwards INT,
    Ccuwards INT,
    Er_Id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY(Er_Id));
    """
cur.execute(sql)

sql = """INSERT INTO ER_table (
        Sido, Sigungu, Datetime, Hpname, Ercall, Erwards, Orwards, Ct, Mri, Vent, Icuwards, Ccuwards, Er_Id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
for data in new_datas:
    cur.execute(sql, data)

# 병원 위치 API DB 저장하기
# sql = "CREATE TABLE IF NOT EXISTS LOC_table (Hpname VARCHAR(200), Hpaddr VARCHAR(300), Hplat FLOAT, Hplon FLOAT, Loc_Id INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(Loc_Id), FOREIGN KEY(Loc_Id) REFERENCES ER_table(Er_Id));"
# cur.execute(sql)

# sql = "INSERT INTO LOC_table (Hpname, Hpaddr, Hplat, Hplon, Loc_Id) VALUES (%s, %s, %s, %s, %s);"
# for data in all_datas_region:
#     cur.execute(sql, data)

# machine learning csv DB 저장하기
cur.execute("DROP TABLE IF EXISTS HEART_table;")

sql = """CREATE TABLE IF NOT EXISTS HEART_table (
    Heart_Id INT NOT NULL AUTO_INCREMENT,
    Age INT NOT NULL,
    Sex INT NOT NULL,
    Cp INT NOT NULL,
    Trtbps INT NOT NULL,
    Chol INT NOT NULL,
    Fbs INT NOT NULL,	 
    Restecg INT NOT NULL,	
    Thalachh INT NOT NULL,
    Output INT,
    PRIMARY KEY(Heart_Id)
);"""
cur.execute(sql)

for idx, row in df.iterrows():
    cur.execute("INSERT INTO HEART_table (Heart_Id, Age, Sex, Cp, Trtbps, Chol, Fbs, Restecg, Thalachh, Output) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", list(row.values))


conn.commit()
cur.close()
conn.close()