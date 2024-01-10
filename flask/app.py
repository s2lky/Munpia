from flask import Flask, render_template, request
import mysql.connector
app = Flask(__name__)

app.config['MYSQL_HOST'] = 
app.config['MYSQL_USER'] = 
app.config['MYSQL_PASSWORD'] = 
app.config['MYSQL_DB'] = 


mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

# 예제로 사용할 목록
from flask import render_template


@app.route('/')
def index():
    # 여기에서 MySQL에서 데이터를 불러와서 처리하는 로직을 추가합니다.
    # 필터링 기준에 따라 데이터를 가져오고 정렬합니다.

    # 세 개의 필터링 버튼의 목록 (예: 정렬 기준)을 생성합니다.
    filter_options_1 = ['선택 없음', '조회수', '추천수', '선호작수']
    filter_options_2 = ['선택 없음', '퓨전', '판타지', '무협', '현대판타지', '대체역사', '게임', '로맨스', '공포·미스테리',
                        '스포츠','라이트노벨', 'SF', '추리', '전쟁·밀리터리', '일반소설', '시·수필', 
                        '중·단편', '아동소설·동화', '드라마', '연극·시나리오', 'BL', '팬픽·패러디']
    filter_options_3 = [10, 20, 30, 50, 100]
    return render_template('index.html', filter_options_1=filter_options_1, filter_options_2=filter_options_2, filter_options_3=filter_options_3)


@app.route('/filter', methods=['POST'])
def apply_filter():
    filter1 = request.form.get('filter1')
    filter2 = request.form.get('filter2')
    filter3 = request.form.get('filter3')

    
    if filter1 == "조회수":
        query1 = "ORDER BY total_view DESC"
    elif filter1 == "추천수":
        query1 = "ORDER BY total_recommend DESC"
    elif filter1 == "선호작수":
        query1 = "ORDER BY prefer DESC"
    else:
        query1 = ""
    
    if filter2 == "선택 없음":
        query2 = ""
    else:
        query2 = f"WHERE genre LIKE '%{filter2}%'"
    
    final_query = f"SELECT * FROM munpia_db.series_total_data_2023_09_10 {query2} {query1} LIMIT {filter3}"
    cursor = mysql.cursor(dictionary=True)
    cursor.execute(final_query)
    result = cursor.fetchall()
    cursor.close()
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
