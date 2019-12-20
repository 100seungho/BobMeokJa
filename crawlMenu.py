from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

web_url = "http://snuco.snu.ac.kr/ko/foodmenu?field_menu_date_value_1[value][date]=&field_menu_date_value[value][date]=12/19/2019"

with urllib.request.urlopen(web_url) as response:
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

table = soup.find(class_ = 'views-table cols-4')
restaurant = [item.get_text() for item in soup.find_all(class_ = 'views-field views-field-field-restaurant')]
breakfast = [item.get_text() for item in soup.find_all(class_ = 'views-field views-field-field-breakfast')]
lunch = [item.get_text() for item in soup.find_all(class_ = 'views-field views-field-field-lunch')]
dinner = [item.get_text() for item in soup.find_all(class_ = 'views-field views-field-field-dinner')]

def get_meal(i):
    return print(restaurant[i], breakfast[i], lunch[i], dinner[i])