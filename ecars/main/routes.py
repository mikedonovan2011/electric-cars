from flask import render_template, request, Blueprint
from ecars.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)  # i.e. http://localhost:5000/?page=1
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  # desc = descending
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')


@main.route("/test", methods=['GET', 'POST'])
def test():
    from flask import make_response, current_app
    #response = make_response('<h1>Bad Request!</h1>')
    #response.status_code = 400
    #return response

    from ecars.main.test_form import NameForm
    from flask import Flask, render_template, session, redirect, url_for

    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('main.test'))  # Post/Redirect/Get pattern; force a get of this page again
    return render_template('test.html', title='Oops', name=session.get('name'), form=form)
