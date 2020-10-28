from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, TrialForm
from app.models import User, Trial
from app.params import *

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = TrialForm()
    num_completed_trials = current_user.trials.count()
    cur_card = CARD_ORDER[min(num_completed_trials, len(CARD_ORDER)-1)]
    cur_answer = ANSWER[num_completed_trials]
    if sum(cur_answer) == 1:
        cur_answer = cur_answer.index(1)
    if form.validate_on_submit():
        trial = Trial(body=form.chosen_bin.data, author=current_user, trial_num=num_completed_trials+1)
        db.session.add(trial)
        db.session.commit()
        flash('You chose {} and correct answer is bin{}'.format(form.chosen_bin.data, cur_answer))
        return redirect(url_for('index'))
    return render_template("index.html", title='Home Page', form=form, num_bins=NUM_BINS, card=cur_card, num_completed_trials=num_completed_trials, num_trials=NUM_TRIALS)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)