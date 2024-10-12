from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from bs4 import BeautifulSoup
import json
import undetected_chromedriver as uc
from datetime import datetime

from config.variaveis_globais import (
    url_decolar,
    arquivo_de_palavras
)

def extrair_dados_completos(url):
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--start-maximized")
    
    driver = uc.Chrome(options=options)
    
    try:
        driver.get(url)
        time.sleep(10)  # Aumentado o tempo de espera inicial

        # Tenta fechar o banner de LGPD, se existir
        try:
            lgpd_banner = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "lgpd-banner"))
            )
            close_button = lgpd_banner.find_element(By.CLASS_NAME, "btn-close")
            driver.execute_script("arguments[0].click();", close_button)
        except:
            print("Banner de LGPD não encontrado ou não foi possível fechá-lo.")

        # Loop para clicar no botão "Ver mais ofertas"
        while True:
            try:
                ver_mais_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'see-more-offers')]//em[contains(@class, 'btn-text') and text()='Ver mais ofertas']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", ver_mais_button)
                time.sleep(2)  # Aumentado o tempo de espera após a rolagem
                driver.execute_script("arguments[0].click();", ver_mais_button)
                time.sleep(5)  # Aumentado o tempo de espera após o clique
            except ElementClickInterceptedException:
                print("Elemento interceptado, tentando novamente.")
                continue
            except TimeoutException:
                print("Botão 'Ver mais ofertas' não encontrado ou não clicável. Finalizando a extração.")
                break
            except Exception as e:
                print(f"Erro ao clicar no botão 'Ver mais ofertas': {e}")
                break

        # Extrai o conteúdo da página carregada
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        dados = []
        oferta_cards = soup.find_all('div', class_='offer-card')
        
        # Obter a data e hora atual
        now = datetime.now()
        data_extracao = now.strftime("%Y-%m-%d")
        hora_extracao = now.strftime("%H:%M:%S")
        
        for oferta in oferta_cards:
            titulo = oferta.find('div', class_='offer-card-title')
            preco_atual = oferta.find('span', class_='offer-card-pricebox-price-amount')
            descricao = oferta.find('p', class_='offer-card-description')
            duracao = oferta.find('span', class_='offer-card-main-driver')
            datas = oferta.find('div', class_='offer-dates-container')
            cidade_saida = oferta.find('span', class_='offer-card-departure-city')
            servicos_incluidos = oferta.find('div', class_='offer-card-services')
            preco_original = oferta.find('span', class_='offer-card-pricebox-price-old')
            economia = oferta.find('span', class_='discount-top-label')
            pontos = oferta.find('span', class_='eva-3-pricing-points')
            imagem = oferta.find('img', class_='offer-card-image-main-not-eva')['src'] if oferta.find('img', class_='offer-card-image-main-not-eva') else None
            
            if titulo and preco_atual:
                dados.append({
                    'titulo': titulo.text.strip(),
                    'preco_atual': preco_atual.text.strip(),
                    'descricao': descricao.text.strip() if descricao else None,
                    'duracao': duracao.text.strip() if duracao else None,
                    'datas': datas.text.strip() if datas else None,
                    'cidade_saida': cidade_saida.text.strip() if cidade_saida else None,
                    'servicos_incluidos': servicos_incluidos.text.strip() if servicos_incluidos else None,
                    'preco_original': preco_original.text.strip() if preco_original else None,
                    'economia': economia.text.strip() if economia else None,
                    'pontos': pontos.text.strip() if pontos else None,
                    'imagem': imagem,
                    'data_extracao': data_extracao,
                    'hora_extracao': hora_extracao
                })

        # Salvar em arquivo JSON
        with open(arquivo_de_palavras, 'w', encoding='utf-8') as json_file:
            json.dump(dados, json_file, ensure_ascii=False, indent=4)

        # Salvar em arquivo de texto
        with open('data/external/dados_completos.txt', 'w', encoding='utf-8') as arquivo:
            for dado in dados:
                for key, value in dado.items():
                    if value:
                        arquivo.write(f"{key.capitalize()}: {value}\n")
                arquivo.write("\n---\n\n")
        
        print(f"Extraídos {len(dados)} itens.")

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        driver.quit()

def run_scraper():
    extrair_dados_completos(url_decolar)


if __name__ == "__main__":
    run_scraper()