import pandas
import matplotlib.pyplot as plt
import csv
import time
import os
from utils import *
import pandas as pd
import pingouin as pg
import seaborn as sns
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from bioinfokit.analys import stat
from numpy.polynomial.polynomial import polyfit


sns.set_theme(style="whitegrid")

if __name__ == '__main__':
    column_names = ['id', 'condition', 'username', 'robot_teaching', 'user_learning', 'age', 'gender', 'ethnicity', 'education', 'robot']
    robot_teaching = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
    user_learning = ["Strongly Disagree","Disagree","Neutral","Agree","Strongly Agree"]
    age = ["18-24","25-34","35-44","45-54","55-64", "65-74","75-84","85 or older"]
    gender =  ["Male","Female","Other"]
    education = ["Less than high school degree","High school graduate (high school diploma or equivalent including GED)","Some college but no degree","Associate degree in college (2-year)","Bachelor’s degree in college (4-year)","Master’s degree","Doctoral degree","Professional degree (JD, MD)"]
    ethnicity = ["White","Black or African American","American Indian or Alaska Native","Asian","Native Hawaiian or Pacific Islander","Other"]
    robot = ["Not at all","Slightly","Moderately","Very","Extremely"]
    
    df_user = pandas.read_csv('result/user_updated.csv')
    df_trial = pandas.read_csv('result/trial_updated.csv')
    df_demo = pandas.read_csv('result/demo_updated.csv')

    ids = list(df_user.id)[1:]
    df_user = df_user[df_user.id != 1]
    df_trial = df_trial[df_trial.user_id != 1]
    df_demo = df_demo[df_demo.user_id != 1]

    trials = list(range(1,11))

    trials_dict = {}
    
    for i,c in zip(list(df_trial.trial_num),list(df_trial.text_feedback)):
        if str(i) not in trials_dict:
            trials_dict[str(i)] = 0
        # print(c)
        if c == 'Correct!':
            trials_dict[str(i)] += 1/19

    trials_none = {}
    
    for i,c,f in zip(list(df_trial.trial_num),list(df_trial.text_feedback), list(df_trial.feedback_type)):
        if str(i) not in trials_none:
            trials_none[str(i)] = 0
        # print(c)
        if c == 'Correct!' and f == 'none':
            trials_none[str(i)] += 1/5
    
    trials_both = {}
    
    for i,c,f in zip(list(df_trial.trial_num),list(df_trial.text_feedback), list(df_trial.feedback_type)):
        if str(i) not in trials_both:
            trials_both[str(i)] = 0
        # print(c)
        if c == 'Correct!' and f == 'both':
            trials_both[str(i)] += 1/5

    trials_text = {}
    
    for i,c,f in zip(list(df_trial.trial_num),list(df_trial.text_feedback), list(df_trial.feedback_type)):
        if str(i) not in trials_text:
            trials_text[str(i)] = 0
        # print(c)
        if c == 'Correct!' and f == 'text':
            trials_text[str(i)] += 1/5

    trials_nonverbal = {}
    
    for i,c,f in zip(list(df_trial.trial_num),list(df_trial.text_feedback), list(df_trial.feedback_type)):
        if str(i) not in trials_nonverbal:
            trials_nonverbal[str(i)] = 0
        # print(c)
        if c == 'Correct!' and f == 'nonverbal':
            trials_nonverbal[str(i)] += 1/4

    # fig,ax = plt.subplots(figsize=(15,5))
    # X = np.arange(1,11)
    # ax.set_xlabel('Trial number', fontsize=15)
    # ax.set_ylabel('correctness %', fontsize=15)
    # ax.set_xticks(X)
    # ax.plot(X, list(trials_none.values()),'v-', color = 'b',  label='none', linewidth=2)
    # ax.plot(X, list(trials_text.values()), '8-',color = 'g', label='text', linewidth=2)
    # ax.plot(X, list(trials_nonverbal.values()), 's-',color = 'r', label='nonverbal', linewidth=2)
    # ax.plot(X, list(trials_both.values()), '*-',color = 'c', label='both', linewidth=2)
    # ax.plot(X,list(trials_dict.values()), 'o-', color='black', label='combined', linewidth=2)

    # ax.legend(fontsize=13)
    # plt.savefig('correctness_byfeedback.png')
    # plt.show()


    data_trials = pandas.DataFrame({'none': list(trials_none.values()),
                                    'text': list(trials_text.values()), 
                                    'nonverbal': list(trials_nonverbal.values()), 
                                    'both': list(trials_both.values())})
    df_melt = pandas.melt(data_trials.reset_index(), id_vars=['index'], value_vars=['none', 'text', 'nonverbal', 'both'])
    df_melt.columns = ['index', 'feedback_type', 'correctness']
    model = ols('correctness ~ C(feedback_type)', data=df_melt).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    res = stat()
    res.tukey_hsd(df=df_melt, res_var='correctness', xfac_var='feedback_type', anova_model='correctness ~ C(feedback_type)')
    # print(res.tukey_summary)

    none_id = [5,14, 15, 17, 19]
    text_id = [2, 4, 6, 8, 11]
    nonverbal_id = [7, 10,12,16]
    both_id = [20,18,13,9,3]
    
    ul_none = [] # user learning score in likert scale
    rt_none = [] # robot teaching score in likert scale
    correct_none = []
    age_range = []
    gender_user = []
    ethnicity_user = []
    robot_user = []
    for i in none_id:
        ul_none += list(df_user[df_user.id==i].user_learning)
        rt_none += list(df_user[df_user.id==i].robot_teaching)
        correct_none += [list(df_trial[df_trial.user_id==i].text_feedback)]
        age_range += list(df_user[df_user.id==i].age)
        gender_user += list(df_user[df_user.id==i].gender)
        ethnicity_user += list(df_user[df_user.id==i].ethnicity)
        robot_user += list(df_user[df_user.id==i].robot)

    
    ul_text = []
    rt_text = []
    correct_text = []
    for i in text_id:
        ul_text += list(df_user[df_user.id==i].user_learning)
        rt_text += list(df_user[df_user.id==i].robot_teaching)
        correct_text += [list(df_trial[df_trial.user_id==i].text_feedback)]
        age_range += list(df_user[df_user.id==i].age)
        gender_user += list(df_user[df_user.id==i].gender)
        ethnicity_user += list(df_user[df_user.id==i].ethnicity)
        robot_user += list(df_user[df_user.id==i].robot)


    ul_nonverbal = []
    rt_nonverbal = []
    correct_nonverbal = []
    for i in nonverbal_id:
        ul_nonverbal += list(df_user[df_user.id==i].user_learning)
        rt_nonverbal += list(df_user[df_user.id==i].robot_teaching)
        correct_nonverbal += [list(df_trial[df_trial.user_id==i].text_feedback)]
        age_range += list(df_user[df_user.id==i].age)
        gender_user += list(df_user[df_user.id==i].gender)
        ethnicity_user += list(df_user[df_user.id==i].ethnicity)
        robot_user += list(df_user[df_user.id==i].robot)


    ul_both = []
    rt_both = []
    correct_both = []
    for i in both_id:
        ul_both += list(df_user[df_user.id==i].user_learning)
        rt_both += list(df_user[df_user.id==i].robot_teaching)
        correct_both += [list(df_trial[df_trial.user_id==i].text_feedback)]
        age_range += list(df_user[df_user.id==i].age)
        gender_user += list(df_user[df_user.id==i].gender)
        ethnicity_user += list(df_user[df_user.id==i].ethnicity)
        robot_user += list(df_user[df_user.id==i].robot)

    
    correct_none = [np.mean([1 if c == 'Correct!' else 0 for c in l]) for l in correct_none]
    correct_text = [np.mean([1 if c == 'Correct!' else 0 for c in l]) for l in correct_text]
    correct_nonverbal = [np.mean([1 if c == 'Correct!' else 0 for c in l]) for l in correct_nonverbal]
    correct_both = [np.mean([1 if c == 'Correct!' else 0 for c in l]) for l in correct_both]

    age_dic = {}
    for a in age_range:
        if age[int(a)] not in age_dic:
            age_dic[age[int(a)]] = 0
        age_dic[age[int(a)]] += 1

    gender_dic = {}
    for a in gender_user:
        if gender[int(a)] not in gender_dic:
            gender_dic[gender[int(a)]] = 0
        gender_dic[gender[int(a)]] += 1

    ethnicity_dic = {}
    for a in ethnicity_user:
        if ethnicity[int(a)] not in ethnicity_dic:
            ethnicity_dic[ethnicity[int(a)]] = 0
        ethnicity_dic[ethnicity[int(a)]] += 1

    robot_dic = {}
    for a in robot_user:
        if robot[int(a)] not in robot_dic:
            robot_dic[robot[int(a)]] = 0
        robot_dic[robot[int(a)]] += 1

    data_ul = pandas.DataFrame({'none': ul_none,
                                    'text': ul_text, 
                                    'nonverbal': ul_nonverbal+[None], 
                                    'both': ul_both})
    df_melt = pandas.melt(data_ul.reset_index(), id_vars=['index'], value_vars=['none', 'text', 'nonverbal', 'both'])
    df_melt.columns = ['index', 'feedback_type', 'likert_score']
    model = ols('likert_score ~ C(feedback_type)', data=df_melt).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    res = stat()
    res.tukey_hsd(df=df_melt, res_var='likert_score', xfac_var='feedback_type', anova_model='likert_score ~ C(feedback_type)')

    # print(res.tukey_summary)
    # fig, axs = plt.subplots(2, 2)

    # axs[0, 0].plot(ul_none, list(trials_none.values()))
    # axs[0, 0].set_title('No Feedback')
    # axs[0, 1].plot(ul_text, list(trials_text.values()), 'tab:orange')
    # axs[0, 1].set_title('Text Feedback')
    # axs[1, 0].plot(ul_nonverbal, list(trials_nonverbal.values()), 'tab:green')
    # axs[1, 0].set_title('Nonverbal Feedback')
    # axs[1, 1].plot(ul_both, list(trials_both.values()), 'tab:red')
    # axs[1, 1].set_title('Both Feedbacks')

    # plt.show()

    ### Histogram of accuracy distriburion for all feedbacks

    # fig, axs = plt.subplots(2,2)
    # fig.tight_layout(pad=2.0)
    # X = np.arange(0,6)*0.2
    # axs[0, 0].hist(list(data_trials.none), color='b', width=0.15, label='none')
    # axs[0, 0].set_title('No feedback')
    # axs[0, 0].set_xticks(X)
    # axs[0, 0].set_xlabel('# of occurances', fontsize=9)
    # axs[0, 0].set_ylabel('correctness %', fontsize=9)
    # axs[0, 1].hist(list(data_trials.text), color='g', width=0.15, label='text')
    # axs[0, 1].set_title('Text feedback')
    # axs[0, 1].set_xticks(X)
    # axs[0, 1].set_xlabel('# of occurances', fontsize=9)
    # axs[0, 1].set_ylabel('correctness %', fontsize=9)
    # axs[1, 0].hist(list(data_trials.nonverbal), color='r', width=0.15, label='nonverbal')
    # axs[1, 0].set_title('Nonverbal feedback')
    # axs[1, 0].set_xticks(X)
    # axs[1, 0].set_xlabel('# of occurances', fontsize=9)
    # axs[1, 0].set_ylabel('correctness %', fontsize=9)
    # axs[1, 1].hist(list(data_trials.both), color='c', width=0.15, label='both')
    # axs[1, 1].set_title('Both feedbacks')
    # axs[1, 1].set_xticks(X)
    # axs[1, 1].set_xlabel('# of occurances', fontsize=9)
    # axs[1, 1].set_ylabel('correctness %', fontsize=9)

    # plt.savefig('distribution_histogram.png')
    # plt.show()

    ## Boxplot for trial data distribution comparison

    # fig, ax = plt.subplots()
    # data_trials.boxplot(['none', 'text', 'nonverbal', 'both'], ax=ax)
    # ax.set_ylabel('correctness %',fontsize=14)
    # ax.set_xlabel('feedback type', fontsize=14)
    # plt.savefig('boxplot.png')
    # plt.show()

    ## Boxplot for user learning score distribution comparison

    # fig, ax = plt.subplots()
    # user_learning = pandas.DataFrame({'none': ul_none,'text': ul_text, 'nonverbal': ul_nonverbal+[None], 'both': ul_both})
    # user_learning.boxplot(['none', 'text', 'nonverbal', 'both'], ax=ax)

    # ax.set_ylabel('likert score',fontsize=14)
    # ax.set_xlabel('feedback type', fontsize=14)
    # plt.savefig('boxplot_ul.png')
    # plt.show()

    ## Boxplot for user learning score distribution comparison

    # fig, ax = plt.subplots()
    # user_learning = pandas.DataFrame({'none': rt_none,'text': rt_text, 'nonverbal': rt_nonverbal+[None], 'both': rt_both})
    # user_learning.boxplot(['none', 'text', 'nonverbal', 'both'], ax=ax)

    # ax.set_ylabel('likert score',fontsize=14)
    # ax.set_xlabel('feedback type', fontsize=14)
    # plt.savefig('boxplot_rt.png')
    # plt.show()

    ## correlation between subjective and objective performance

    fig, ax = plt.subplots(2,2)
    fig.tight_layout(pad=3.0)
    ax[0,0].scatter(ul_none, correct_none, label='none', color='b')
    # b, m = polyfit(ul_none, correct_none, 1)
    # ax[0,0].plot(ul_none, b + np.multiply(ul_none,m), '-', color='b')
    ax[0,1].scatter(ul_text, correct_text, label='text', color='g')
    # b, m = polyfit(ul_text, correct_text, 1)
    # ax[0,1].plot(ul_text, b + np.multiply(ul_text,m), '-', color='g')
    ax[1,0].scatter(ul_nonverbal, correct_nonverbal, label='nonverbal', color='r')
    # b, m = polyfit(ul_nonverbal, correct_nonverbal, 1)
    # ax[1,0].plot(ul_nonverbal, b + np.multiply(ul_nonverbal,m), '-', color='r')
    ax[1,1].scatter(ul_both,correct_both, label='both', color='c')
    # b, m = polyfit(ul_both, correct_both, 1)
    # ax[1,1].plot(ul_both, b + np.multiply(ul_both, m), '-', color='c')
    names = [['No feedback', 'Text'],['Nonverbal', 'Both']]
    for i in range(2):
        for j in range(2):
            ax[i,j].set_ylabel('correctness %', fontsize=10)
            ax[i,j].set_xlabel('user learning likert score', fontsize=10)
            ax[i,j].set_yticks([0,0.25,0.5,0.75,1.0])
            ax[i,j].set_xticks([0,1,2,3,4])
            ax[i,j].set_title(names[i][j])
    plt.savefig('correlation.png')
    plt.show()

    x = pd.Series(correct_none)
    y = pd.Series(ul_none)
    print(x.corr(y))
    x = pd.Series(correct_text)
    y = pd.Series(ul_text)
    print(x.corr(y))
    x = pd.Series(correct_nonverbal)
    y = pd.Series(ul_nonverbal)
    print(x.corr(y))
    x = pd.Series(correct_both)
    y = pd.Series(ul_both)
    print(x.corr(y))