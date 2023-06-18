. .venv/bin/activate
export ENV=development
export DATABASE_URI=sqlite:///database.sqlite3
export SECRET_KEY=iamasecretkey1234!@#$
export UPLOADS=$PWD/static/images/uploads
export JWT_SECRET_KEY=thisisasecretkey
export SENDER_EMAIL_ADDRESS="inpat2020@gmail.com"
export SENDER_EMAIL_PASSWORD="hdxzbrbboqlobcxk"
export WEBHOOK_URL="https://chat.googleapis.com/v1/spaces/AAAAFdiV4EQ/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=4BbVL_uTtg8byQ-OQniOx5muCRNLxQl0uo-b2WD_VeQ%3D"

celery --app api.celery beat --max-interval 1 -l info