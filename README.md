# 📢 IPO Notifier: Sharesansar Scraper + PushBullet + PostgreSQL

A Python automation tool that scrapes the latest IPO-related news from [Sharesansar](https://www.sharesansar.com/) and sends real-time notifications to your device using PushBullet. The system ensures **no duplicate alerts** by tracking previously notified IPOs in a PostgreSQL database.

---

## 🚀 Features

- 🔍 Scrapes IPO news headlines from Sharesansar using Selenium.
- ⚙️ Handles JavaScript-rendered content dynamically.
- 🔔 Sends push notifications to your mobile or PC via PushBullet.
- ♻️ Prevents duplicate alerts using PostgreSQL tracking.
- 🧾 Logs all activities for traceability.
- 🔐 Manages API keys and credentials securely with `.env`.

---

## 🛠️ Tech Stack

- **Language:** Python 3
- **Web Scraping:** Selenium WebDriver
- **Database:** PostgreSQL
- **Notifications:** PushBullet API
- **DB Connection:** psycopg2
- **Environment Variables:** python-dotenv

---

## 📦 Requirements
`requirements.txt`

```
selenium
psycopg2
python-dotenv
```
- Install dependencies:

```bash
pip install -r requirements.txt
```
---
## 🔐 Environment Setup
Create a .env file in the project root:
```sql
PUSHBULLET_API_KEY=your_pushbullet_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ipo_notifier
DB_USER=your_db_username
DB_PASSWORD=your_db_password
```
---
## 🗄️ PostgreSQL Configuration

Install PostgreSQL and create a database named ipo_notifier.

Run the following SQL to create the required table:
```bash
CREATE TABLE notified_ipos (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
Ensure your `.env` file has the correct credentials.

## 📁 .gitignore
Add the following to `.gitignore` to avoid committing sensitive or unnecessary files:

```
.env
__pycache__/
*.pyc
*.log
```
## ▶️ How to Run
Run the script using:
```
python db_added_ipo_notifier_with_selenium_&_no_repetition.py

```
## ✅ Sample Output

<img width="415" height="1157" alt="Screenshot 2025-07-23 210041" src="https://github.com/user-attachments/assets/9ab3c81e-fdad-4e39-a731-3cfdd0e351af" />
<img width="1397" height="962" alt="Screenshot 2025-07-23 231513" src="https://github.com/user-attachments/assets/555da470-dd56-4069-b872-5874e9619fb8" />

## 📝 Future Improvements
⏰ Add scheduling (e.g., via cron or Windows Task Scheduler)

🐳 Dockerize for containerized deployment

📧 Support email notifications

🌐 Add a simple web dashboard for monitoring

## 📚 Project Structure

```bash
ipo-notifier/
├── db_added_ipo_notifier_with_selenium_&_no_repetition.py
├── .env
├── requirements.txt
├── .gitignore
└── README.md
```
🤝 Contributing
Contributions are welcome! Feel free to fork the project and submit a pull request.


