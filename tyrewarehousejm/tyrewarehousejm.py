import re
import time
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

ENLACE = "https://www.tyrewarehousejm.com/search/tires"

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(60)

driver.get(ENLACE)

def cargar_medidas():
    with open('./medidas.csv', 'r', encoding='utf-8') as archivo:
        medidas = archivo.readlines()[1:]
        return medidas

def select_location():
    find()
    button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//button[@form='search_location_826']"))
    )    
    ActionChains(driver).move_to_element(button).click().perform()

def select(width, profile, size):
    selector('width').select_by_value(width)
    selector('profile').select_by_value(profile)
    selector('size').select_by_value(size)

def selector(select):
    if select == 'width':
        return Select(WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//select[@name = 'width']"))))
    elif select == 'profile':
        return Select(WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, "//select[@name = 'aspect']"))))
    else:
        return Select(WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH, "//select[@name = 'diameter']"))))

def get_options(select):
    if select == 'width':
        return [option.text for option in selector('width').options]
    elif select == 'profile':
        return [option.text for option in selector('profile').options]
    else:
        return [option.text for option in selector('size').options]

def find():
    button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, "//div[@id='bySize']//button[@type='submit' and text() = 'FIND TIRES NOW']"))
    )
    ActionChains(driver).move_to_element(button).click().perform()

def links():
    web_elements = WebDriverWait(driver, 3).until(
        ec.presence_of_all_elements_located((By.XPATH, "//a[@title='Add to Quote']"))
    )
    return len(web_elements)

select_location()

medidas = cargar_medidas()

count = 0

with open('medidas.txt', 'a', encoding='utf-8') as archivo:
    for medida in medidas:        
        try:
            match = re.match(r"(\d+)/(\d+)R(\d+)", medida.strip())
            width, profile, size = match.groups()
            select(width, profile, size)
            find()
            count += links()
            print("Llantas encontradas: "+Fore.BLUE+f"{count}"+Fore.RESET)
            archivo.write(f"{width}/{profile}R{size}\n")
            time.sleep(3)
        except Exception as e:
            print(Fore.YELLOW+f"No se encontraron llantas: {e}"+Fore.RESET)
        driver.get(ENLACE)         
                
driver.quit()



