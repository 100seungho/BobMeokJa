import scrapy, datetime
from .menu import Menu


class MenuSpider(scrapy.Spider):
    name = "menus" # unique name

    def start_requests(self):
        dt = datetime.datetime.now()

        counter = 0
        urls = []

        while counter < 7:
            urls.append(f'http://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1[value][date]=&field_menu_date_value[value][date]={dt.strftime("%m/%d/%Y")}')
            dt += datetime.timedelta(days=1)
            counter += 1

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
                    breakfast = menus[index].new_menu(breakfast, 'breakfast')
                    
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
                    menus[index].new_menu_dure(lunch[1], "lunch")

                if dinner is not None:
                    menus[index].new_menu_dure(dinner[1], "dinner")
                
        
        for menu in menus:
            for _menu in menu.menus:
                yield {'restaurant_name': _menu['restaurant_name'],
                    'restaurant_tel' : _menu['restaurant_tel'],
                    'name' : _menu['name'],
                    'price' : _menu['price'],
                    'no_pork' : _menu['no_pork'],
                    'is_vege' : _menu['is_vege'],
                    'is_halal' : _menu['is_halal'],
                    'date' : _menu['date'],
                    'time_for' : _menu['time_for'],
                }
            # yield {
            #     "date": menu.menus[0]['date'],
            #     "restaurant": menu.menus[0]['restaurant_name'],
            #     "menu": menu.menus
            #     # menu.name: menu.menus
            # }