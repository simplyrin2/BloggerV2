# BloggerV2
#### Version 2 of the blogging application Blogger

BloggerV2 is a multi-user application for you can upload and engage with blogs. The application allows one to create blogs, follow/unfollow other users, like or comment on blogs or archive their own blogs.

## Installation

Blogger requires Python, redis-server to run the backend.
Blogger requires npm to run the frontend.

## Running the Backend
1. Navigate to the ./Backend directory
2. Create a virtual environment

```sh
python3 -m venv .venv
```

3. Run the virtual environment

```sh
source .venv/bin/activate
```

4. Install the required packages in requirements.txt present in the root folder

```sh
pip3 install -r requirements.txt
```

For running the application: 
5. Make the required configuration changes in run.sh file and run the script

```sh
redis-server
bash run.sh
bash celery_run.sh
bash celery_beat.sh
bash gunicorn.sh
```

## Running the frontend
1. Install node and npm on your system
2. Navigate to the ./Frontend directory
3. Install the required packages
```sh
npm install
```

4. Run the vue program
```sh
npm run serve
```
