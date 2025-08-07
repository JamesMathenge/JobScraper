# 🧠 JobScraper

A simple Django web app that allows users to search for remote jobs and scrape live listings from [RemoteOK](https://remoteok.com/). It stores recent searches and displays job results with company info, location, and descriptions.

---

## 🚀 Features

- 🔎 Search for remote jobs by title
- 🌐 Scrapes job data live from RemoteOK
- 🧾 Stores recent search history in the database
- 📋 Displays top 10 job listings per search
- 🧱 Built with Django, BeautifulSoup, and Bootstrap 5

---

## 📁 Project Structure

```
JobScraper/
├── manage.py
├── JobScraper/
│   ├── settings.py
│   ├── urls.py
├── scraper/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/
│   │   └── jobs.html
├── requirements.txt
```

---

## ⚙️ Tech Stack

- **Backend:** Django 4.2
- **Web Scraping:** Requests & BeautifulSoup4
- **Database:** SQLite3 (default Django DB)
- **Frontend:** Bootstrap 5

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/JobScraper.git
cd JobScraper
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the Development Server
```bash
python manage.py runserver
```

Open your browser and visit: http://127.0.0.1:8000

---

## 🛠 How It Works

1. Users enter a job title on the homepage.
2. The app sends a request to https://remoteok.com/remote-<job>-jobs.
3. BeautifulSoup parses the returned HTML and extracts job details.
4. Results are saved to the database and displayed to the user.