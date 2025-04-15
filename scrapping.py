  
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()


produtos_data = []

with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
    url = "https://www.cacaushow.com.br/categoria/p%C3%A1scoa"
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    produtos_container = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="product-search-results"]/div[2]/div[2]/div[3]')
    ))

    produtos = produtos_container.find_elements(By.XPATH, './div')

    for produto in produtos:
        try:
            imagem_tag = produto.find_element(By.XPATH, './div/div/div[2]/div[1]/a')
            imagem_link = imagem_tag.get_attribute('href')

            nome = produto.find_element(By.XPATH, './div/div/div[2]/div[2]').text

            preco_div = produto.find_element(By.XPATH, './div/div/div[3]/div[1]/div/div[1]/div')
            precos_texto = preco_div.text.split("\n")

            # Detectar se tem preço antigo + atual ou só o atual
            if len(precos_texto) == 2:
                preco_antigo = precos_texto[0].replace("R$", "").replace(",", ".").strip()
                preco = precos_texto[1].replace("R$", "").replace(",", ".").strip()
            else:
                preco_antigo = ""
                preco = precos_texto[0].replace("R$", "").replace(",", ".").strip()

            produto_info = {
                "nome": nome,
                "imagem": imagem_link,
                "preco_antigo": preco_antigo,
                "preco": preco,
                "etiquetas": []  # Pode adicionar lógica para etiquetas depois
            }

            produtos_data.append(produto_info)

        except Exception as e:
            print("Erro ao extrair produto:", e)

# Gera arquivo Python com os dados
with open("produtos_extraidos.py", "w", encoding="utf-8") as f:
    f.write("produtos = ")
    json.dump(produtos_data, f, ensure_ascii=False, indent=4)
