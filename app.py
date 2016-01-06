from flask import Flask, render_template, request, redirect
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
    posts = Post.query.all()
    return render_template('list_post.html', posts=posts)

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

if __name__ == '__main__':
    app.run(debug=True)
