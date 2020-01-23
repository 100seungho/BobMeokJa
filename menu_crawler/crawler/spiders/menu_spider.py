import scrapy, datetime, html
from ..items import MealItem


class MenuSpider(scrapy.Spider):
    name = "menus" # unique name

    def start_requests(self):
        dt = datetime.datetime.now()

        counter = 0
        urls = []

        urls.append(f'http://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1[value][date]=&field_menu_date_value[value][date]=01/22/2020')

        # while counter < 7:
        #     urls.append(f'http://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1[value][date]=&field_menu_date_value[value][date]={dt.strftime("%m/%d/%Y")}')
        #     dt += datetime.timedelta(days=1)
        #     counter += 1

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        date_raw = response.url.split("=")[-1]
        handled_date = date_raw.split("/")
        date = {}
        date['month'] = handled_date[0]
        date['day'] = handled_date[1]
        date['year'] = handled_date[2]

        def save_html():
            # html을 저장하는 함수. 딱히 필요 없다. (안 씀)

            filename = f"{concatenate('menus', date['month'], date['day'], date['year'], seperator = '-')}.html"
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)

        class Menu:
            def __init__(self, name, date):
                self.menus = []
                self.is_open = True
                self.name = name
                self.date = date

            def new_menu(self, meal_name, time_for):
                menu = {}
                
                name_tel = self.parse_restaurant(self.name)
                menu['restaurant_name'] = name_tel[0]
                menu['restaurant_tel'] = name_tel[1]
                
                name_price = self.parse_name_price(meal_name)
                
                menu['name'] = name_price[0]
                menu['price'] = name_price[1]
                
                menu['name'] = self.remove_xa0(menu['name'])
                menu['name'] = html.unescape(menu['name'])
                
                # check vegan
                if self.no_pork(menu['name']):
                    menu['no_pork'] = True
                    menu['is_vege'] = False
                    menu['is_halal'] = False
                    menu['name'] = menu['name'].replace('(#)', '')
                    
                elif self.is_vege(menu['name']):
                    menu['is_vege'] = True
                    menu['no_pork'] = False
                    menu['is_halal'] = False
                    menu['name'] = menu['name'].replace('(채식)', '')
                    
                elif self.is_halal(menu['name']):
                    menu['is_halal'] = True
                    menu['is_vege'] = False
                    menu['no_pork'] = False
                    menu['name'] = menu['name'].replace('(HALAL)', '')
                
                else:
                    menu['no_pork'] = False
                    menu['is_vege'] = False
                    menu['is_halal'] = False
                
                menu['date'] = f"{self.date['month']}/{self.date['day']}/{self.date['year']}"
                menu['time_for'] = time_for

                self.menus.append(menu)
                
            def new_menu_301(self, meal_name):
                menu = {}
                
                name_tel = self.parse_restaurant(self.name)
                menu['restaurant_name'] = name_tel[0]
                menu['restaurant_tel'] = name_tel[1]
                
                menu['name'] = meal_name
                menu['price'] = "6,000원"
                
                menu['name'] = self.remove_xa0(menu['name'])
                menu['name'] = html.unescape(menu['name'])
                
                menu['no_pork'] = False
                menu['is_vege'] = False
                menu['is_halal'] = False
                
                menu['date'] = f"{self.date['month']}/{self.date['day']}/{self.date['year']}"
                menu['time_for'] = "lunch"
                
                self.menus.append(menu)
            
            def new_menu_301_2(self, main_meal, side_meal):
                menu = {}
                
                name_tel = self.parse_restaurant(self.name)
                menu['restaurant_name'] = name_tel[0]
                menu['restaurant_tel'] = name_tel[1]
                
                menu['name'] = f"{main_meal}({side_meal})"
                menu['price'] = "5,500원"
                
                menu['name'] = self.remove_xa0(menu['name'])
                menu['name'] = html.unescape(menu['name'])
                
                menu['no_pork'] = False
                menu['is_vege'] = False
                menu['is_halal'] = False
                
                menu['date'] = f"{self.date['month']}/{self.date['day']}/{self.date['year']}"
                menu['time_for'] = "lunch"
                
                self.menus.append(menu)

            def new_menu_dure(self, meal_name, time_for):
                menu = {}
                
                name_tel = self.parse_restaurant(self.name)
                menu['restaurant_name'] = name_tel[0]
                menu['restaurant_tel'] = name_tel[1]
                
                menu['name'] = meal_name
                menu['price'] = "6,000원"
                
                menu['name'] = self.remove_xa0(menu['name'])
                menu['name'] = html.unescape(menu['name'])
                
                menu['no_pork'] = False
                menu['is_vege'] = False
                menu['is_halal'] = False
                
                menu['date'] = f"{self.date['month']}/{self.date['day']}/{self.date['year']}"
                menu['time_for'] = time_for
                
                self.menus.append(menu)
            
            @staticmethod
            def parse_restaurant(restaurant):
                # resaurant 이름이 처음에 아래 주석같이 나온다. 그래서 이 함수로 레스토랑 이름을 파싱한다.
                # '\n            학생회관식당(880-5543)          '
                restaurant = restaurant.replace('\n            ', '') # '학생회관식당(880-5543)          '
                restaurant = restaurant.replace(')          ', '') # '학생회관식당(880-5543'
                restaurant_name = restaurant[:-9] # 학생회관식당
                restaurant_tel = f"02-{restaurant[-8:]}" # 02-880-5543
                return restaurant_name, restaurant_tel
            
            @staticmethod
            def remove_xa0(string):
                string = string.replace('\xa0', '')
                string = string.replace('\n', '')
                return string
            
            @staticmethod
            def parse_name_price(string):
                name = string[:-7]
                price = string[-6:]
                return (name, price)
            
            @staticmethod
            def no_pork(string):
                if '(#)' in string:
                    return True
                else:
                    return False
                
            @staticmethod
            def is_vege(string):
                if '(채식)' in string:
                    return True
                else:
                    return False
                
            @staticmethod
            def is_halal(string):
                if '(HALAL)' in string:
                    return True
                else:
                    return False
            
        menu_by_restaurant = response.css("tbody tr")

        menus = []

        for table_row in menu_by_restaurant:
            restaurant = table_row.css("td.views-field-field-restaurant::text").get()
            
            if "학생회관" in restaurant or "자하연" in restaurant or "예술계" in restaurant or "동원관" in restaurant or "기숙사" in restaurant or "감골" in restaurant or "3식당" in restaurant or "302동" in restaurant or "220동" in restaurant or "4식당" in restaurant:
            # if "5543" or "7888" or "1006" or "8697" or "9072" or "5544" or "5545" or "1939" or "0240" or "6946" in restaurant:
                menus.append(Menu(restaurant, date))
                index = len(menus) - 1

                breakfast = table_row.css("td.views-field-field-breakfast p::text").get()
                lunch = table_row.css("td.views-field-field-lunch p::text").getall()
                dinner = table_row.css("td.views-field-field-dinner p::text").getall()

                if breakfast is not None:
                    menus[index].new_menu(breakfast, 'breakfast')
                    
                if lunch is not None:
                    for menu in lunch:
                        if len(menu) > 5: # 4식당의 공백을 제거하기 위해서 있는 조건.
                            menus[index].new_menu(menu, 'lunch')
                            
                if dinner is not None:
                    for menu in dinner:
                        if len(menu) > 5: # 4식당의 공백을 제거하기 위해서 있는 조건.
                            menus[index].new_menu(menu, 'dinner')
            
            if "301동" in restaurant:
            # if "8955" in restaurant:
                menus.append(Menu(restaurant, date))
                index = len(menus) - 1

                lunch = table_row.css("td.views-field-field-lunch p::text").getall()
                
                if lunch is not None:
                    menus[index].new_menu_301(lunch[11])
                    menus[index].new_menu_301_2(lunch[13], lunch[14])

            if "두레미담" in restaurant:
                menus.append(Menu(restaurant, date))
                index = len(menus) - 1

                lunch = table_row.css("td.views-field-field-lunch p::text").getall()
                dinner = table_row.css("td.views-field-field-dinner p::text").getall()

                if lunch is not None:
                    menus[index].new_menu_dure(lunch[1], "lunch"

                if dinner is not None:
                    menus[index].new_menu_dure(dinner[1], "dinner")
                
        
        for menu in menus:
            yield {
                menu.menus[0]['restaurant_name']: menu.menus
                # menu.name: menu.menus
            }
            