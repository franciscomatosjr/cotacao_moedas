import time
import datetime
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from logger_python.logger_python import logger
import traceback


def setup_driver(headless: bool = True) -> webdriver.Chrome:
    """
    Configura o Selenium WebDriver (Chrome).
    """
    logger.info("Configurando o Selenium WebDriver")
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    # Se necessário, especifique o caminho do chromedriver:
    # service = Service("/caminho/para/chromedriver")
    service = Service()  # assume chromedriver no PATH
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def main():

    logger.info("Carregar o config")
    with open("config.json", encoding="utf-8") as f:
        config = json.load(f)

    moeda_de = config["moeda_de"]
    lst_moeda_para = config["moeda_para"]

    logger.info(f"Moeda base da conversão: {moeda_de}")

    driver = setup_driver(False)
    actions = ActionChains(driver)

    try:
        data_for_data_frame = []
        for moeda_para in lst_moeda_para:

            logger.info(f"Moeda para -> '{moeda_para}'")
            driver.get("https://www.bcb.gov.br/conversao")
            wait = WebDriverWait(driver, 10)

            logger.info("Aguarda campo da data e insere a data atual")
            data_str = datetime.date.today().strftime("%d/%m/%Y")
            date_input = wait.until(EC.presence_of_element_located(
                (By.ID, "dataMask")))
            date_input.clear()
            date_input.send_keys(data_str)

            logger.info("Preenche o valor")
            amount_input = driver.find_element(By.NAME, "valorBRL")
            amount_input.clear()
            amount_input.send_keys("100")

            logger.info("Abre dropdown 'Converter de'")
            btn_converter_de = driver.find_element(By.ID, "button-converter-de")
            btn_converter_de.click()

            logger.info("Aguarda lista e seleciona a moeda DE")
            time.sleep(1)
            moedas_de = driver.find_elements(By.CSS_SELECTOR, "#moedaBRL a.dropdown-item")
            for item in moedas_de:
                if moeda_de in item.text:
                    actions.move_to_element(item).click().perform()
                    break

            time.sleep(1)

            logger.info('Abre dropdown "Para"')
            btn_para = driver.find_element(By.ID, "button-converter-para")
            btn_para.click()

            logger.info("Aguarda lista e seleciona a moeda PARA")
            time.sleep(1)
            moedas_para = driver.find_elements(By.CSS_SELECTOR, "#moedaUSD a.dropdown-item")
            for item in moedas_para:
                if moeda_para in item.text:
                    actions.move_to_element(item).click().perform()
                    break

            btn_converter = driver.find_element(By.XPATH, "//*[@title='Converter']")
            actions.move_to_element(btn_converter).click().perform()

            logger.info("Aguarda resultado aparecer")
            resultado = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@class='resultado']"))
            )

            texto = resultado.text

            logger.info("Quebra o texto em linhas")
            linhas = [linha.strip() for linha in texto.strip().splitlines() if linha.strip()]

            logger.info("Mapeia os dados manualmente")
            resultado = {
                "conversao_de": linhas[1].split(":", 1)[1].strip(),
                "valor_a_converter": linhas[2].split(":", 1)[1].strip(),
                "para": linhas[3].split(":", 1)[1].strip(),
                "resultado_da_conversao": linhas[4].split(":", 1)[1].strip(),
                "data_cotacao_utilizada": linhas[5].split(":", 1)[1].strip(),
                "taxa": {
                    "de_para": linhas[7].strip(),
                    "para_de": linhas[8].strip()
                }
            }

            if resultado.get('data_cotacao_utilizada') == data_str:
                status = 'Consulta OK'
            else:
                status = 'Contação encontrada não é da data atual'

            data_for_data_frame.append({
                "Data": resultado.get('data_cotacao_utilizada'),
                "Moeda entrada": moeda_de,
                "Moeda saida": moeda_para,
                "Taxa": "1,00",
                "Valor cotação": resultado.get('resultado_da_conversao'),
                "Status": status
            })

        # Salva no Excel
        df = pd.DataFrame(data_for_data_frame)

        df.to_excel("cotacao_conversao.xlsx", index=False)
        logger.info("Resultado salvo em cotacao_conversao.xlsx")

    except Exception as error:
        logger.error(error)
        logger.info(traceback.format_exc())
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()