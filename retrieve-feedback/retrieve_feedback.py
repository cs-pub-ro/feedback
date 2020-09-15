#!/usr/bin/env python3
# (c) Mihai Chiroiu 18 May 2020
# sudo pip3 install requests
# https://docs.moodle.org/dev/Web_service_API_functions

import json
import requests
import sys
import configparser


CONFIG_FILE = "feedback.conf"

username = ""
base_url = ""
rest_url = ""
moodle_token = ""
userid = ""


def parse_config(config_file):
    global username
    global password
    global base_url
    global rest_url

    config = configparser.ConfigParser()
    config.read(config_file)

    base_url = config['connect']['url']
    rest_url = base_url + "/webservice/rest/server.php"
    username = config['connect']['username']
    password = config['connect']['password']


def get_auth_token():
    global moodle_token

    token_url = base_url + "/login/token.php"
    payload = {
            "username":username,
            "password":password,
            "moodlewsrestformat":"json",
            "service":"moodle_mobile_app"
            }

    r = requests.post(token_url, params=payload)
    res_json = r.json()
    moodle_token = res_json['token']


def get_userid():
    global moodle_token
    global userid

    payload = {
            "wstoken":moodle_token,
            "moodlewsrestformat":"json",
            "wsfunction":"core_webservice_get_site_info"
            }
    r = requests.post(rest_url, params=payload)
    res_json = r.json()
    userid = res_json['userid']


def get_user_courses():
    global moodle_token
    global userid

    payload = {
            "wstoken":moodle_token,
            "moodlewsrestformat":"json",
            "wsfunction":"core_enrol_get_users_courses",
            "userid":userid
            }
    r = requests.post(rest_url, params=payload)
    return r.json()


def get_courses():
    global moodle_token
    global userid

    payload = {
            "wstoken":moodle_token,
            "moodlewsrestformat":"json",
            "wsfunction":"core_course_get_courses"
            }
    r = requests.post(rest_url, params=payload)
    return r.json()


def get_user_courses_ids():
    course_ids = {}

    for course in get_user_courses():
        course_ids[course['id']] = course['shortname']
    return course_ids


def get_courses_ids():
    course_ids = {}

    for course in get_courses():
        course_ids[course['id']] = course['shortname']
    return course_ids


def get_user_feedback_ids():
    global moodle_token
    global userid

    course_ids = get_courses_ids()

    payload = {
            "wstoken":moodle_token,
            "moodlewsrestformat":"json",
            "wsfunction":"mod_feedback_get_feedbacks_by_courses"
            }
    # Create a JSON of all courses id for the user.
    i = 0
    NUM_COURSES_PER_QUERY = 50
    feedback_ids = {}
    for course_id in course_ids:
        course_id_json = {"courseids["+str(i)+"]":course_id}
        i+=1
        payload.update(course_id_json)

        if i == NUM_COURSES_PER_QUERY:
            r = requests.post(rest_url, params=payload)
            res_json = r.json()
            # Create the list of feedback IDs for courses.
            for feedback in res_json['feedbacks']:
                # Ignore additional feedbacks for a course.
                if course_ids[feedback['course']] in feedback_ids.values():
                    print("Already exists feedback for course {} ({})".format(feedback['course'], course_ids[feedback['course']]))
                    continue
                feedback_ids[feedback['id']] = course_ids[feedback['course']]
            # Reset counter.
            i = 0
    return feedback_ids


def get_user_feedback():
    global moodle_token
    global userid

    feedback_ids = get_user_feedback_ids()

    payload = {
            "wstoken":moodle_token,
            "moodlewsrestformat":"json",
            "wsfunction":"mod_feedback_get_responses_analysis"
            }

    for feedback_id in feedback_ids:
        course_id_json = {"feedbackid":feedback_id}
        payload.update(course_id_json)

        r = requests.post(rest_url, params=payload)
        res_json = r.json()
        with open(feedback_ids[feedback_id].replace("/","|")+".json", 'w') as outfile:
            json.dump(res_json, outfile)


def main():
    parse_config(CONFIG_FILE)
    get_auth_token()
    get_userid()
    get_user_feedback()


if __name__ == "__main__":
    sys.exit(main())
