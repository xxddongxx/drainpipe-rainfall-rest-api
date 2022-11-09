# :umbrella::droplet: Drainpipe Rainfall REST API Service
랩큐 Open API 방식의 공공 데이터를 수집, 가공하여 REST API 개발

# :bookmark_tabs: 목차
* [Drainpipe Raiinfall](#Drainpipe-Rainfall-REST-API)
  * [목차](#목차)
  * [프로젝트 요구사항](#프로젝트-요구사항)
  * [API Docs](#api-docs)


# :clipboard: 프로젝트 요구사항
1. 서울시 하수관로 수위 현황과 강우량 정보 데이터를 결합
2. 출력값 중 GUBN_NAM과 GU_NAME 기준으로 데이터를 결합
3. 데이터는 JSON으로 전달

# :books: API Docs
## 현황 조회
> Method: GET<br>
URL: /api/v1/drainpiperainfall/latest/?gu_name="구이름"
Description: 구이름으로 조회된 하수관로 수위, 강우량 최신 데이터 조회
* Response
```json
"message": "Success",
"status": 200,
"result": {
    "Drain_Pipe": [
        {
            "IDN": "03-0005",
            "GUBN": "03",
            "GUBN_NAM": "용산",
            "MEA_YMD": "2022-11-09 15:23:00.0",
            "MEA_WAL": "0.41",
            "SIG_STA": "통신양호",
            "REMARK": "서울특별시 용산구 문배동 24-21 용산아크로 타워 아파트 102동 201동 사이 도로에 위치"
        },
        .
        .
        .
        {
            "IDN": "03-0007",
            "GUBN": "03",
            "GUBN_NAM": "용산",
            "MEA_YMD": "2022-11-09 15:23:00.0",
            "MEA_WAL": "0.04",
            "SIG_STA": "통신양호",
            "REMARK": "서울특별시 용산구 청파3동 73-2"
        },
    ],
    "RainFall": [
        {
            "RAINGAUGE_CODE": "1601.0",
            "RAINGAUGE_NAME": "용산구청",
            "GU_CODE": "116.0",
            "GU_NAME": "용산구",
            "RAINFALL10": "0",
            "RECEIVE_TIME": "2022-11-09 15:19"
        },
        {
            "RAINGAUGE_CODE": "1602.0",
            "RAINGAUGE_NAME": "한남P",
            "GU_CODE": "116.0",
            "GU_NAME": "용산구",
            "RAINFALL10": "0",
            "RECEIVE_TIME": "2022-11-09 15:19"
        }
    ]
}
}
```