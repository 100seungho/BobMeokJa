import html
from ..items import MealItem

class Menu:
    def __init__(self, name, date):
        self.menus = []
        self.is_open = True
        self.name = name
        self.date = date

    def new_menu(self, meal_name, time_for):
        menu = MealItem()
        
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
        
        menu['date'] = f"{self.date['year']}{self.date['month']}{self.date['day']}"
        menu['time_for'] = time_for

        self.menus.append(menu)
        
        return menu
        
    def new_menu_301(self, meal_name):
        menu = MealItem()
        
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
        
        menu['date'] = f"{self.date['year']}{self.date['month']}{self.date['day']}"
        menu['time_for'] = "lunch"
        
        self.menus.append(menu)

        return menu
    
    def new_menu_301_2(self, main_meal, side_meal):
        menu = MealItem()
        
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
        
        menu['date'] = f"{self.date['year']}{self.date['month']}{self.date['day']}"
        menu['time_for'] = "lunch"
        
        self.menus.append(menu)

        return menu

    def new_menu_dure(self, meal_name, time_for):
        menu = MealItem()
        
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
        
        menu['date'] = f"{self.date['year']}{self.date['month']}{self.date['day']}"
        menu['time_for'] = time_for
        
        self.menus.append(menu)

        return menu
    
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