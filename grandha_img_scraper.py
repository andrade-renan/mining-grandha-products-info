import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import time
import os

# URL base do site da Grandha
base_url = "https://www.lojagrandha.com.br/loja/busca.php?loja=1068419&palavra_busca="

# Criando diretório para salvar a imagem
directory = 'data/images'
os.makedirs(directory, exist_ok=True)

selectors = [
    "div.image.swiper-slide.active.swiper-slide-active > div > img.zoomImg",
    "div.image.swiper-slide.swiper-slide-active > div > img.zoomImg"
]

# Iterar sobre todas as 12 páginas
for page in range(1, 12):
    url = f"{base_url}&pg={page}"
    response = requests.get(url)

    if response.status_code == 200:
        # Utilizando o BeautifulSoup para analisar o conteúdo HTML recebido
        soup = BeautifulSoup(response.text, 'html.parser')

        # Selecionar todos os elementos de produto na página
        product_elements = soup.select('div.application > main > div > div > div > div.col-content > div.catalog-content > div > ul > li > div > div.image > a')
        
        for product_element in product_elements:
            if product_element.has_attr('href'):
                product_link = product_element['href']
                print("Link encontrado:", product_link)

                response_link = requests.get(product_link)
                if response_link.status_code == 200:
                    soup = BeautifulSoup(response_link.text, 'html.parser')

                    # Selecionar o nome do produto para criação da pasta
                    product_name = soup.select_one('#product-wrapper > div.product-box > div.product-form > h1').get_text(strip=True)
                    product_name = product_name.replace("/", "-")
                    # Criando um subdiretório de com o nome do produto
                    sub_directory = os.path.join(directory, product_name)
                    os.makedirs(sub_directory, exist_ok=True)

                    # Selecionar todas as imagens com data-src dentro de div.zoom
                    images = soup.select("div.zoom > img")

                    # Lista para armazenar URLs de imagens
                    image_urls = []

                    # Extrair URLs do artributo data-src
                    for img in images:
                        img_url = img.get("data-src")
                        if img_url and img_url not in image_urls: # Evitar URLs duplicadas
                            image_urls.append(img_url)

                    # Baixar e salvar cada imagem
                    for i, img_url in enumerate(image_urls, start=1):
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_path = os.path.join(sub_directory, f"{product_name}_{i}.jpg")
                            with open(img_path,  "wb") as f:
                                f.write(img_response.content)
                            print(f"Imagem {product_name}_{i} salvo em {img_path}")
                        else:
                            print(f"Erro ao baixar a imagem {img_url}")
                        
            

                else:
                    print(f"Erro ao carregar a página do link: Status {response_link.status_code}")
            else:
                print("Link não encontrado em um dos produtos.")

        time.sleep(1)  # Pausa entre cada requisição para evitar sobrecarga no servidor
    else:
        print(f"Erro ao acessar a página {page}: Status {response.status_code}")
