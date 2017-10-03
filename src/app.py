from flask import Flask, render_template, request, session, make_response

from src.models.blog import Blog
from src.models.common.database import Database
from src.models.user import User

app = Flask(__name__)
app.secret_key = "Password@1$"


@app.route('/')
def home():
    return render_template('home.html')


@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        email = session['email']
        user = User.get_by_email(email)
        return render_template("profile.html", name=user.name)
    else:
        session['email'] = None

    return render_template("profile.html", email=session['email'])


@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    User.register(name, email, password)
    user = User.get_by_email(email)

    return render_template("profile.html", name=user.name)


@app.route('/auth/logout')
def logout():
    User.logout()
    return render_template("home.html")


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, name=user.name)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        new_blog = Blog(user.name, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


if __name__ == '__main__':
    app.run()
