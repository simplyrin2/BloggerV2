# BloggerV2
#### Version 2 of the blogging application Blogger

BloggerV2 is a multi-user application for you can upload and engage with blogs. The application allows one to create blogs, follow/unfollow other users, like or comment on blogs or archive their own blogs.

## Working Application Snapshots
![Pic1](https://github.com/user-attachments/assets/24f734a2-12ba-4a3b-a52d-15e9c63915cc)
![Pic2](https://github.com/user-attachments/assets/97c1a792-c41f-42f9-874b-129f51f98ba0)
![Pic3](https://github.com/user-attachments/assets/d18e5995-1c88-479c-9359-b230896eac95)
![Pic4](https://github.com/user-attachments/assets/e620cd57-b913-4f47-8797-442c946e6d21)
![Pic5](https://github.com/user-attachments/assets/9ae23e1f-f7fd-4096-911e-10929b2d3537)
![Pic6](https://github.com/user-attachments/assets/10e9347c-a58a-4def-8688-a5c9f86b9d69)
![Pic7](https://github.com/user-attachments/assets/370af614-27b1-42c0-ab7e-d3daf6588c68)


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
