echo " BUILD START"
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3.10 manage.py makemigrations --noinput
python3.10 manage.py migrate --noinput
python3.10 manage.py collectstatic --noinput
echo "BUILD END"