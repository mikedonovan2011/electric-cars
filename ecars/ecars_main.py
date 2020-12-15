
from flask import Flask, render_template, url_for, flash, redirect
from ecars.forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '9b7a4b42d9f5b0e3426016fcbc9c5c89'   #environment variable at some point

posts = [
    {
        'author': 'Mike',
        'title': 'Blog Post 1',
        'content': 'This is the content of the first post.',
        'date_posted': '13 Dec 2020'
    },
    {
        'author': 'Chanel',
        'title': 'Blog Post 2',
        'content': 'This is the content of the second post.',
        'date_posted': '14 Dec 2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
