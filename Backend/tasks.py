from workers import celery
import datetime
from celery.schedules import crontab
from jinja2 import Template
from weasyprint import HTML
import smtplib, os, boto3, io, redis, requests, uuid
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask_sse import sse
from requests.exceptions import RequestException
from flask import send_file

from data.models import User
from data import data_access

SMTP_SERVER_HOST = "smtp.gmail.com"
SMTP_SERVER_PORT = 465
SENDER_ADDRESS = os.environ.get('SENDER_EMAIL_ADDRESS')
SENDER_PASSWORD = os.environ.get('SENDER_EMAIL_PASSWORD')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
BUCKET = 'bloggerv2'

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
active_users = 'active_users'

def send_email(to_address, subject, message, content="text", attachment_file=None):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    if content.lower() == "html":
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain')) 

    if attachment_file:
        with open(attachment_file, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())  
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment_file}") 
        msg.attach(part)    

    s = smtplib.SMTP_SSL(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

def img_url_formatter(filename, BUCKET='bloggerv2', REGION='ap-south-1'):
    if filename == None or filename=='':
        return ''
    post_img_url = "https://{bucket_name}.s3.{region_name}.amazonaws.com/{filename}".format(bucket_name=BUCKET, region_name=REGION, filename=filename)
    return post_img_url

def format_report(template_file, data={}):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data)
    
def create_pdf(data):
    message= format_report("emailTemplate.html", data=data)
    html = HTML(string=message)
    file_name = str(uuid.uuid4()) + '.pdf'
    print(file_name)
    html.write_pdf(target=file_name)

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=18, minute=0), daily_reminder.s(), name='Daily Reminder')
    sender.add_periodic_task(crontab(0, 0, day_of_month='1'), monthly_report.s(), name='Monthly Report')

# ---------------------------------------------------------TASKS---------------------------------------------------------

    
@celery.task(autoretry_for=(RequestException,), max_retries= 5, retry_backoff=True)
def daily_reminder():
    l = []
    for username in redisClient.smembers(active_users):
        l.append(username.decode('utf-8'))
    inactive_users = User.query.filter((User.username.notin_(l))).all()
    msg = ''
    for u in inactive_users:
        msg += '@{} '.format(u.username)
    print(msg)
    if msg == '':
        print("NO INACTIVE USERs TODAY")
        return '',200
    data = {"text": msg+"You have not visited today!"}
    post_response = requests.post(WEBHOOK_URL, json=data)
    print(post_response.json())
    while(redisClient.scard(active_users) > 0):
        redisClient.spop(active_users)

@celery.task(autoretry_for=(RequestException,), max_retries=5, retry_backoff=True)
def monthly_report():
    users = User.query.all()
    for user in users:
        data = {'name': user.name, 'username': user.username,'pic': img_url_formatter(user.pic),'followers': len(user.followers), 'following': len(user.following), 'total_posts': 0,'total_likes': 0, 'total_comments': 0}
        for post in user.posts:
            today = datetime.date.today()
            first = today.replace(day=1)
            last_month = first - datetime.timedelta(days=1)
            if last_month.month != 12 and last_month.month==post.created_on.month:
                data['total_posts'] += 1
                data['total_likes'] += len(post.likes)
                data['total_comments'] += len(post.comments)
            if last_month.month == 12 and last_month.month==post.created_on.month and last_month.year==(post.created_on.year-1):
                data['total_posts'] += 1
                data['total_likes'] += len(post.likes)
                data['total_comments'] += len(post.comments)

        if user.email:
            send_email(user.email, subject="Monthly Report for Bloggerv2", message=format_report(template_file='emailTemplate.html',data=data), content='html')
        print(data)

@celery.task(autoretry_for=(RequestException,), max_retries=5, retry_backoff=True)
def exportCSV(username):
    user = User.query.filter_by(username=username).first()
    if user.email:
        with open('export.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["SNo", "Title", "Content", "Image", "Created On"])
            i=1
            for post in user.posts:
                if not post.archieved:
                    writer.writerow([i, post.title, post.content, img_url_formatter(post.img), post.created_on])
                    i = i+1
            file.close()
        send_email(user.email, subject="Blogs as CSV", message="Attached is a CSV file.", content='html', attachment_file='export.csv')
        sse.publish({'message': 'The CSV file has been sent to your email'}, type='exportcsv')

