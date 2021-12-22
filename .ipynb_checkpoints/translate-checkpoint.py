# Import libraries

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from time import sleep

# Función de entrar al traductor y traducir

def translate(arr, sl="auto", tl="en"):
    my_url = "https://translate.google.com.ar/?hl=es&sl=" + sl + "&tl=" + tl + "&op=translate"

    option = Options()
    option.headless = False
    driver = webdriver.Chrome(options=option)
    driver.get(my_url)
    driver.maximize_window()

    results = {
        "from" : [],
        "to" : []
    }
    for s in arr:
        counter = 0
        while True:
            try:
                # Write sentence to translate
                from_bar = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable((By.XPATH,
                    "/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea")))
                from_bar.clear()
                from_bar.send_keys(s)
                sleep(5)

                # Get result
                html = BeautifulSoup(driver.page_source, 'html.parser')
                result = html.find(class_="J0lOec").span.span.span.text
                results["from"].append(s)
                results["to"].append(result)

                # Volver
                break
            except:
                if counter < 2:
                    counter += 1
                    print(f'Failed to scrape. Trying again in 5 seconds.')
                    sleep(5)
                    continue
                else:
                    break
                    
    # Cerrar ventana
    driver.quit()
    return results


#BORRAR PARA FUNCIONAR EN JUPYTER
'''arr = [
    "Hola, soy un robot",
    "Estoy escrito en Python",
    "Y estoy automatizado para traducir estas frases",
    "Que tengan buenas noches"
]
results = translate(arr)
print(results)'''