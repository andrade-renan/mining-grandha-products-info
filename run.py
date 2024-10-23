import requests
import pandas as pd
from bs4 import BeautifulSoup

# URL do site da Grandha
url = "https://www.lojagrandha.com.br/loja/busca.php"

response = requests.get(url)

# Verificando se a requisição foi bem sucedida
if response.status_code == 200:
    # Utilizando o BeautifulSoup para analisar o conteúdo HTML recebido
    soup = BeautifulSoup(response.text, 'html.parser')

    # Usando o seletor CSS para encontrar o link dentro do primeiro elemento específico
    link_element = soup.select_one('div.application > main > div > div > div > div.col-content > div.catalog-content > div > ul > li:nth-of-type(1) > div > div.image > a')

    if link_element and link_element.has_attr('href'):
        link = link_element['href']
        print("Link encontrado:", link)

        # Fazendo uma segunda requisição para o link encontrado
        response_link = requests.get(link)
        if response_link.status_code == 200:
            print("Página do link carregada com sucesso!")

            # Imprimir conteúdo da págna do link
            print(response_link.text[:500]) # Imprimir os primeiros 500 caracteres
        
        else:
            
else:
    print(f"Erro ao acessar a página: Status {response.status_code}")

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
    "Altura": [],
    "Largura": [],
    "Comprimento": [],
    "Peso": [] 
}

df = pd.DataFrame(data)

df.to_csv("Produtos da Grandha.csv", index=False, sep=";")