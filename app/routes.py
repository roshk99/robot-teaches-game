from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, TrialForm, ClearTrialForm, DemoForm, ClearDemoForm
from app.models import User, Trial, Demo
from app.params import *
from app.utils import rules_to_str, str_to_rules


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    clear_trial = ClearTrialForm()
    clear_demo = ClearDemoForm()

    if clear_trial.submit_trial.data and clear_trial.validate_on_submit():
        current_user.trials.delete()
        db.session.commit()
        flash("All Trials Deleted!")
        return redirect(url_for("index"))

    if clear_demo.submit_demo.data and clear_demo.validate_on_submit():
        current_user.demos.delete()
        db.session.commit()
        flash("All Demonstrations Deleted!")
        return redirect(url_for("index"))

    num_completed_trials = current_user.trials.count()
    num_completed_demos = current_user.demos.count()

    return render_template("index.html",
                           title="Home Page",
                           clear_trial_form=clear_trial,
                           clear_demo_form=clear_demo,
                           num_completed_trials=num_completed_trials,
                           num_trials=NUM_TRIALS,
                           num_completed_demos=num_completed_demos,
                           num_demos=NUM_DEMOS)


@app.route("/trials", methods=["GET", "POST"])
@login_required
def trials():
    form = TrialForm()
    num_completed_trials = current_user.trials.count()
    cur_card = CARD_ORDER[min(num_completed_trials, len(CARD_ORDER) - 1)]
    cur_answer = ANSWER[min(num_completed_trials, len(CARD_ORDER) - 1)]
    feedback = []
    for ii, answer in enumerate(cur_answer):
        if answer == 0:
            feedback.append("Incorrect!")
        else:
            feedback.append("Correct!")
            correct_bin = ii

    if form.validate_on_submit():
        chosen_bin = int(form.chosen_bin.data[3])
        trial = Trial(author=current_user,
                      trial_num=num_completed_trials + 1,
                      card_num=cur_card,
                      correct_bin=correct_bin,
                      chosen_bin=chosen_bin,
                      feedback_given=feedback[chosen_bin],
                      feedback_type="text",
                      rule_set=rules_to_str(RULES))
        db.session.add(trial)
        db.session.commit()
        if num_completed_trials < NUM_TRIALS:
            return redirect(url_for("trials"))
        else:
            return redirect(url_for("index"))
    if num_completed_trials < NUM_TRIALS:
        return render_template("trials.html",
                               title="Trials",
                               form=form,
                               num_bins=NUM_BINS,
                               card=cur_card,
                               num_completed_trials=num_completed_trials,
                               num_trials=NUM_TRIALS,
                               feedback=feedback)
    else:
        return redirect(url_for("index"))


@app.route("/demos", methods=["GET", "POST"])
@login_required
def demos():
    form = DemoForm()
    num_completed_demos = current_user.demos.count()
    cur_card = CARD_ORDER_DEMO[min(num_completed_demos,
                                   len(CARD_ORDER_DEMO) - 1)]
    cur_answer = ANSWER_DEMO[min(num_completed_demos,
                                 len(CARD_ORDER_DEMO) - 1)]

    for ii, answer in enumerate(cur_answer):
        if answer == 1:
            correct_bin = ii

    if form.validate_on_submit():
        demo = Demo(author=current_user,
                    demo_num=num_completed_demos + 1,
                    card_num=cur_card,
                    correct_bin=correct_bin,
                    rule_set=rules_to_str(RULES))
        db.session.add(demo)
        db.session.commit()
        if num_completed_demos < NUM_DEMOS:
            return redirect(url_for("demos"))
        else:
            return redirect(url_for("index"))
    if num_completed_demos < NUM_DEMOS:
        return render_template("demos.html",
                               title="Demonstrations",
                               form=form,
                               num_bins=NUM_BINS,
                               card=cur_card,
                               correct_bin=correct_bin,
                               num_completed_demos=num_completed_demos + 1,
                               num_demos=NUM_DEMOS)
    else:
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)