from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Follow(db.Model):
    __tablename__ = 'follow'
    follower = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)
    following = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)

class User(db.Model):
    __tablename__='user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    pic = db.Column(db.String)
    bio = db.Column(db.String(100))
    email = db.Column(db.String(30))
    followers = db.relationship('User', secondary='follow',  primaryjoin='User.user_id==follow.c.following', secondaryjoin='User.user_id==follow.c.follower', uselist=True, back_populates='following', order_by='user.c.name')
    following = db.relationship('User', secondary='follow', primaryjoin='User.user_id==follow.c.follower', secondaryjoin='User.user_id==follow.c.following', foreign_keys='user.c.user_id', uselist=True, back_populates='followers', order_by='user.c.name')

    posts = db.relationship('Post', uselist=True, backref='created_by', order_by='post.c.created_on.desc()', cascade='all, delete', lazy='subquery')
    comments = db.relationship('Comment', uselist=True, backref='commentor', cascade='all, delete')
    notifications = db.relationship('Notification', uselist=True, backref='user', primaryjoin='User.user_id==notification.c.to_notify', cascade='all, delete', order_by='notification.c.timestamp.desc()')

    def get_role(self):
        return self.role

    def get_id(self):
        return self.user_id
    
class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    img = db.Column(db.String)
    created_on = db.Column(db.DateTime, nullable=False)
    archieved = db.Column(db.Boolean, default=False)
    likes = db.relationship('User', secondary='like', primaryjoin='Post.post_id==like.c.post_id', secondaryjoin='User.user_id==like.c.liked_by', uselist=True, backref='post', lazy='subquery')
    comments = db.relationship('Comment', uselist=True, backref='post', cascade='all, delete', lazy='subquery')

class Like(db.Model):
    __tablename__ = 'like'
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='CASCADE'), primary_key=True)
    liked_by = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True)

class Comment(db.Model):
    __tablename__= 'comment'
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id', ondelete='CASCADE'))
    comment_by = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    comment = db.Column(db.String, nullable='False')

class Notification(db.Model):
    __tablename__='notification'
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    to_notify = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    timestamp = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer)
    username = db.Column(db.String)
    seen = db.Column(db.Boolean, default=False)


