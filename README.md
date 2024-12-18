# Build Project

1. Create a Virtual Environment

Windows:
```bash
python -m venv .venv
```

Mac/Linux:
```bash
python3 -m venv .venv
```

---

2. Activate the Virtual Environment

Windows:
```bash
.venv/Scripts/activate
```

Mac/Linux:
```bash
source .venv/bin/activate
```

---

3. Install Dependencies

Windows:
```bash
pip install -r requirements.txt
```

Mac/Linux:
```bash
pip3 install -r requirements.txt
```

---


4. Migrate the Database

Windows:
```bash
python manage.py makemigrations
python manage.py migrate
```

Mac/Linux:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

---

5. Create a Superuser

Windows:
```bash
python manage.py createsuperuser
```

Mac/Linux:
```bash
python3 manage.py createsuperuser
```

---

6. Run the Development Server

Windows:
```bash
python manage.py runserver
```

Mac/Linux:
```bash
python3 manage.py runserver
```
