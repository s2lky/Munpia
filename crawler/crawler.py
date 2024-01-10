from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import pandas as pd
import time
import requests
from datetime import datetime, timedelta
import mysql.connector
import pytz

from selenium.webdriver.chrome.options import Options

# 헤드리스 모드 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 헤드리스 모드로 실행

now = datetime.now()
formatted_datetime = now.strftime("%Y-%m-%d %H:%M")
scrape_time = now.strftime("%Y-%m-%d")
that_time = now.strftime("%Y_%m_%d")


db_config = {
        "host": "3.35.53.188",
        "user": "team15",
        "password": "1234",
        "database": "munpia_db"
        }


data = pd.read_csv('./primary.csv')
data = data['series_id'].to_list()
def scrape_website():
    driver = Chrome(options=chrome_options)
    count = 0
    data_list = []

    for i in data:
        print(i)
        driver.get(f'https://novel.munpia.com/{i}')
        try:
            driver.find_element(By.CLASS_NAME, 'pagination')
            series_id = ((driver.find_element(By.CLASS_NAME, 'dd').find_element(By.TAG_NAME, 'a').get_attribute('href')).split('.com/'))[1]
            title = driver.find_element(By.CLASS_NAME, 'dd').find_element(By.TAG_NAME, 'a').get_attribute('title')
            try:
                author = driver.find_element(By.CLASS_NAME, 'member-trigger').find_element(By.TAG_NAME, 'strong').text
            except:
                author = driver.find_element(By.CLASS_NAME, 'meta-author').find_element(By.TAG_NAME, 'dd').text
            genre = driver.find_element(By.CLASS_NAME, 'meta-path').find_element(By.TAG_NAME, 'strong').text
            series_info = (driver.find_elements(By.CLASS_NAME, 'meta-etc'))[1].find_elements(By.TAG_NAME, 'dd')
            total_series = int((((series_info[0].text).split(' '))[0]).replace(',', ''))
            total_view = int((series_info[1].text).replace(',', ''))
            total_recommend = int((series_info[2].text).replace(',', ''))
            total_text = int((series_info[3].text).replace(',', ''))
            prefer = int((driver.find_element(By.CLASS_NAME, 'fr').find_element(By.TAG_NAME, 'b').text).replace(',', ''))
            data_list.append({'series_id': series_id, 'title': title, 'author': author, 'genre': genre, 'total_series': total_series, 'total_view': total_view,
                            'total_recommend': total_recommend, 'total_text': total_text, 'prefer': prefer, 'scraped_time': scrape_time})
        except:
            count+=1
    df_data_list = pd.DataFrame(data_list)
    df_data_list.to_csv('./data', index=False)
    driver.quit()
    return df_data_list

def create_table():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = f"CREATE TABLE IF NOT EXISTS munpia_db.series_total_data_{that_time} (\
        series_id INT NOT NULL,\
        title VARCHAR(100) NULL DEFAULT NULL,\
        author_name VARCHAR(100) NULL DEFAULT NULL,\
        genre VARCHAR(100) NULL DEFAULT NULL,\
        total_series INT NULL DEFAULT NULL,\
        total_view INT NULL DEFAULT NULL,\
        total_recommend INT NULL DEFAULT NULL,\
        total_text INT NULL DEFAULT NULL,\
        prefer INT NULL DEFAULT NULL,\
        scraped_time TIMESTAMP NULL,\
        INDEX seires_total_data_series_id_idx (series_id ASC) VISIBLE,\
        CONSTRAINT seires_total_data_series_id_{that_time}\
        FOREIGN KEY (series_id)\
        REFERENCES munpia_db.primary (series_id))"
        
    cursor.execute(query)
    cursor.close()
    conn.close()


def insert_id_data_into_mysql(df_data_list):
    count = 0
    series_count = 0
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    data_to_insert = df_data_list
    insert_query = "INSERT INTO munpia_db.primary(series_id) VALUES (%s)"
    for index, row in data_to_insert.iterrows():
        series_count += 1
        try:
            values = (row['series_id'],)
            cursor.execute(insert_query, values)
            conn.commit()
        except:
            count += 1
    print(f"전체 작품 {series_count}개 중에 같은 primary key {count}개가 이미 존재합니다.")
    cursor.close()
    conn.close()
def insert_series_data_into_mysql(df_data_list):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    data_to_insert = df_data_list
    insert_query = f"INSERT INTO munpia_db.series_total_data_{that_time}(series_id, title, author_name, genre, total_series, total_view, total_recommend, total_text, prefer, scraped_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    for index, row in data_to_insert.iterrows():
        values = (row['series_id'], row['title'], row['author'], row['genre'], row['total_series'], row['total_view'], row['total_recommend'], row['total_text'], row['prefer'], row['scraped_time'])
        cursor.execute(insert_query, values)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    scrape_website()
    create_table()
    insert_id_data_into_mysql(df_data_list)
    insert_series_data_into_mysql(df_data_list)

