import os
from flask import render_template, url_for, flash, redirect, request
from gymbo import app, db, bcrypt
from gymbo.models import User, Lift, UserLift
from gymbo.forms import RegistrationForm, LoginForm, UpdateProfileForm, UpdateLiftForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    else:
        profile_pic = url_for('static', filename='profile_pics/default.jpg')
    return render_template('home.html', profile_pic=profile_pic, title='Gymbo')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(profile))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Create hashed password to store in db
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(profile))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

#Saves uploaded profile pic to fs
def save_pic(pic):
    #random_hex = secrets.token_hex(8)
    #_, f_ext = os.path.splitext(pic.filename)
    #picture_fn = random_hex + f_ext
    picture_fn = pic.filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    pic.save(picture_path)

    return picture_fn

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateLiftForm()
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    bench = UserLift.query.filter_by(userid=current_user.id, liftid=form.bench_id).first()
    squat = UserLift.query.filter_by(userid=current_user.id, liftid=form.squat_id).first()
    front_squat = UserLift.query.filter_by(userid=current_user.id, liftid=form.front_squat_id).first()
    deadlift = UserLift.query.filter_by(userid=current_user.id, liftid=form.deadlift_id).first()
    if form.validate_on_submit():
        max_bench = UserLift(userid=current_user.id, liftid=form.bench_id, current_lift=form.bench_press.data, max_lift=form.bench_press.data)
        max_squat = UserLift(userid=current_user.id, liftid=form.squat_id, current_lift=form.squat.data, max_lift=form.squat.data)
        max_front_squat = UserLift(userid=current_user.id, liftid=form.front_squat_id, current_lift=form.front_squat.data, max_lift=form.front_squat.data)
        max_deadlift = UserLift(userid=current_user.id, liftid=form.deadlift_id, current_lift=form.deadlift.data, max_lift=form.deadlift.data)
        if bench:
            bench.current_lift = form.bench_press.data
            if bench.current_lift > bench.max_lift:
                bench.max_lift = form.bench_press.data
        else:
            db.session.add(max_bench)
        if squat:
            squat.current_lift = form.squat.data
            if squat.current_lift > squat.max_lift:
                squat.max_lift = form.squat.data
        else:
            db.session.add(max_squat)
        if front_squat:
            front_squat.current_lift = form.front_squat.data
            if front_squat.current_lift > front_squat.max_lift:
                front_squat.max_lift = form.front_squat.data
        else:
            db.session.add(max_front_squat)
        if deadlift:
            deadlift.current_lift = form.deadlift.data
            if deadlift.current_lift > deadlift.max_lift:
                deadlift.max_lift = form.deadlift.data
        else:
            db.session.add(max_deadlift)
        db.session.commit()
        flash('Lifts updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        if bench:
            form.bench_press.data = bench.current_lift
        else:
            form.bench_press.data = 0
        if squat:
            form.squat.data = squat.current_lift
        else:
            form.squat.data = 0
        if front_squat:
            form.front_squat.data = front_squat.current_lift
        else:
            form.front_squat.data = 0
        if deadlift:
            form.deadlift.data = deadlift.current_lift
        else:
            form.deadlift.data = 0
    return render_template('profile.html', profile_pic=profile_pic, form=form, title='Profile', lifts=[bench, squat, front_squat, deadlift])

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/update", methods=['POST', 'GET'])
@login_required
def update():
    form = UpdateProfileForm()
    #Allows users to update username/email/profile picture information to db
    if form.validate_on_submit():
        #Sets uploaded image to profile picture
        if form.pic.data:
            picture_file = save_pic(form.pic.data)
            current_user.profile_pic = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your accout has been updated', 'success')
        return redirect(url_for('profile'))
    #Puts current data inside form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_pic = url_for('static', filename='profile_pics/' + current_user.profile_pic)
    return render_template('update.html', form=form, profile_pic=profile_pic, title='Profile Update')
