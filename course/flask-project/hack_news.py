from flask import render_template, request, redirect, url_for, session, flash, json, jsonify
from flask.ext.login import LoginManager, login_user, login_required
from sqlalchemy import desc 

from config import app, db
from forms import HackNewsUserForm, HackNewsPostForm
from models import User, Post 


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signup'


@login_manager.user_loader
def load_user(user):
    print user 
    return User.query.get(user)


@app.route("/", methods=["GET", "POST"])
def home():
    
    # demonstrating how we can simply update the database
    # post4 = Post.query.get(5)
    # post4.points += 301
    # db.session.add(post4)
    # db.session.commit()
 
    all_posts = Post.query.order_by(desc(Post.points))
    return render_template("home.html", all_posts=all_posts)


@app.route("/submit", methods=["GET", "POST"])
def submit():
    print "hit submit route, now to execute posting to the form"

    hack_news_submit_form = HackNewsPostForm(request.form)
    error = None
    print "session: ", session 
    print "request.form: {}".format(request.form)
    
    if request.method == "POST":
        print "method was post", request.method
        if hack_news_submit_form.validate_on_submit():
            print "form validated"
            post = Post(hack_news_submit_form.title.data, 
                        hack_news_submit_form.url.data, 
                        'test_user')
            db.session.add(post)
            db.session.commit()

            return redirect(url_for('home'))

    return render_template("submit.html", hack_news_submit_form=hack_news_submit_form, error=error)


@app.route("/signup", methods=["GET", "POST"]) 
def signup():
    print 'request.args: ', request.args

    signup_form = HackNewsUserForm(request.form)
    error = None

    if request.method == "POST":
        print 'posted: ', request.method
        if signup_form.validate_on_submit():

            user = User(signup_form.name.data,
                        signup_form.password.data,
                        signup_form.email.data)

            db.session.add(user)
            db.session.commit()

            flash('Logged in successfully.')
            login_user(user)

            print 'request.args: ', request.args
            print 'session: ', session
            print "request.args.get('next'): ", request.args.get('next')
            print "user: ", user

            return redirect(url_for('hello_again'))

    return render_template("signup.html", signup_form=signup_form, error=error)


#displays users to be deleted in final project
@app.route("/hi", methods=["GET", "POST"])
@login_required
def hello_again():
    all_users = User.query.all()
    return render_template("custom_hello.html", all_users=all_users)

@app.route('/signup_user', methods=["GET", "POST"])
def sign_up_user():
    user =  request.form['username']
    password = request.form['password']
    print user, password
    return json.dumps({'status':'OK','user':user,'pass':password})

@app.route('/ok', methods=["GET", "POST"])
def upvote():
    voted = request.form.items()
    print 'voted', voted
    vote = list(request.form.to_dict())
    print vote
    try:
        vote_id = int(vote.pop())
    except:
        vote_id = 0
    #query db by vote_id
    print 'vote_id', vote_id
    post_by_id = Post.query.filter_by(id=vote_id).first()
    print post_by_id
    #add 1 to points count
    post_by_id.points += 1
    # save to db
    db.session.add(post_by_id)
    db.session.commit()


    # print dir(request.form)
    print "vote_id", vote_id, "this was vote_id"
    print "vote", vote_id, "this was vote"
    print "request.args", request.args 
    dat = request.args.get('z', 1, type=int)
    dat2 = request.args.get('data', 1, type=int)
    dat3 = request.args.get('upvote_id', 1, type=int)
    print dat, dat2, dat3, "dats"
    print "request.form", request.form
    return json.dumps({'status':'OK', 'vote id':vote_id, 'dat':dat,'dat2':dat2, 'dat3':dat3})

@app.route('/server_add', methods=["GET", "POST"])
def server_add():
    print "request.args", request.args


@app.route('/_add_numbers', methods=["GET", "POST"])
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print a, b
    c = request.args.get('c', 0, type=int)
    print 'c', c
    print 'request.args', request.args 
    print jsonify(result = a+b)
    print jsonify({'value of c': c})
    return jsonify(result = a+b)

@app.route('/_more_add_numbers', methods=["GET", "POST"])
def more_add_numbers():
    print 'request.args', request.args
    e_num = request.args.get('e', type=int)
    print e_num
    return jsonify({e_num: e_num})

if __name__ == '__main__':
    app.run(debug=True)