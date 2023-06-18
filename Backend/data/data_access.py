from data.models import User, Post
from sqlalchemy import desc
from __init_app__ import cache

@cache.memoize(30)
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

@cache.memoize(30)
def get_user_by_userid(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    return user

@cache.memoize(30)
def search_by_query(query, username):
    users = User.query.filter((User.username != username) & (User.username.like(query+'%') | User.name.like(query+'%'))).all()
    return users

@cache.memoize(5)
def get_all_posts_by_users(users):
    posts = Post.query.filter(Post.archieved==False).filter(Post.author.in_(users)).order_by(desc(Post.created_on)).all()
    return posts

def get_post(post_id):
    post = Post.query.filter_by(post_id=post_id).first()
    return post