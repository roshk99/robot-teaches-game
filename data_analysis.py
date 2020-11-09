import numpy as np
import csv
import time
import os
from app.utils import *

class User():
    def __init__(self, row, time):
        self.id = int(row['id'])
        self.time = time
        self.username = row['username']
        self.consent = int(row['consent'])
        self.training = int(row['training'])
        self.robot_teaching = int(row['robot_teaching'])
        self.user_learning = int(row['user_learning'])
        self.age = int(row['age'])
        self.gender = int(row['gender'])
        self.ethnicity = int(row['ethnicity'])
        self.education = int(row['education'])
        self.robot = int(row['robot'])
        self.demos = {}
        self.trials = {}

    def add_demo(self, row):
        self.demos[row['demo_num']] = {
            'card_num': row['card_num'],
            'correct_bin': row['correct_bin'],
            'rule_set': str_to_rules(row['rule_set'])
        }
    
    def add_trial(self, row):
        self.trials[row['trial_num']] = {
            'card_num': row['card_num'],
            'correct_bin': row['correct_bin'],
            'chosen_bin': row['chosen_bin'],
            'feedback_given': row['feedback_given'],
            'feedback_type': row['feedback_type'],
            'rule_set': str_to_rules(row['rule_set'])
        }



def create_users():
    user_arr = {}
    with open('result/user.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        created_time = time.gmtime(os.path.getctime('result/user.csv'))

        for row in reader:
            cur_user = User(row, created_time)
            user_arr[get_user_index(cur_user.id, cur_user.time)] = cur_user
    return user_arr

def add_demos(user_arr):
    with open('result/demo.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        created_time = time.gmtime(os.path.getctime('result/demo.csv'))

        for row in reader:
            user_arr[get_user_index(row['user_id'], created_time)].add_demo(row)
    return(user_arr)

def add_trials(user_arr):
    with open('result/trial.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        created_time = time.gmtime(os.path.getctime('result/trial.csv'))

        for row in reader:
            user_arr[get_user_index(row['user_id'], created_time)].add_trial(row)

    return(user_arr)

user_arr = create_users()
user_arr = add_demos(user_arr)
user_arr = add_trials(user_arr)