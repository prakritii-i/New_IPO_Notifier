import time
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pushbullet
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()  # takes environment variables from .env

CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
PUSHBULLET_API_KEY = os.getenv('PUSHBULLET_API_KEY')

DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}


# === DB FUNCTIONS ===
def connect_db():
    return psycopg2.connect(**DB_PARAMS)

# consults with db to chceck if the ipo has already been notified or not
def already_notified(url):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM notified_ipos WHERE url = %s", (url,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result is not None

def mark_as_notified(title, url):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO notified_ipos (title, url) VALUES (%s, %s) ON CONFLICT DO NOTHING", (title, url))
    conn.commit()
    cur.close()
    conn.close()

# === NOTIFICATION ===
def send_pushbullet_notification(title, url):
    pb = pushbullet.PushBullet(PUSHBULLET_API_KEY)
    pb.push_note(title, url)

# === SCRAPER ===
def get_ipo_articles():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    from selenium.webdriver.chrome.service import Service

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.sharesansar.com/category/ipo")

    time.sleep(5)  # wait for page load

    articles = driver.find_elements(By.CSS_SELECTOR, "h4.featured-news-title")

    ipo_list = []
    for article in articles:
        title = article.text.strip()
        url = None
        try:
            parent = article.find_element(By.XPATH, "./..")
            if parent.tag_name == 'a':
                url = parent.get_attribute('href')
            else:
                grandparent = parent.find_element(By.XPATH, "./..")
                if grandparent.tag_name == 'a':
                    url = grandparent.get_attribute('href')
        except Exception:
            pass

        if url and ('ipo' in title.lower() or 'ipo' in url.lower()):
            ipo_list.append((title, url))

    driver.quit()
    return ipo_list


# === MAIN ===
def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for IPOs...")

    new_ipos = 0
    ipo_articles = get_ipo_articles()

    print(f"Found {len(ipo_articles)} IPO articles.")

    for title, url in ipo_articles:
        print(f"Checking IPO: {title} - {url}")
        if not already_notified(url):
            print("Not notified yet, sending notification...")
            send_pushbullet_notification(title, url)
            mark_as_notified(title, url)
            new_ipos += 1
        else:
            print("Already notified.")

    if new_ipos == 0:
        print("No new IPOs to notify.")
    else:
        print(f"{new_ipos} new IPO(s) notified.")

if __name__ == "__main__":
    main()
