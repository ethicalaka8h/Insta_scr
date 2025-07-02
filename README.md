# 🔍 Instagram Follower Scraper (Terminal Edition)

A powerful, terminal-based tool to scrape followers from any public Instagram account. Built with Python, this script uses rich CLI UI to offer a smooth, professional scraping experience directly from your terminal.

---

## 🚀 Features

- 🔐 Secure login with masked password input
- 📥 Scrapes followers of any Instagram account (including your own)
- 📂 Exports data to a clean `.txt` file
- 💡 Rich interface with loading bars, styled panels, and color-coded logs
- 🧠 Handles rate-limiting, retries, and session management
- 📱 Emulates mobile headers for greater API compatibility
- 🧩 No API key or developer account required

---

## ⚙️ Requirements

- Python 3.8+
- Install required libraries using pip:

```bash
pip install -r requirements.txt
```

requirements.txt should include:
```
requests
rich
user_agent
```

---

🛠 Usage

python app.py

1. Enter your Instagram username and password when prompted.


2. Input the target username whose followers you want to scrape.

Leave empty to scrape your own followers.



3. The script will scrape followers and save them into a .txt file in the same directory.




---

📁 Output

Example filename:

followers_<username>_<timestamp>.txt

Each line will contain one follower's Instagram username.


---

📸 Screenshot
```
┌─────────────────────────────────────────────┐
│        Instagram Follower Scraper           │
└─────────────────────────────────────────────┘
USERNAME: your_username
PASSWORD: ***********
✓ Login successful!
Scraping followers... 203 collected
✓ Successfully saved 203 followers to followers_target_1720189291.txt

```
---

⚠️ Disclaimer

This project is for educational purposes only. Scraping data from Instagram may violate their terms of service. Use responsibly.


---

📬 Author

Developed by Aakash — Making automation beautiful and powerful.

Feel free to ⭐ star the repo if you find it useful!

---
