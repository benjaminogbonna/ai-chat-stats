echo " BUILD START"
python3.9 -m venv venv
source venv/bin/activate
pip uninstall -r requirements_dev.txt
pip uninstall -r requirements.txt
python3.9 manage.py makemigrations --noinput
python3.9 manage.py migrate --noinput
python3.9 manage.py collectstatic --noinput
echo "BUILD END"