echo " BUILD START"
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements_dev.txt
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
python3.9 manage.py collectstatic --noinput
echo "BUILD END"