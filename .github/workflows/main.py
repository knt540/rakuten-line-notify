import os
import requests
from bs4 import BeautifulSoup

# 商品ページURL
PRODUCT_URL = "https://books.rakuten.co.jp/rb/18210487/"

# Discord Webhook URL（GitHub Secretsから取得）
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# 前回の状態を記録するファイル
STATUS_FILE = "last_status.txt"

def send_discord_notification(message):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"通知失敗: {response.status_code} - {response.text}")

def get_product_status():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    if "カートに入れる" in text:
        return "Available"
    elif "ご注文できない商品" in text:
        return "Unavailable"
    else:
        return "Unknown"

def read_last_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    return None

def write_last_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)

def main():
    current_status = get_product_status()
    last_status = read_last_status()

    if current_status != last_status or current_status == "Available":
        message = f"楽天ブックスの商品状態が変わりました: {current_status}\n{PRODUCT_URL}"
        send_discord_notification(message)
        write_last_status(current_status)

    print(f"Checked status: {current_status}")

if __name__ == "__main__":
    main()
