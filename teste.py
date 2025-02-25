import requests
from twocaptcha import TwoCaptcha
import base64
from bs4 import BeautifulSoup

# 🛠️ Configuração
API_KEY = "c559ef9877a25f6c80f12d9e846ea1f0"  # API Key do TwoCaptcha
SITE_KEY = "6Lel5yQTAAAAAL3DDXn2lm6J31ke4awM587E001a"  # Site Key do reCAPTCHA
URL_SITE = "https://atende.cemig.com.br/Login"
URL_LOGIN = "https://atende.cemig.com.br/Login"

# 🏗️ Função para resolver o CAPTCHA
def call_recaptcha_api(api_key):
    solver = TwoCaptcha(api_key)
    return solver

def recaptcha(solver, recaptcha_key, url_site):
    captcha_response = None
    while not captcha_response:
        try:
            result = solver.recaptcha(sitekey=recaptcha_key, url=url_site)
            captcha_response = result['code']
            print('✅ Captcha Resolvido:', captcha_response)
            return captcha_response
        except Exception as e:
            print('❌ Erro ao resolver captcha:', e)

# 🔑 Criando sessão de login
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 🛠️ Pegando o Token CSRF (__RequestVerificationToken)
response_login_page = session.get(URL_SITE, headers=headers)
soup = BeautifulSoup(response_login_page.text, 'html.parser')
csrf_input = soup.find('input', {'name': '__RequestVerificationToken'})

if csrf_input and csrf_input.get('value'):
    csrf_token = csrf_input.get('value')
    print("✅ Token CSRF capturado:", csrf_token)
else:
    print("❌ Não foi possível capturar o token CSRF")
    exit()

# 🚀 Resolvendo o CAPTCHA
solver = call_recaptcha_api(API_KEY)
captcha_response = recaptcha(solver, SITE_KEY, URL_SITE)

# 🔒 Encode da Senha em Base64
senha_original = "Casaevideo1"
senha_encoded = base64.b64encode(senha_original.encode()).decode()

# 📤 Fazendo a requisição de login
payload = {
    "__RequestVerificationToken": csrf_token,
    "AcessoCompartilhado": "False",
    "RedirectExcluirConta": "False",
    "Acesso": "11.114.284/0001-63",  # Seu CNPJ/CPF
    "Senha": senha_encoded,  # Senha em Base64
    "g-recaptcha-response": captcha_response
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Requested-With": "XMLHttpRequest"
}

response = session.post(URL_LOGIN, data=payload, headers=headers)

# 📝 Verificando resposta
if response.status_code == 200:
    print("✅ Login bem-sucedido!")
    print(response.json())  # Exibe o retorno do login (possivelmente um token de autenticação)
else:
    print("❌ Falha no login:", response.text)