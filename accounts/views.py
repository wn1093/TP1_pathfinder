from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from models.Price_prediction import predict_ticket, predict_hotel
from accounts.models import PfAirline

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials...')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken...")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "email taken...")
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, "user created...")
                return redirect('login')
        else:
            messages.info(request, "password not matched...")
            return redirect('register')
        return redirect('/')
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def contact(request):
    return render(request, 'contact.html')

def contactAirline(request):
    departure = request.GET.get('departure')
    arrival = request.GET.get('arrival')
    direct_flight = '직항' if request.GET.get('direct_flight') == '1' else '경유'
    departure_date = request.GET.get('departure_date')
    return_date = request.GET.get('return_date')
    personnel = request.GET.get('personnel')

    # 출발일 기준 항공 목록
    arrive_list = PfAirline.objects.filter(start_airport=departure, arrival_airport=arrival, direct1=direct_flight,
                                            flight_date = departure_date)
    disp_arrive_list = []
    
    for info in arrive_list:
        text = 'Airline : ' + info.airline + ' | Start Airport : ' + info.start_airport + ' | Start Time : ' + str(info.start_time) + ' | Arrival Airport : ' + info.arrival_airport + ' | Arrival Time : ' + str(info.arrival_time)

        disp_arrive_list.append(text)

    # 도착일 기준 항공 목록
    return_list = PfAirline.objects.filter(start_airport=departure, arrival_airport=arrival, direct1=direct_flight,
                                            flight_date = return_date)
    
    disp_return_list = []
    
    for info in return_list:
        text = 'Airline : ' + info.airline + ' | Start Airport : ' + info.start_airport + ' | Start Time : ' + str(info.start_time) + ' | Arrival Airport : ' + info.arrival_airport + ' | Arrival Time : ' + str(info.arrival_time)

        disp_return_list.append(text)
    
    return_value = {}

    # 설정 정보
    return_value['departure'] = departure
    return_value['arrival'] = arrival
    return_value['direct_flight'] = request.GET.get('direct_flight')
    return_value['departure_date'] = departure_date
    return_value['return_date'] = return_date
    return_value['personnel'] = personnel
    return_value['arrive_list'] = disp_arrive_list
    return_value['return_list'] = disp_return_list

    return render(request, 'contact.html', return_value)

def about(request):
    return render(request, 'about.html')

def news(request):
    # 변수 선언
    departure_date = request.GET.get('departure_date')
    return_date = request.GET.get('return_date')
    departure_airport = request.GET.get('departure')
    return_airport = request.GET.get('arrival')
    direct_flight = request.GET.get('direct_flight')

    ticket_price = predict_ticket(departure_date, return_date, departure_airport, return_airport, direct_flight)
    hotel_price = predict_hotel(departure_date, return_date)
    return_value = {}

    # 티켓 가격 셋팅
    return_value['ticketPrice'] = ticket_price

    # 호텔 가격 셋팅
    setting_cnt = 10 if len(hotel_price) > 10 else len(hotel_price)
    for idx in range(0, setting_cnt-1):
        hotel = hotel_price[idx]
        return_value['hotelPrice'+str(idx+1)] = hotel[0] + " : " + str(hotel[1]) + "원"

    return render(request, 'news.html', return_value)

def destinations(request):
    return render(request, 'destinations.html')


