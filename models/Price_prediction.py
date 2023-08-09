# pip install pandas
# pip install pycaret

import os
import pandas as pd
from pycaret.regression import load_model
from pycaret.regression import predict_model
# import datetime

# 항공권 가격 예측
# 전처리
'''
모델에 사용되는 feature 추출 과정
'''
def preprocessing(date,airport,direct):
    # 날짜 데이터 타입 변경 (str → date)
    date = pd.to_datetime(date, format='%Y-%m-%d')
    # 월 / 일 분류
    date_Month, date_Day = date.month, date.day
    # 현재 시점으로 부터 3개월 뒤에 여행을 출발하는지 / 3개월 이내에 여행 출발하는지 여부
    target_date = date - pd.DateOffset(months=3)
    three_month = int(date >= target_date)
    # 출국(1 : 인천→파리) 입국(0 : 파리→인천) 여부
    Departure_status = 1 if airport == 'ICN' else  0
    return [date_Month, date_Day, three_month, Departure_status, direct]

# 티켓 가격 예측
'''
    편도 예상 비용은 큰 오차 없어보이지만 왕복 비용의 경우 항공사 내부 지침에 따라 계산 되므로 편도+편도 비용과는 차이가 있음
    따라서 비용 오차가 큼
'''
def predict_ticket(Departure_date, Return_date, Departure_airport, Return_airport, direct_flight):
    # 웹으로 부터 입력 받을 데이터 : Departure_date / Return_date / Departure_airport / Return_airport / direct_flight
    # Departure_date = input("출발 날짜 입력 (YYYY-MM-DD) : ") # 출발 날짜
    # Return_date =  input("복귀 날짜 입력 (YYYY-MM-DD) : ") # 복귀 날짜
    # Departure_airport = input("출발 공항 코드 입력 (ICN) : ") # 출발 공항 코드
    # Return_airport = input("복귀 공항 코드 입력 (CDG) : ") # 복귀 공항 코드
    # three_month =  input("현재 시점으로 3개월 이후의 항공권인가 (0: 3개월 이내 여행출발 / 1: 3개월 이후 여행출발) : ") # 해당 데이터는 웹에서 받아오지 않아도 됨. 전처리 단계에서 추가되는 데이터
    # direct_flight = input("직항인가 (0: 경유/ 1: 직항) : ") # 직항/경유 여부

    # 전처리 실행
    Departure = preprocessing(Departure_date,Departure_airport,direct_flight)
    Return = preprocessing(Return_date,Return_airport,direct_flight)

    # 모델 실행

    columns = ['월', '일', '3개월', '출국여부', '직항여부']
    Data = pd.DataFrame([Departure, Return], columns=columns)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, 'Flight_ML')
    Hotel_model_path = os.path.join(script_dir, 'Hotel_ML')
    Flight_ML = load_model(model_path)
    Hotel_ML = load_model(Hotel_model_path)
    result = predict_model(Flight_ML, data = Data)['prediction_label']

    print('예상 인천 → 파리 항공권 비용 : ',int(result[0])) # 편도 예상 비용 출력 용도
    print('예상 파리 → 인천 항공권 비용 : ',int(result[1])) # 편도 예상 비용 출력 용도
    print('예상 비용 : ', int(sum(result))) # 왕복 예상 비용 출력 용도

    return int(sum(result))

# 호텔 가격 예측
'''
초기에 입력 받은 날짜를 그대로 사용하므로 마지막 줄 'regions'에서 뽑아서 출력하는 것 외에 추가할 작업은 없음
시차를 고려하여 
'''
def predict_hotel(departure_date, return_date):
    # 함수 호출하여 데이터프레임 생성
    hotel_data = hotel_preprocessing(departure_date, return_date)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    hotel_model_path = os.path.join(script_dir, 'Hotel_ML')
    Hotel_ML = load_model(hotel_model_path)
    
    # 지역 별 호텔 가격 예측 
    regions = {}
    for i, region in enumerate(['Louvre', 'Bourse', 'Le Marais', 'Hotel_de_Ville','Latin Quarter', 'Saint-Germain-des-Prés',
    'Invalides','champs-elysees', 'Opera_Paris_Department_France','Paris_Charles_de_Gaulle_Airport']):
        hotel_data['구역'] = i
        hotel_result = predict_model(Hotel_ML, data = hotel_data)['prediction_label']
        regions[region] = int(sum(hotel_result))
    
    # 가격이 낮은 순으로 정렬
    regions = sorted(regions.items(), key=lambda x: x[1])

    # 각 구역별 예측 가격
    # 결과물 출력 형태 : Dictionary
    # 총 10개 구역 (1 ~ 9 구역, 공항)
    # key, value 형태로 결과값 뽑아서 사용
    # print(regions)
    # {'Louvre': 1328356, 'Bourse': 843404, 'Le Marais': 930752, 'Hotel_de_Ville': 851341, 'Latin Quarter': 676807, 'Saint-Germain-des-Prés': 913870, 'Invalides': 810114, 'champs-elysees': 938063, 'Opera_Paris_Department_France': 603958, 'Paris_Charles_de_Gaulle_Airport': 433428}
    
    return regions


# 전처리
def hotel_preprocessing(Start, End):
    # 출발 날짜와 복귀 날짜를 datetime 객체로 변환
    departure_date = pd.to_datetime(Start)
    return_date = pd.to_datetime(End)

    # 날짜 데이터 생성
    dates = pd.date_range(departure_date, return_date - pd.Timedelta(days=1), freq='D')

    # 요일 데이터 생성 (1부터 7까지)
    weekdays = [date.weekday() + 1 for date in dates]

    # 주말 feature 생성 (금요일 또는 토요일인 경우 1, 그 외의 경우 0)
    is_weekend = [1 if weekday in [5, 6] else 0 for weekday in weekdays]

    # 데이터프레임 생성
    df = pd.DataFrame({
        '년': dates.year,
        '월': dates.month,
        '일': dates.day,
        '요일': weekdays,
        '주말': is_weekend
    })

    return df

