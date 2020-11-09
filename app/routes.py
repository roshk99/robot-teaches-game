from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, TrialForm, ClearTrialForm, DemoForm, ClearDemoForm, ConsentForm, TrainingForm, SurveyForm, ClearConsentForm, ClearTrainingForm, ClearSurveyForm
from app.models import User, Trial, Demo
from app.params import *
from utils import rules_to_str, str_to_rules


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    clear_trial = ClearTrialForm()
    clear_demo = ClearDemoForm()
    clear_consent = ClearConsentForm()
    clear_training = ClearTrainingForm()
    clear_survey = ClearSurveyForm()

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
    
    if clear_consent.submit_consent.data and clear_consent.validate_on_submit():
        current_user.consent = None
        db.session.commit()
        flash("Consent Deleted!")
        return redirect(url_for("index"))
    
    if clear_training.submit_training.data and clear_training.validate_on_submit():
        current_user.training = None
        db.session.commit()
        flash("Training Deleted!")
        return redirect(url_for("index"))
    
    if clear_survey.submit_survey.data and clear_survey.validate_on_submit():
        current_user.robot_teaching = None
        current_user.user_learning = None
        db.session.commit()
        flash("All Survey Responses Deleted!")
        return redirect(url_for("index"))

    return render_template("index.html",
                           title="Home Page",
                           clear_trial_form=clear_trial,
                           clear_demo_form=clear_demo,
                           clear_consent_form=clear_consent,
                           clear_training_form=clear_training,
                           clear_survey_form=clear_survey,
                           num_completed_trials=current_user.trials.count(),
                           num_trials=NUM_TRIALS,
                           num_completed_demos=current_user.demos.count(),
                           num_demos=NUM_DEMOS,
                           consent=current_user.consent,
                           training=current_user.training,
                           survey=current_user.robot_teaching,
                           debug_mode=DEBUG_MODE)

@app.route("/consent", methods=["GET", "POST"])
@login_required
def consent():
    form = ConsentForm()
    if form.validate_on_submit():
        current_user.consent = 1
        db.session.commit()
        redirect(url_for("index"))
    if current_user.consent:
        flash("Consent already completed!")
        return redirect(url_for("index"))
    else:
        return render_template("consent.html", title="Consent", form=form)

@app.route("/training", methods=["GET", "POST"])
@login_required
def training():
    form = TrainingForm()
    if form.validate_on_submit():
        current_user.training = 1
        db.session.commit()
        redirect(url_for("index"))
    if current_user.training:
        flash("Training already completed!")
        return redirect(url_for("index"))
    elif not current_user.consent:
        flash("Consent not yet completed!")
        return redirect(url_for("index"))
    else:
        return render_template("training.html", title="Training", form=form)

@app.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        current_user.robot_teaching = form.robot_teaching.data
        current_user.user_learning = form.user_learning.data
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.ethnicity = form.ethnicity.data
        current_user.education = form.education.data
        current_user.robot = form.robot.data
        db.session.commit()
        redirect(url_for("index"))

    num_completed_trials=current_user.trials.count()
    num_completed_demos=current_user.demos.count()
    if current_user.robot_teaching:
        flash("You have completed the survey!")
        return redirect(url_for("index"))
    else:
        if current_user.consent and num_completed_demos == NUM_DEMOS and num_completed_trials == NUM_TRIALS and current_user.training:
            return render_template("survey.html", methods=["GET", "POST"], form=form)
        else:
            flash("You must complete the modules in order!")
            return redirect(url_for("index"))

@app.route("/trials", methods=["GET", "POST"])
@login_required
def trials():
    form = TrialForm()
    num_completed_trials = current_user.trials.count()
    num_completed_demos=current_user.demos.count()
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
        if num_completed_trials == NUM_TRIALS:
            flash("You have completed all the trials!")
            return redirect(url_for("index"))
        else:
            if current_user.consent and num_completed_demos == NUM_DEMOS and current_user.training:
                return redirect(url_for("trials"))
            else:
                flash("You must complete the modules in order!")
                return redirect(url_for("index"))
    if num_completed_trials == NUM_TRIALS:
        flash("You have completed all the trials!")
        return redirect(url_for("index"))
    else:
        if current_user.consent and num_completed_demos == NUM_DEMOS and current_user.training:
            return render_template("trials.html",
                               title="Trials",
                               form=form,
                               num_bins=NUM_BINS,
                               card=cur_card,
                               num_completed_trials=num_completed_trials,
                               num_trials=NUM_TRIALS,
                               feedback=feedback)
        else:
            flash("You must complete the modules in order!")
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
        if num_completed_demos == NUM_DEMOS:
            flash("You have seen all the demonstrations!")
            return redirect(url_for("index"))
        else:
            if current_user.consent and current_user.training:
                return redirect(url_for("demos"))
            else:
                flash("You must complete the modules in order!")
                return redirect(url_for("index"))
    if num_completed_demos == NUM_DEMOS:
        flash("You have seen all the demonstrations!")
        return redirect(url_for("index"))
    else:
        if current_user.consent and current_user.training:
            return render_template("demos.html",
                            title="Demonstrations",
                            form=form,
                            num_bins=NUM_BINS,
                            card=cur_card,
                            correct_bin=correct_bin,
                            num_completed_demos=num_completed_demos + 1,
                            num_demos=NUM_DEMOS)
        else:
            flash("You must complete the modules in order!")
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