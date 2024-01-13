# Flask를 통한 소설 랭킹 서비스

---

**프로젝트 기간:** 2023.08.29 ~ 2023.09.12 (2주)

**프로젝트 도구:** Flask, MySQL, Github

**사용 언어:** Python, SQL

---

### ****프로젝트 개요****

- 소설의 상위 순위 리스트를 웹으로 간편하게 볼 수 있는 서비스 구축

### 프로젝트 배경

- 기존의 랭킹 서비스는 일정시간 동안의 인기를 추산해서 랭킹으로 서비스로 보여줌
- 가장 인기 있던 소설의 리스트를 볼 수 있는 서비스가 존재하지 않았기에 랭킹을 보여줄 수 있는 서비스를 만들기로 함

### 프로젝트 아키텍쳐
<img width="793" alt="데이터 엔지니어링 아키텍쳐" src="https://github.com/s2lky/Munpia/assets/132236456/551d8ae1-dd5a-406b-95d9-7f754289809e">

### 프로젝트 기술 스택

- **Backend/Frontend**
    
    ![Flask](https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white)
    
- **Database**
    
    ![MySQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
    
- **Tools**
    
    ![github](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white)
    

**Flask 선택 이유**

- 간단하게 front/back을 파이썬으로 구현 가능

### 프로젝트 진행 과정

1. 크롤러 개발
2. AWS EC2를 통한 크롤링 및 DB 적재
3. Flask를 통해 DB와의 통신으로 유저에게 소설 데이터 제공

### 프로젝트 구현 내용

1. 크롤러 개발 및 DB 구축
2. FLASK를 통한 USER와의 통신
![Flask1](https://github.com/s2lky/Munpia/assets/132236456/34e44d19-07fa-4282-9a51-b53d6c8de258)
![Flask2](https://github.com/s2lky/Munpia/assets/132236456/9c714ba4-9248-4267-ae6e-a7bd276788b6)

### 프로젝트 한계 및 개선 방안

**한계**

- Airflow로 주기적으로 데이터를 스크래핑해오도록 구현하려 하였지만 로컬 standalone 상태의 Airflow에서 selenium 작동 오류로 구현하지 못함
- selenium의 높은 리소스 점유율과, 속도 문제

**개선 방안**

- requests와 bs4, 그리고 멀티 프로세싱을 활용한 코드 개선으로 속도 개선 및 리소스 사용량 최소화
- Airflow를 통한 데이터 스크래핑 자동화
