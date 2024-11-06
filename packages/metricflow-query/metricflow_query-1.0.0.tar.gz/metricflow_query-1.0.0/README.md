# metricflow-query

dbt metricflow로 생성한 metric을 쿼리로 관리할 수 있도록 도와주는 라이브러리입니다.

## Installation
1. metricflow-query 라이브러리를 설치해주세요.
    ```bash
    pip3 install git+https://github.com/liner-engineering/metricflow-query.git
    ```
2. `metricflow-query init` 또는 `mq init`을 통해 초기 설정을 해주세요
3. 원하는 metricflow를 이용한 sql 파일에 macro를 import하여 사용해주세요.
