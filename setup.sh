
# this setup creates a virtual environment for running the service
# it instantiates sqlite3-db an pre-populates it with a few polls

python3 -m venv poll_app
source poll_app/bin/activate
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata utils/initiate_db.json  # populates the db with some initial polls
python3 manage.py runserver

# note to self: to start testing from scratch:
# deactivate
# rm -rf poll_app
# rm db.sqlite3
