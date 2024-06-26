# drf-trash
A backend for MEPhI's group project /drf-trash
competition, allowing customers to get information about their
grocery wrappers including a list of materials, recyclability and
more eco-friendly alternatives. The app also provides tools for
getting statistics waste produced by a person, a region or a
manufacturer, written in python + django-rest + MySQL.

# How to run
1. Clone this Repository
2. Navigate to the directory with this README
3. Create virtualenv - Optional
```
python -m venv venv
source venv/bin/activate
# venv\Scripts\activate on Windows
```
4. Install the requirements for the package:
```
pip install -r requirements.txt
```
5. Apply migrations
```
python manage.py migrate
```
6. Create Superuser (optional)
```
python manage.py createsuperuser
```
7. Run the server
```
python manage.py runserver
```

# How to use
You can open swagger documentation on http://127.0.0.1:8000/swagger/ , all currently supported requests are documented there.
