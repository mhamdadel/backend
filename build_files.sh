echo "Build Start"
python -m pip install -r installedapp.txt
python manage.py collectstatic --noinput --clear
echo "Build finished"