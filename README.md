# Conversor de Moedas - Banco Central do Brasil (BCB)

Este projeto automatiza a consulta de conversões de moedas no site oficial do Banco Central do Brasil (`https://www.bcb.gov.br/conversao`) utilizando Python e Selenium.

---

## 🔧 Funcionalidades

- Seleção da data atual automaticamente.
- Preenchimento do valor base a ser convertido.
- Seleção dinâmica da moeda de origem e das moedas de destino com base em um arquivo `config.json`.
- Extração da cotação e resultado da conversão.
- Geração de arquivo `.xlsx` com o histórico da consulta.
- Logs de execução via biblioteca `logger_python`.

---

## 📁 Estrutura esperada do `config.json`

```json
{
  "moeda_de": "Real (BRL)",
  "moeda_para": [
    "Dólar dos Estados Unidos (USD)",
    "Franco suíço (CHF)",
    "Xelim de Uganda (UGX)"
  ]
}
```

---

## 📦 Requisitos

- Python 3.8+
- Google Chrome instalado
- [ChromeDriver](https://sites.google.com/chromium.org/driver/) compatível com sua versão do Chrome no PATH

### Instalação de dependências:

```bash
pip install selenium pandas openpyxl logger-python
```

---

## ▶️ Como executar

1. Configure o `config.json` com as moedas desejadas.
2. Execute o script com:

```bash
python nome_do_arquivo.py
```

3. O resultado será salvo no arquivo `cotacao_conversao.xlsx`.

---

## 📄 Estrutura do arquivo Excel

| Data       | Moeda entrada | Moeda saida                    | Taxa | Valor cotação | Status                                |
|------------|----------------|--------------------------------|------|----------------|----------------------------------------|
| 16/05/2025 | Real (BRL)     | Dólar dos Estados Unidos (USD) | 1,00 | 0.1757         | Consulta OK                            |
| ...        | ...            | ...                            | ...  | ...            | Cotação encontrada não é da data atual |

---

## 📂 Logs

Logs são emitidos em tempo real durante a execução, informando cada passo do processo, erros e exceções, via a biblioteca `logger_python`.

---

## 🛠️ Estrutura do Código

- `setup_driver()` – Inicializa o Selenium WebDriver com opções (incluindo modo headless).
- `main()` – Função principal que executa:
  - Leitura da configuração
  - Consulta para cada moeda de destino
  - Extração dos dados
  - Gravação em planilha Excel

---

## 🧪 Testado em

- Python 3.11
- Chrome 124+
- ChromeDriver 124+

---

## 📝 Licença

MIT © [Seu Nome ou Organização]