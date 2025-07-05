# Cashback Promotion – Django Project Setup

This project is a Django-based cashback promotion system.

## 🔧 Project Structure

```
cashback_promotion/
    │
    ├── cashback_promositon/       # Main Django app
    ├── config/                    # Project settings
    ├── manage.py                  # Django management script
    ├── requirements.txt           # Python dependencies
    ```

---

## 🚀 Getting Started

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/vishalpandhare01/cashback_promotion.git
cd cashback_promotion
```

### 2. Create and Activate a Virtual Environment

**For macOS/Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

**For Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

---

## 📝 Notes

* Make sure you are using Python 3.7 or higher.
* Adjust settings in `config/settings.py` if needed (e.g. database, debug mode).
* The default app is located in the `cashback_promositon/` directory.

---
