import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree

data = {
    "REF": [],
    "Nome do Produto": [],
    "Linha": [],
    "Valor": [],
    "Descrição Geral": [],
    "Código": [],
    "Código de Barras": [],
    "Modo de Uso": [],
    "Composição": [],
}

# URL do site da Grandha
url = "https://www.lojagrandha.com.br/loja/busca.php"

response = requests.get(url)

# Verificando se a requisição foi bem sucedida
if response.status_code == 200:
    # Utilizando o BeautifulSoup para analisar o conteúdo HTML recebido
    soup = BeautifulSoup(response.text, 'html.parser')

    # Usando o seletor CSS para encontrar o link dentro do primeiro elemento específico
    product_element = soup.select_one('div.application > main > div > div > div > div.col-content > div.catalog-content > div > ul > li:nth-of-type(9) > div > div.image > a')
    if product_element and product_element.has_attr('href'):
        product_link = product_element['href']
        print("Link encontrado:", product_link)

        # Fazendo uma segunda requisição para o link encontrado
        response_link = requests.get(product_link)
        if response_link.status_code == 200:
            print("Página do link carregada com sucesso!")

            soup = BeautifulSoup(response_link.text, 'html.parser')

            # Capturando nome do produto
            product_name = soup.select_one('#product-wrapper > div.product-box > div.product-form > h1').get_text(strip=True)
            
            # Capturando referência do produto
            product_ref = soup.select_one('#product-reference').get_text(strip=True)

            tree = etree.HTML(response_link.text)
            # Capturando linha do produto
            product_line_element = tree.xpath('//*[@id="product-wrapper"]/div[1]/div[2]/div[3]/strong/text()')

            # Capturando o preço do produto
            product_price = soup.select_one('#variacaoPreco').get_text(strip=True)

            # Capturando a descrição geral do produto
            # TODO

            # Acessando a aba de ficha técnica do produto
            technicalSheet_element = soup.select_one('#product-wrapper > div.product-tabs > ul > li:nth-child(2) > a')
            if technicalSheet_element and technicalSheet_element.has_attr('href'):
                technicalSheet_link = technicalSheet_element['href']
                print("Link Encontrado:", technicalSheet_link)

            # Capturando o Código do Produto


            if product_line_element:
                product_line = product_line_element[0].strip()

            # Imprimir conteúdo da págna do link
            data["Nome do Produto"].append(product_name)
            data["REF"].append(product_ref)
            data["Linha"].append(product_line)
            data["Valor"].append(product_price)
            data["Código"].append("")
            data["Código de Barras"].append("")
            data["Modo de Uso"].append("")
            data["Composição"].append("")
            data["Descrição Geral"].append("")
        
        else:
            print(f"Erro ao carregar a página do link: Status {response_link.status_code}")
    else:
        print("Arquivo não encontrado")
        
else:
    print(f"Erro ao acessar a página: Status {response.status_code}")

print(data["Nome do Produto"])
print(data["REF"])
print(data["Linha"])
print(data["Valor"])
df = pd.DataFrame(data)

df.to_csv("Produtos da Grandha.csv", index=False, sep=";")