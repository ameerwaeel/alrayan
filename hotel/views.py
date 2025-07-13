from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup

class ScrapeLegendOfMoscowView(APIView):
    def get(self, request):
        url = "https://thelegendofmoscow.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a")
            result = []
            for link in links:
                href = link.get("href")
                if href:
                    result.append(href)
            return Response({"links": result})
        else:
            return Response({"error": "Failed to fetch website", "code": response.status_code}, status=500)
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests

class ScrapeRoomsView(APIView):
    def get(self, request):
        # 1. Get user inputs from query params
        check_in = request.query_params.get("checkin")
        check_out = request.query_params.get("checkout")
        adults = request.query_params.get("adults", "2")
        children = request.query_params.get("children", "0")
        rooms = request.query_params.get("rooms", "1")
        promo = request.query_params.get("promo", "")

        # 2. Prepare target URL
        booking_url = f"https://thelegendofmoscow.com/booking/?adults={adults}&children={children}&checkIn={check_in}&checkOut={check_out}&rooms={rooms}&promo={promo}"

        # 3. Send the request
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(booking_url, headers=headers)

        # 4. Parse the response with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # 5. Example: extract all room blocks (you’ll need to inspect the site structure)
        rooms = []
        for room in soup.select('.room-item, .room-type, .room'):  # this selector may change
            title = room.select_one(".room-title, h2, h3")
            price = room.select_one(".room-price, .price")
            rooms.append({
                "title": title.get_text(strip=True) if title else "N/A",
                "price": price.get_text(strip=True) if price else "N/A"
            })

        return Response({
            "booking_url": booking_url,
            "rooms": rooms
        })
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class ScrapeRoomView(APIView):
    def get(self, request):
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')
        adults = request.GET.get('adults', 1)
        children = request.GET.get('children', 0)
        rooms = request.GET.get('rooms', 1)
        promo = request.GET.get('promo', '')

        # تأليف URL بناءً على الداتا اللي دخلت
        url = f"https://thelegendofmoscow.com/booking/?adults={adults}&children={children}&checkIn={checkin}&checkOut={checkout}&rooms={rooms}&promo={promo}"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                # لو عايز تطلع الروابط أو الداتا من الـ HTML
                # soup = BeautifulSoup(response.text, 'html.parser')
                # هنا تقدر تعمل parsing للبيانات

                return Response({
                    "booking_url": url,
                    "status": "success",
                    "html_length": len(response.text)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to fetch booking page"}, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class SubmitRoomSearchView(APIView):
#     def post(self, request):
#         data = request.data
#         checkin = data.get("checkin")
#         checkout = data.get("checkout")
#         adults = data.get("adults")
#         children = data.get("children")
#         rooms = data.get("rooms")
#         promo = data.get("promo")

#         booking_url = f"https://thelegendofmoscow.com/booking/?adults={adults}&children={children}&checkIn={checkin}&checkOut={checkout}&rooms={rooms}&promo={promo}"

#         return Response({
#             "status": "success",
#             "booking_url": booking_url
#         }, status=status.HTTP_200_OK)
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SubmitRoomSearchView(APIView):
    def post(self, request):
        try:
            data = request.data
            checkin = data.get("checkin")
            checkout = data.get("checkout")
            adults = data.get("adults", "2")
            children = data.get("children", "0")
            rooms = data.get("rooms", "1")
            promo = data.get("promo", "")

            checkin_date = datetime.strptime(checkin, "%Y-%m-%d")
            checkout_date = datetime.strptime(checkout, "%Y-%m-%d")
            nights = (checkout_date - checkin_date).days

            booking_url = f"https://thelegendofmoscow.com/en/booking/?date={checkin}&nights={nights}&adults={adults}&children-age=5;11&access-code={promo}"

            # إعداد المتصفح
            options = Options()
            options.add_argument('--headless=new')  # جرب `--headless=new` إذا `--headless` القديمة لا تعمل
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument("--window-size=1920,1080")

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(booking_url)

            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "b-room__item"))
            )

            soup = BeautifulSoup(driver.page_source, "html.parser")

            rooms_data = []
            for room in soup.select(".b-room__item"):
                name = room.select_one(".b-room__title")
                price = room.select_one(".b-room__price")
                rooms_data.append({
                    "name": name.text.strip() if name else "غير محدد",
                    "price": price.text.strip() if price else "غير متوفر"
                })

            driver.quit()

            return Response({
                "status": "success",
                "booking_url": booking_url,
                "rooms": rooms_data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=500)
