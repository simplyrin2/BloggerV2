# BloggerV2
#### Version 2 of the blogging application Blogger

BloggerV2 is a multi-user application for you can upload and engage with blogs. The application allows one to create blogs, follow/unfollow other users, like or comment on blogs or archive their own blogs.

## Working Application Snapshots
![Pic1](https://github.com/user-attachments/assets/a42288fa-3a04-44e0-b503-2acda6708e08)
![Pic2](https://github.com/user-attachments/assets/b3dd96a2-930c-4c27-8112-f0a72d8f568a)
![Pic3](https://github.com/user-attachments/assets/8ba16c16-dfa6-453d-aa47-cc95e0acb7d8)
![Pic4](https://github.com/user-attachments/assets/ad5e18fc-8e71-4431-a641-1b0cadade3c0)
![Pic5](https://github.com/user-attachments/assets/49561378-e2cf-4981-9748-89108cf1856f)


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
