# :umbrella::droplet: Drainpipe Rainfall REST API Service
랩큐 Open API 방식의 공공 데이터를 수집, 가공하여 REST API 개발

# :bookmark_tabs: 목차
* [Drainpipe Raiinfall](#umbrelladroplet-drainpipe-rainfall-rest-api-service)
  * [목차](#bookmark_tabs-목차)
  * [프로젝트 요구사항](#clipboard-프로젝트-요구사항)
  * [API Docs](#books-api-docs)
    * [현황 조회](#현황-조회)
  * [추가 구현](#추가-구현)
    * [강우량 현재까지](#강우량-00시--현-시간-까지-조회)
    * [하수관 수위 현재까지](#하수관-00시--현-시간-까지-조회)


# :clipboard: 프로젝트 요구사항
1. 서울시 하수관로 수위 현황과 강우량 정보 데이터를 결합
2. 출력값 중 GUBN_NAM과 GU_NAME 기준으로 데이터를 결합
3. 데이터는 JSON으로 전달

# :books: API Docs

## 현황 조회
> Method: GET<br>
URL: /api/v1/drainpiperainfall/latest/?gu_name="구이름"<br>
Description: 구이름으로 조회된 하수관로 수위, 강우량 최신 데이터 조회

* Response
```json
}
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

# 추가 구현
## 강우량 00시 ~ 현 시간 까지 조회
> Method: GET<br>
URL: /api/v1/drainpiperainfall/rainfall/today/?gu_name="구이름"<br>
Description: 구이름으로 조회된 강우량 00시 ~ 현 시간 까지의 데이터 조회

* Response
```json
}
    "message": "Success",
    "status": 200,
    "result": {
        "total_count": 272,
        "RainFall": [
            {
                "RAINGAUGE_CODE": "2101.0",
                "RAINGAUGE_NAME": "동작구청",
                "GU_CODE": "121.0",
                "GU_NAME": "동작구",
                "RAINFALL10": "0",
                "RECEIVE_TIME": "2022-11-10 22:59"
            },
            {
                "RAINGAUGE_CODE": "2102.0",
                "RAINGAUGE_NAME": "흑석P",
                "GU_CODE": "121.0",
                "GU_NAME": "동작구",
                "RAINFALL10": "0",
                "RECEIVE_TIME": "2022-11-10 22:59"
            },
            {
                "RAINGAUGE_CODE": "2102.0",
                "RAINGAUGE_NAME": "흑석P",
                "GU_CODE": "121.0",
                "GU_NAME": "동작구",
                "RAINFALL10": "0",
                "RECEIVE_TIME": "2022-11-10 22:49"
            },
            .
            .
            .
    }
}
```

## 하수관 00시 ~ 현 시간 까지 조회
> Method: GET<br>
URL: /api/v1/drainpiperainfall/drainpipe/today/?gu_name="구이름"<br>
Description: 구이름으로 조회된 하수관 수위 00시 ~ 현 시간 까지의 데이터 조회(**Pagenation 필요**)

* Response
```json
{
    "message": "Success",
    "status": 200,
    "result": {
        "total_count": 5496,
        "Drain_Pipe": [
            {
                "IDN": "01-0004",
                "GUBN": "01",
                "GUBN_NAM": "종로구",
                "MEA_YMD": "2022-11-10 00:00:04.0",
                "MEA_WAL": "0.11",
                "SIG_STA": "통신양호",
                "REMARK": "종로구 세종대로178 뒤 맨홀(KT광화문사옥뒤 자전거보관소앞 종로1길, 미대사관~종로소방서 남측, 중학천 하스박스)"
            },
            {
                "IDN": "01-0003",
                "GUBN": "01",
                "GUBN_NAM": "종로구",
                "MEA_YMD": "2022-11-10 00:00:04.0",
                "MEA_WAL": "0.1",
                "SIG_STA": "통신양호",
                "REMARK": "종로구 자하문로 21 앞 맨홀(영해빌딩앞코너 측구측, 백운동천 하수박스)"
            },
            {
                "IDN": "01-0002",
                "GUBN": "01",
                "GUBN_NAM": "종로구",
                "MEA_YMD": "2022-11-10 00:00:04.0",
                "MEA_WAL": "0.1",
                "SIG_STA": "통신양호",
                "REMARK": "중로구 세종대로 지하189 (세종로지하주차장 6층 천장)"
            },
            {
                "IDN": "01-0001",
                "GUBN": "01",
                "GUBN_NAM": "종로구",
                "MEA_YMD": "2022-11-10 00:00:04.0",
                "MEA_WAL": "0.04",
                "SIG_STA": "통신양호",
                "REMARK": "종로구 새문안로9길 9 앞 맨홀(세븐일레븐앞, 현대해상화재빌딩뒤, 백운동천하수박스)"
            },
            .
            .
            .
    }
}
```