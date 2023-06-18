. .venv/bin/activate
export ENV=development
export DATABASE_URI=sqlite:///database.sqlite3
export SECRET_KEY=iamasecretkey1234!@#$
export UPLOADS=$PWD/static/images/uploads
export JWT_SECRET_KEY=thisisasecretkey
export SENDER_EMAIL_ADDRESS="example@gmail.com"
export SENDER_EMAIL_PASSWORD="thisisapassword"
export WEBHOOK_URL="https://thisisawebhookurl"

python api.py
