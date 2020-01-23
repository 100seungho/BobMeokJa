from flask import Flask, jsonify, request
# from bs4 import BeautifulSoup
# import urllib.request, urllib.parse, datetime

# class Crawler:
#     def __init__(self):
#         pass

#     def crawl_request():
#         dt = datetime.datetime.now()

#         counter = 0
#         urls = []

#         while counter < 7:
#             urls.append(f"http://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1[value][date]=&field_menu_date_value[value][date]={dt.strftime("%m/%d/%Y")}")
#             dt += datetime.timedelta(days=1)
#             counter += 1

#         for url in urls:
#             with urllib.request.urlopen(url) as response:
#             html = response.read()
#             soup = BeautifulSoup(html, 'html.parser')

#             table = soup.find(class_ = 'views-table cols-4')

        

app = Flask(__name__)
class Restaurant:
    class _Menu:
        def __init__(self, name: str, price: int, time_for: str, date: str, is_vegan: bool):
            self.name = name
            self.price = price
            self.time_for = time_for
            self.date = date
            self.is_vegan = True
        
        def __str__(self):
            return f"""
            name: {self.name}
            price: {self.price}
            time_for: {self.time_for}
            date: {self.date}
            is_vegan: {self.is_vegan}
            """

    def __init__(self, name, is_open):
        self.name = name
        self.is_open = True
        self.menus = []
        self.menu_count = 0

    def __str__(self):
        return f"""
        name: {self.name}
        is_open: {self.is_open}
        menu_count: {self.menu_count}
        """

    def menu_is(self):
        for menu in self.menus:
            print(menu)

    def add_menu(self, name: str, price: int, time_for: str, date: str, is_vegan: bool):
        menu = self._Menu(name, price, time_for, date, is_vegan)
        self.menu_count += 1
        return self.menus.append(menu)

today = []
dormitory = Restaurant("기숙사 식당", True)
dormitory.add_menu("쇠고기 된장찌개", 1500, "breakfast", "2020-01-11", False)
print(dormitory)
dormitory.menu_is()

@app.route('/today')
def get_today_menu():
    return jsonify({'today': today})
# meals = [
#     "기숙사식당": {
#         "is_open": "true",
#         "meal": [
#             {
#                 "name": "쇠고기 된장찌개",
#                 "price": 1500,
#                 "time_for": "breakfast",
#                 "date": "2020-01-11"
#                 "is_vegan": true
#             }, {
#                 "name": "시나몬 스테이크",
#                 "price": 2500,
#                 "time_for": "lunch",
#                 "date": "2020-01-11",
#                 "is_vegan": "true"
#             }
#         ]
#     }, "동원관": {

#     }
# ]

app.run(port=6000)