Crunchyroll Account Checker
A Python script to check Crunchyroll account validity with proxy support and sending valid/custom accounts to a Discord webhook.

Requirements
Python 3.8 or higher installed

Google Chrome installed (used by Selenium)

Internet connection

Discord webhook URL (to receive valid/custom accounts)

Installing dependencies
Open your terminal and run:

bash
Copier
Modifier
pip install selenium webdriver-manager requests
Setup
Clone or download this repository

bash
Copier
Modifier
git clone https://github.com/your-username/your-repo.git
cd your-repo
Configure your Discord webhook

Open your script file (e.g. checker.py) and replace the DISCORD_WEBHOOK_URL variable with your own webhook URL:

python
Copier
Modifier
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN"
Preparing files
accounts.txt: list of accounts to check, one per line, format email:password

proxies.txt (optional): list of proxies, one per line, format IP:PORT or USER:PASSWORD@IP:PORT

How to use
Run the script

bash
Copier
Modifier
python checker.py
In the menu:

Choose 1 to add accounts manually (or edit accounts.txt directly)

Choose 2 to add proxies (optional)

Choose 3 to start the checker

Choose 4 to exit

Results:

Valid premium accounts are saved to valid.txt and sent to your Discord webhook

Valid accounts without subscription (custom) are saved to custom.txt and sent to your Discord webhook

Invalid accounts are saved to invalid.txt

Important notes
The script runs Chrome in headless mode (no visible browser window).

Make sure your proxies are working properly to avoid connection issues.

Avoid running the checker too fast to prevent being blocked by Crunchyroll.

The Discord webhook only receives valid and custom accounts with status indication.

Troubleshooting
ChromeDriver errors: Ensure Chrome is installed and updated.

Proxy problems: Try running without proxies to isolate the issue.

Missing dependencies: Install them using pip install selenium webdriver-manager requests.

Chrome won’t start: Make sure your ChromeDriver version matches your Chrome version.

License
Use this project at your own risk. Provided "as-is" without warranty.

