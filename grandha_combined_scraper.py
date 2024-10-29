
import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import os
import time

# URL base do site da Grandha
base_url = "https://www.lojagrandha.com.br/loja/busca.php?loja=1068419&palavra_busca="

# Diretório para salvar dados e imagens
data_directory = 'data'
image_directory = os.path.join(data_directory, 'images')
os.makedirs(image_directory, exist_ok=True)

# Estrutura de dados para salvar informações de produtos
data = {
    "REF": [],
    "Nome do Produto": [],
    "Linha": [],
    "Valor": [],
    "Descrição Geral": [],
    "Código de Barras": [],
    "Modo de Uso": [],
    "Composição": [],
    "Link do Produto": []
}

# Seletores de imagens
image_selector = "div.zoom > img"

# Iterar sobre as páginas
for page in range(1, 12):
    url = f"{base_url}&pg={page}"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        product_elements = soup.select('div.application > main > div > div > div > div.col-content > div.catalog-content > div > ul > li > div > div.image > a')
        
        for product_element in product_elements:
            if product_element.has_attr('href'):
                product_link = product_element['href']
                print("Link encontrado:", product_link)

                response_link = requests.get(product_link)
                if response_link.status_code == 200:
                    soup = BeautifulSoup(response_link.text, 'html.parser')

                    # Extraindo informações do produto
                    product_name = soup.select_one('#product-wrapper > div.product-box > div.product-form > h1').get_text(strip=True)
                    product_name_sanitized = product_name.replace("/", "-")  # Para nome de pasta
                    product_ref = soup.select_one('#product-reference').get_text(strip=True)
                    product_price = soup.select_one('#variacaoPreco').get_text(strip=True)
                    product_description = soup.select_one("#descricao").text
                    product_mode = soup.select_one("#AbaPersonalizadaConteudo9").text
                    product_ean = f"'{soup.select_one('table tr:nth-child(2) td:nth-child(2)').get_text(strip=True)}"
                    
                    tree = etree.HTML(response_link.text)
                    product_line_elements = tree.xpath('//*[@id="product-wrapper"]/div[1]/div[2]/div[3]/strong/text()')
                    product_line = product_line_elements[0].strip() if product_line_elements else "Não encontrado"
                    product_composition = ','.join(tree.xpath('//*[@id="AbaPersonalizadaConteudo13"]/div/p[2]/text()'))

                    # Salvar informações do produto
                    data["Nome do Produto"].append(product_name)
                    data["REF"].append(product_ref)
                    data["Linha"].append(product_line)
                    data["Valor"].append(product_price)
                    data["Descrição Geral"].append(product_description)
                    data["Código de Barras"].append(product_ean) 
                    data["Modo de Uso"].append(product_mode)
                    data["Composição"].append(product_composition)
                    data["Link do Produto"].append(product_link)

                    # Diretório específico para imagens do produto
                    product_image_directory = os.path.join(image_directory, product_name_sanitized)
                    os.makedirs(product_image_directory, exist_ok=True)

                    # Extraindo e salvando imagens
                    images = soup.select(image_selector)
                    image_urls = [img.get("data-src") for img in images if img.get("data-src")]
                    
                    for i, img_url in enumerate(image_urls, start=1):
                        img_response = requests.get(img_url)
                        if img_response.status_code == 200:
                            img_path = os.path.join(product_image_directory, f"{product_name_sanitized}_{i}.jpg")
                            with open(img_path, "wb") as f:
                                f.write(img_response.content)
                            print(f"Imagem {product_name_sanitized}_{i} salva em {img_path}")
                        else:
                            print(f"Erro ao baixar a imagem {img_url}")
                
                else:
                    print(f"Erro ao carregar a página do link: Status {response_link.status_code}")
            else:
                print("Link não encontrado em um dos produtos.")

        time.sleep(1)  # Pausa entre cada requisição para evitar sobrecarga no servidor
    else:
        print(f"Erro ao acessar a página {page}: Status {response.status_code}")

# Criando DataFrame e salvando em CSV
df = pd.DataFrame(data)
os.makedirs(data_directory, exist_ok=True)
df.to_csv(os.path.join(data_directory, "Produtos_da_Grandha.csv"), index=False, sep=";", encoding='utf-8-sig')
print("Arquivo CSV criado com sucesso!")
