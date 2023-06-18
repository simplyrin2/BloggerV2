import uuid, os, datetime as dt, base64, re, io, datetime as dt, redis, boto3
from flask import jsonify, make_response, request
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_cors import CORS
from sqlalchemy import desc
from flask_sse import sse
from PIL import Image

# Local module imports
from __init_app__ import app, cache
from data.models import db, User, Post, Like, Comment, Follow, Notification
from data import data_access
import workers
import tasks

api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app, supports_credentials=True, allow_headers=["Content-Type", "Accept", "X-CSRF-TOKEN", "Authorization"])

db.init_app(app)
app.app_context().push()
with app.app_context(): 
    db.create_all()

# ---------------------------------CELERY_WORKERS--------------------------------------

celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND']
)

celery.Task = workers.ContextTask

#--------------------------------REDIS CLIENT---------------------------------------------
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
active_users = 'active_users'

# -----------------------------------CONFIGURATIONS----------------------------------------------
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = dt.timedelta(days=1) 

BUCKET='bloggerv2'
REGION='ap-south-1'

#----------------------------------UTILITY FUNCTIONS------------------------------------
user_username_validate = re.compile('^[a-zA-Z0-9]*$')
user_name_validate = re.compile('^[a-zA-Z]*\s?[a-zA-Z]*$')

def upload_file_1(image, object_name, bucket=BUCKET):
    s3_client = boto3.client('s3')
    format = object_name.split('.')[-1]
    in_mem_file = io.BytesIO()
    image.save(in_mem_file, format=format,quality=95)
    in_mem_file.seek(0)
    response = s3_client.upload_fileobj(in_mem_file, bucket, object_name, ExtraArgs={"ACL": "public-read"})
    return response

def delete_file(object_name, bucket=BUCKET):
    if object_name is None or object_name == '':
        return
    client = boto3.client('s3')
    client.delete_object(Bucket=bucket, Key=object_name)


def check_file(file):
    if '.' not in file:
        return False
    
    allowed_extensions = ['jpg', 'png', 'jpeg']
    extension = file.split('.')[-1].lower()
    print(extension)

    if extension not in allowed_extensions:
        return False
    return True


def check_user_exist(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return True
    return False

def delete_image(filename, bucket=BUCKET):
    if filename is None or filename == '':
        return
    os.remove(os.path.join(app.config['UPLOADS'], filename))
    object_name = filename
    s3_client = boto3.client('s3')
    response = s3_client.delete_object(bucket, object_name)
    return response

def img_url_formatter(filename):
    if filename == None or filename=='':
        return ''
    post_img_url = "https://{bucket_name}.s3.{region_name}.amazonaws.com/{filename}".format(bucket_name=BUCKET, region_name=REGION, filename=filename)
    return post_img_url

def crop_Image(img):
    foo = Image.open(img)
    x,y = foo.size
    print(x,y)

    if x!=y:
        m = min(x,y)
        (l,t) = ((x-m)/2, (y-m)/2)
        foo = foo.crop((l,t,l+m,t+m))
    return foo

def time_stamp(t):
    diff = dt.datetime.now() - t
    t_diff=0
    flag='s'
    if diff.seconds < 60:
        t_diff = int(diff.seconds)
        return [str(t_diff), flag]
    else:
        t_diff = round(diff.seconds / 60)
        flag='min'
        if t_diff >= 60:
            if diff.days >= 1:
                t_diff = round(diff.days)
                flag='d'
            elif diff.days >= 7:
                t_diff = round(diff.days / 7)
                flag='w'
                if t_diff >= 4:
                    t_diff = round(t_diff / 4)
                    flag='mo'
                if t_diff >= 12:
                    t_diff = dt.datetime.strptime(t, "%d %m %y")
                    flag=''
            else:
                t_diff = round(t_diff / 60)
                flag='h'
    return [str(t_diff), flag]

def notification_content_formatter(n):
    content = ''
    if n.type==0:
        content = '@{username} started following you'.format(username=n.username)
    elif n.type==1:
        content = '@{username} liked your post'.format(username=n.username)
    elif n.type==2:
        content = '@{username} commented your post'.format(username=n.username)
    return content

def trigger_notification(to_notify, type, username, post_id=None):
    timestamp = dt.datetime.now()
    n = None
    if type==0:
        n = Notification(timestamp=timestamp, to_notify=to_notify, username=username, type=type)
    else:
        n = Notification(timestamp=timestamp, to_notify=to_notify, id=post_id, username=username, type=type)
    return n

def sse_notification(username):
    sse.publish({'message': 'New notification'}, type=username)

#-----------------------------------------APIs-----------------------------------------------

class SignUpAPI(Resource):
    def post(self):
        form = request.form
        username = form.get('username')
        name = form.get('name')
        password = form.get('password')
        confirm_password = form.get('confirm_password')
        bio = form.get('bio')
        email = form.get('email')

        if not username:
            return make_response(jsonify({'msg': 'Username required'}),409)
        if data_access.get_user_by_username(username):
            return make_response(jsonify({'msg': 'Username already exists'}),409)
        if not name:
            return make_response(jsonify({'msg': 'Name required'}),409)
        if not password:
            return make_response(jsonify({'msg': 'Password required'}),409)
        if password is None or password.strip() == '' or password[0] == ' ' or password[-1] == ' ':
            return make_response(jsonify({'msg': 'Invalid password'}),409)
        if password != confirm_password:
            return make_response(jsonify({'msg': 'Passwords should match'}),409)
        password = password.strip()

        if len(username) < 4 or len(username) > 20 or not user_username_validate.match(username):
            return make_response(jsonify({'msg': 'Invalid username'}),409)
        if len(name) < 2 or len(name) > 50 or not user_name_validate.match(name):
            return make_response(jsonify({'msg': 'Invalid Name'}),409)
        if len(password) < 4:
            return make_response(jsonify({'msg': 'Passwords too small'}),409)
        if len(password) > 20:
            return make_response(jsonify({'msg': 'Passwords too long'}),409)

        hashed_password = bcrypt.generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, name=name, role='USER', email=email)
        image = request.files.get('image')
        if image:
            f_name=secure_filename(image.filename)
            if not check_file(f_name):
                return {"error_code": "IMGERROR", "error_message": "Image extension not supported"}, 400
            format = f_name.split('.')[-1]
            if format.lower() == 'jpg':
                format = 'jpeg'
            filename = str(uuid.uuid4())+"."+format
            image = crop_Image(image)
            upload_file_1(image, filename)
            new_user.pic = filename
        if bio:
            new_user.bio = bio  
        try:
            db.session.add(new_user)
        except:
            db.session.rollback()
        else:
            db.session.commit()
            return make_response(jsonify({'msg':'User created successfully'}), 201)

class VerifyTokenAPI(Resource):
    @jwt_required()
    def get(self):
        response = jsonify({"msg": "Verfied", "username": get_jwt_identity()})
        redisClient.sadd(active_users, get_jwt_identity())
        return make_response(response, 200)

class AccessTokenAPI(Resource):
    def post(self):
        request_body = request.get_json()
        print(request_body)
        username = request_body.get('username')
        password = request_body.get('password')
        print(username, password)
        if username is None:
            return make_response(jsonify({'error_code': 'USER01', 'error_message': 'Username required'}), 404)
        if password is None:
            return make_response(jsonify({'error_code': 'PASS01', 'error_message': 'Password required'}), 404)
        


        user = data_access.get_user_by_username(username)
        if user is None:
            return make_response(jsonify({'msg': 'User not found'}), 404)
        if bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            response = jsonify({'token':access_token, 'username': username})

            redisClient.sadd(active_users, username)
            return make_response(response, 200)
        else:
            return make_response(jsonify({'msg':'Incorrect password'}), 404)

class LogoutAPI(Resource):
    @jwt_required()
    def get(self):
        response = jsonify({"msg": "Logout successful"})
        return response
        
class NotificationsAPI(Resource):
    @jwt_required()
    def get(self):
        user = User.query.filter_by(username=get_jwt_identity()).first()
        output = []
        for n in user.notifications:
            output.append({'not_id': n.notification_id,'content': notification_content_formatter(n), 'timestamp': ' '.join(time_stamp(n.timestamp)), 'type': n.type, 'id': n.id, 'username': n.username})
        return make_response(jsonify(output), 200)
    
    @jwt_required()
    def delete(self, id):
        n = Notification.query.filter_by(notification_id=id).first()
        if n is None:
            return make_response({'msg': 'Not found'}, 404)
        if get_jwt_identity() != n.user.username:
            return make_response({'msg': 'Forbidden'}, 403)
        db.session.delete(n)
        db.session.commit()
        return make_response({'msg': 'Cleared'}, 200)

class FeedAPI(Resource):
    @jwt_required()
    def get(self):
        redisClient.sadd(active_users, get_jwt_identity().encode())
        users=[]
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        for user in current_user.following:
            users.append(user.user_id)
        posts = data_access.get_all_posts_by_users(users)
        output = []
        for post in posts:
            liked = False
            if current_user in post.likes:
                liked= True
            # if len(post.title) > 42:
            #     post.title = post.title[0:43]+'...'
            # if len(post.content) > (56*3-9):
            #     post.content = post.content[0:158]+'...'
            timestamp = ' '.join(time_stamp(post.created_on))
            author = data_access.get_user_by_userid(post.author)
            output.append({'post_id': post.post_id, 'author_name': author.name, 'author_username': author.username, 'title': post.title, 'content': post.content, 'likes': len(post.likes), 'comments': len(post.comments), 'img': img_url_formatter(post.img), 'timestamp': timestamp, 'liked': liked})
        return make_response(jsonify(output), 200)
    
class ViewUserAPI(Resource):
    @jwt_required()
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            return 'User not found', 404
        
        f = False
        current_user = User.query.filter_by(username=get_jwt_identity()).first()
        if username == get_jwt_identity():
            return make_response(jsonify({'msg': 'Not allowed to view'}), 404)
        if user in current_user.following:
            f = True
        if request.args.get('follow'):
            if f==True:
                follow_act = Follow.query.filter_by(follower=current_user.user_id, following=user.user_id).first()
                db.session.delete(follow_act)
                db.session.commit()
                f = False
            else:
                follow_act = Follow(follower=current_user.user_id, following=user.user_id)
                db.session.add(follow_act)
                db.session.commit()
                n=trigger_notification(username, 0, get_jwt_identity())
                db.session.add(n)
                db.session.commit()
                sse_notification(username)
                f = True

        (posts, followers, followings) = ([], [], [])

        for post in user.posts:
            if not post.archieved:
                posts.append({'post_id': post.post_id, 'title': post.title, 'content': post.content, 'like_count': len(post.likes), 'comment_count': len(post.comments), 'img': img_url_formatter(post.img)})
        for follower in user.followers:
            followers.append({'username': follower.username, 'name': follower.name, 'pic': img_url_formatter(follower.pic)})
        
        for following in user.following:
            followings.append({'username': following.username, 'name': following.name, 'pic': img_url_formatter(following.pic)})
        
        return jsonify({'user_id': user.user_id, 'username': user.username, 'name': user.name, 'bio': user.bio, 'pic': img_url_formatter(user.pic), 'followers': followers, 'following': followings, 'posts': posts, 'follow': f})


class UserAPI(Resource):
    @jwt_required()
    def get(self):
        query = request.args.get('search')
        if query:
            output = []
            users = data_access.search_by_query(query, get_jwt_identity())
            for user in users:
                output.append({'user_id': user.user_id, 'username': user.username, 'name': user.name, 'pic': img_url_formatter(user.pic)})
            return make_response(jsonify(output), 200)
        else:
            identify_token_username = get_jwt_identity()
            user = User.query.filter_by(username=identify_token_username).first()
            if user is None:
                return 'User not found', 404
            
            if request.args.get('notifications'):
                output = []
                for n in user.notifications:
                    output.append({'content': n.content, 'timestamp': ' '.join(time_stamp(n.timestamp))})
                return make_response(jsonify(output), 200)

            (posts, followers, followings, archived_posts) = ([], [], [], [])

            for post in user.posts:
                liked = False
                if user in post.likes:
                    liked = True
                p = {'post_id': post.post_id, 'title': post.title, 'content': post.content, 'likes': len(post.likes), 'comments': len(post.comments), 'img': img_url_formatter(post.img), 'timestamp': post.created_on, 'liked': liked}
                if not post.archieved:
                    posts.append(p)
                else:
                    archived_posts.append(p)

            for follower in user.followers:
                followers.append({'username': follower.username, 'name': follower.name, 'pic': img_url_formatter(follower.pic)})
            
            for following in user.following:
                followings.append({'username': following.username, 'name': following.name, 'pic': img_url_formatter(following.pic)})
            
            return jsonify({'user_id': user.user_id, 'username': user.username, 'name': user.name, 'bio': user.bio, 'pic': img_url_formatter(user.pic), 'followers': followers, 'following': followings, 'posts': posts, 'archived_posts': archived_posts, 'email': user.email})

    @jwt_required()
    def put(self):
        identify_token_username = get_jwt_identity()
        user = data_access.get_user_by_username(identify_token_username)

        if not user:
            return make_response(jsonify({'error_code': 'USER05', 'error_message': 'User not found'}), 404)
        
        form = request.form
        username = form.get('username')
        name = form.get('name')
        bio = form.get('bio')
        email = form.get('email')
        imgChanged = form.get('imgChanged')
        print(imgChanged)
        if not username:
            return make_response(jsonify({'error_code': 'USER01', 'error_message': 'Username is required'}), 400)
        if not name:
            return make_response(jsonify({'error_code': 'USER02', 'error_message': 'Name is required'}), 400)

        if name.strip() == '':
            return make_response(jsonify({'error_code': 'USER03', 'error_message': 'Name cannot be null'}), 400)

        if identify_token_username != username:
            any_user = data_access.get_user_by_username(username)
            if any_user:
                return make_response(jsonify({'error_code': 'USER04', 'error_message': 'User with username already exits!'}), 400)
        user.username = username
        user.name = name
        user.bio = bio
        user.email = email

        if imgChanged:
            image = request.files.get('image')
            if image:
                f_name=secure_filename(image.filename)
                if not check_file(f_name):
                    return {"error_code": "IMGERROR", "error_message": "Image extension not supported"}, 400
                
                format = f_name.split('.')[-1]
                if format.lower() == 'jpg':
                    format = 'jpeg'
                filename = str(uuid.uuid4())+"."+format
                image = crop_Image(image)
                upload_file_1(image, filename)
                delete_file(user.pic)
                user.pic = filename
            else:
                delete_file(user.pic)
                user.pic = None

        db.session.add(user)
        db.session.commit()
        return make_response(jsonify({'msg': 'User updated successfully'}), 201)

    @jwt_required()
    def delete(self):
        # # user = User.query.filter_by(username=username).first()
        # if user is None:
        #     return 'User not found', 404

        # identify_token_username = get_jwt_identity()
        # if identify_token_username != username:
        #     return 'You are not permitted!', 403

        # delete_image(user.pic)
        # db.session.delete(user)
        # db.session.commit()
        return 'Not Deleted', 404
    
class LikesAPI(Resource):
    def get(self, post_id):
        post = data_access.get_post(post_id)
        if post is None:
            return make_response(jsonify({"msg": "Post not found"}), 404)
        likes = []
        for like in post.likes:
            likes.append({'username': like.username, 'name': like.name, 'pic': img_url_formatter(like.pic)})
        return make_response(jsonify(likes), 200)
    
    @jwt_required()
    def post(self, post_id):
        post = data_access.get_post(post_id)
        if post is None:
            return make_response(jsonify({"msg": "Post not found"}), 404)
        user = User.query.filter_by(username=get_jwt_identity()).first()
        if user in post.likes:
            post.likes.remove(user)
            db.session.add(post)
            db.session.commit()
            return make_response(jsonify({'like_status': 'Not Liked'}), 200)
        else:
            post.likes.append(user)
            db.session.add(post)
            db.session.commit()
            if post.created_by.username != get_jwt_identity():
                n=trigger_notification(post.author, 1, get_jwt_identity(), post_id)
                db.session.add(n)
                db.session.commit()
                sse_notification(post.created_by.username)
            return make_response(jsonify({'like_status': 'Liked'}), 200)


class CommentsAPI(Resource):
    @cache.memoize(50)
    def get(self, post_id):
        post = data_access.get_post(post_id)
        if post is None:
            return make_response(jsonify({"msg": "Post not found"}), 404)
        comments = []
        for comment in post.comments:
            c = {'username': comment.comment_by.username, 'name': comment.comment_by.name, 'comment': comment.comment, 'comment_id': comment.comment_id}
            comments.append(c)
        return make_response(jsonify({'comments': comments}), 200)
    
    @jwt_required()
    def post(self, post_id):
        post = data_access.get_post(post_id)
        if post is None or post.archieved:
            return make_response(jsonify({'msg': 'Post does not exist'}), 404)
        
        text = request.args.get('comment')
        if len(text) == 0:
            return make_response(jsonify({'msg': 'Comment blank'}), 403)
        if len(text) > 200:
            return make_response(jsonify({'msg': 'Comment length exceeded'}), 403)
        cache.delete_memoized(CommentsAPI.get, post_id)
        cache.delete_memoized(PostAPI.get, post_id)
        identify_token_username = get_jwt_identity()
        user = data_access.get_user_by_username(identify_token_username)
        comment = Comment(comment_by=user.user_id, comment=text)
        post.comments.append(comment)
        db.session.add(post)
        db.session.commit()
        if post.created_by.username != identify_token_username:
            n=trigger_notification(post.author, 2, get_jwt_identity(), post_id)
            db.session.add(n)
            db.session.commit()
            sse_notification(post.created_by.username)
        return make_response(jsonify({'username': identify_token_username, 'name': user.name, 'comment': text, 'comment_id': comment.comment_id}), 201)
    
    @jwt_required()
    def delete(self, comment_id):
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        if comment.commentor.username == get_jwt_identity() or comment.post.created_by.username == get_jwt_identity():
            cache.delete_memoized(CommentsAPI.get, comment.post.post_id)
            cache.delete_memoized(PostAPI.get, comment.post.post_id)
            db.session.delete(comment)
            db.session.commit()
            return make_response(jsonify({'msg':'Comment deleted'}), 200)
        return make_response(jsonify({'msg': 'Something went wrong'}), 404)


class PostAPI(Resource):
    @jwt_required()
    def post(self):
        identify_token_username = get_jwt_identity()
        user = data_access.get_user_by_username(identify_token_username) 

        print(request.files)
        form = request.form
       
        title = form.get('title')
        if title is None:
            return {'error_code': 'POST01', 'error_message': 'Title is required'}, 400
        if title.strip() == '':
            return {'error_code': 'POST02', 'error_message': 'Title cannot be null'}, 400
        content = form.get('content')
        if content is None:
            return {'error_code': 'POST03', 'error_message': 'Content is required'}, 400
        if content.strip() == '':
            return {'error_code': 'POST04', 'error_message': 'Content cannot be null'}, 400
        
        time=dt.datetime.now()
        post = Post(author=user.user_id, title=title, content=content, created_on=time)
        if request.files.get('image'):
            image = request.files.get('image')
            f_name=secure_filename(image.filename)
            if not check_file(f_name):
                return {"error_code": "IMGERROR", "error_message": "Image extension not supported"}, 400
            format = f_name.split('.')[-1]
            if format.lower() == 'jpg':
                format = 'jpeg'
            filename = str(uuid.uuid4())+"."+format
            image = Image.open(image)
            upload_file_1(image, filename)
            post.img = filename

        db.session.add(post)
        db.session.commit()

        return {'post_id': post.post_id, 'title': post.title, 'content': post.content, 'image_url': img_url_formatter(post.img)}, 201
        
    @jwt_required()
    @cache.memoize(50)
    def get(self, post_id):
        post = data_access.get_post(post_id)

        if post is None:
            return 'Post not found', 404
        

        (likes, comments, liked) = ([], [], False)
        for like in post.likes:
            likes.append({'username': like.username, 'name': like.name, 'pic': img_url_formatter(like.pic)})
            if like.username == get_jwt_identity():
                liked = True
        for comment in post.comments:
            user = User.query.filter_by(user_id=comment.comment_by).first()
            comments.append({'comment': comment.comment, 'username': user.username, 'name': user.name, 'comment_id': comment.comment_id})

        return make_response(jsonify({'post_id': post.post_id, 'title': post.title, 'content': post.content, 'likes': likes, 'comments': comments, 'image': img_url_formatter(post.img), 'timestamp': post.created_on, 'author_name': post.created_by.name, 'username': post.created_by.username, 'liked': liked}), 200)

    @jwt_required()
    def put(self, post_id):
        post = data_access.get_post(post_id)
        if post is None:
            return make_response(jsonify({'msg':'Post not found'}), 404)
        
        identify_token_username = get_jwt_identity()
    
        if identify_token_username != post.created_by.username:
            return make_response(jsonify({'msg': 'You are not permitted'}), 403)

        form = request.form
        title = form.get('title')
        content = form.get('content')
        imgChanged = form.get('imgChanged')
        if title is None:
            return make_response(jsonify({'error_message': 'Title is required'}, 400))
        if content is None:
            return make_response(jsonify({'error_message': 'Content is required'}, 400))
        if content.strip() == '':
            return make_response(jsonify({'error_message': 'Content cannot be null'}, 400))
        
        cache.delete_memoized(PostAPI.get, post_id)
        
        if imgChanged:
            if request.files.get('image'):
                image = request.files.get('image')
                f_name=secure_filename(image.filename)
                if not check_file(f_name):
                    return make_response(jsonify({"error_code": "IMGERROR", "error_message": "Image extension not supported"}), 400)
                
                format = f_name.split('.')[-1]
                if format.lower() == 'jpg':
                    format = 'jpeg'
                filename = str(uuid.uuid4())+"."+format
                image = Image.open(image)
                upload_file_1(image, filename)
                delete_file(post.img)
                post.img = filename
            else:
                delete_file(post.img)
                post.img = None

        post.title = title
        post.content = content

        db.session.add(post)
        db.session.commit()
        return make_response(jsonify({'post_id': post.post_id, 'title': post.title, 'content': post.content, 'like_count': len(post.likes), 'comment_count': len(post.comments), 'image': img_url_formatter(post.img)}), 201)

    @jwt_required()
    def delete(self, post_id):
        post = data_access.get_post(post_id)
        
        if post is None:
            return make_response(jsonify({'msg': 'Post not found'}), 404)
        identify_token_username = get_jwt_identity()
    
        if identify_token_username != post.created_by.username:
            return make_response(jsonify({'msg': 'You are not permitted'}), 403)
        
        cache.delete_memoized(PostAPI, post_id)
        cache.delete_memoized(CommentsAPI, post_id)

        if post.img is not None:
            delete_file(post.img)
        likes = Like.query.filter_by(post_id=post_id).all()
        for like in likes:
            db.session.delete(like)
        for comment in post.comments:
            db.session.delete(comment)
        db.session.delete(post)
        db.session.commit()
        return make_response(jsonify({'msg': 'Post deleted successfully'}), 200)
    
class ExportcsvAPI(Resource):
    @jwt_required()
    def get(self):
        token_username = get_jwt_identity()
        user = User.query.filter_by(username=token_username).first()
        print(user.posts)
        if len(user.posts) == 0:
            return make_response({'msg': 'You have not posted anything yet.'}, 404)
        if not user.email:
            sse.publish({'message': 'You have not provided any email'}, type='exportcsv')
            return make_response({'msg': 'You have not provided any email.'}, 404)
        result = tasks.exportCSV.delay(token_username)
        return make_response({'msg': 'Job started'}, 200)

api.add_resource(SignUpAPI, '/api/signup')
api.add_resource(AccessTokenAPI, '/api/access_token')
api.add_resource(LogoutAPI, '/api/logout')
api.add_resource(UserAPI, '/api/user')
api.add_resource(ViewUserAPI, '/api/user/<string:username>')
api.add_resource(PostAPI,'/api/post/<int:post_id>', '/api/post')
api.add_resource(LikesAPI, '/api/post/<int:post_id>/likes', '/api/post/<int:post_id>/like')
api.add_resource(CommentsAPI, '/api/post/<int:post_id>/comments', '/api/comment/<int:comment_id>')
api.add_resource(NotificationsAPI, '/api/notifications', '/api/notifications/<int:id>')
api.add_resource(VerifyTokenAPI, '/api/verify')
api.add_resource(FeedAPI, '/api/feed')
api.add_resource(ExportcsvAPI, '/api/exportcsv')

if __name__=='__main__':
    app.run(debug=True)