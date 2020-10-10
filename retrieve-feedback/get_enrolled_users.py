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


def get_enrolled_users(courses):
    global moodle_token
    global userid

    for course in courses:
        payload = {
                "wstoken":moodle_token,
                "moodlewsrestformat":"json",
                "wsfunction":"core_enrol_get_enrolled_users",
                "courseid":int(course['id'])
                }
        r = requests.post(rest_url, params=payload)
        res_json = r.json()
        with open(course['shortname'].replace("/","|")+"_users.json", 'w') as outfile:
            json.dump(res_json, outfile)


def main():
    parse_config(CONFIG_FILE)
    get_auth_token()
    get_userid()
    get_enrolled_users(get_courses())


if __name__ == "__main__":
    sys.exit(main())
