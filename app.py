from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import flask.ext.login as flask_login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = 'secret_key_random'  #보안

db = SQLAlchemy(app)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

from flask.ext.misaka import Misaka
Misaka(app)

from models import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.verify_password(password):
                flask_login.login_user(user)
                return redirect('/')
            else:
                return redirect('/')
        else:
            return redirect('/')
@app.route('/auth/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

    if request.method == 'POST':
        user = User(email=request.form['email'])
        user.set_password(request.form['password'])
        user.role = 'user'
        db.session.add(user)
        db.session.commit()
        return redirect('/')
@app.route('/auth/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template('list_post.html', posts=posts)

# 새로운 글 생성
@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'GET':
        return render_template('write_post.html')
    if request.method == 'POST':
        # write post to database
        post = Post(
            title=request.form['title'],
            content=request.form['content']
        )
        db.session.add(post)
        db.session.commit()
        return redirect('/')

# 글 상세 보기
@app.route("/post/<int:id>", methods=['GET'])
def post_detail(id):
    if request.method == 'GET':
        post = Post.query.get(id)
        return render_template('detail_post.html', post=post)

# 기존 글 수정
@app.route('/post/update/<int:id>', methods=['GET', 'POST'])
def post_update(id):
    if request.method == 'GET':
        post = Post.query.get(id)
        return render_template('update_post.html', post=post)
    if request.method == 'POST':
        post = Post.query.get(id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/')

# 글 삭제
@app.route('/post/delete/<path:id>', methods=['POST'])
def post_delete(id):
    if request.method == 'POST':
        post = Post.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
