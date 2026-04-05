Локальный запуск
python3 -m venv .venv
# source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver

Открыть:

http://127.0.0.1:8000/
админка: http://127.0.0.1:8000/admin/
Если нужна админка (первый запуск)
python manage.py createsuperuser
Полезно перед запуском
Если вдруг старый venv мешает:

rm -rf .venv
python3 -m venv .venv
# source .venv/bin/activate
pip install -r requirements.txt
Для Railway (чтобы было одинаково с продом)
Локально можно проверить той же командой, что в старте:

python manage.py migrate && python manage.py collectstatic --noinput && gunicorn burger_shop.wsgi:application --bind 0.0.0.0:8000 --log-file -