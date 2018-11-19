# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

def time_to_normalize(time):
    if (len(time.split("a")) == 1):
        time = time.split("p")[0]
        time_two = int(time) + 12

    else:
        time = time.split("a")[0]
        time = int(time)

        if time == 12:
            time = 0
        else:
            pass


# checks if work time-end is will be finished in the sameday#
def parseTimeSet(time):
    timeSet = time.split("-")

    timeTable = []

    index = 0

    for time in timeSet:
        t = time
        if (t.endswith("am")):
            if index == 0:
                timeTable.append({
                    "type": "start",
                    "start_str": t.split("am")[0],
                    "start": int(t.split("am")[0]),
                    "english": "Morning"
                })
            else:
                timeTable.append({
                    "type": "end",
                    "start_str": t.split("am")[0],
                    "start": int(t.split("am")[0]),
                    "english": "Morning"
                })
            index += 1

        else:

            if index == 0:
                starti = int(t.split("pm")[0])

                timeTable.append({
                    "type": "start",
                    "start_str": t.split("pm")[0],
                    "start": int(t.split("pm")[0]),
                    "english": "Evening",
                    "hour": starti + 12
                })
            else:
                timeTable.append({
                    "type": "end",
                    "start_str": t.split("pm")[0],
                    "start": int(t.split("pm")[0]),
                    "english": "Evening",
                    "hour": int(t.split("pm")[0]) + 12
                })
            index += 1

    return (timeTable)


def isTimeSetSame(start, end):
    timetable = parseTimeSet(start + "-" + end)
    prev = timetable[0]["english"]
    now = timetable[1]["english"]

    if (prev == now):
        return True
    else:
        return False


# takes in to account if its an evening start or a morning start#
# if its a evening start +12 is added
def dumb_to_smart(timetable):
    start_smart = 0
    end_smart = 0

    if timetable[0]["english"] == "Morning":
        start_smart = timetable[0]["start"]
    else:
        start_smart = timetable[0]["start"] + 12
        start_smart + 12

    if timetable[1]["english"] == "Evening":
        end_smart = timetable[1]["start"] + 12
    else:
        end_smart = timetable[1]["start"]

    return {
        "start_smart": start_smart,
        "end_smart": end_smart
    };


def hoursWorking(start, end):
    timetable = parseTimeSet(start + "-" + end)
    start_end_arr = dumb_to_smart(timetable)

    start_smart = int(start_end_arr["start_smart"])
    start_end = int(start_end_arr["end_smart"])

    clock_up = 12
    ##minus event from this

    if (start_smart >= start_end):

        dumb_smart = int(start_smart) - 12

        hours_working = 12 - dumb_smart + int(start_end)

        return {
            "hours_worked": hours_working,
            "hours_free_today": 24 - hours_working
        }



    else:
        dumb_smart = 12 - int(start_smart)

        dumb_end = start_end - 12

        ab = dumb_end + dumb_smart

        hours_left = dumb_smart + start_end

        print("most likely the work will finish the same day")

        tf = dumb_end + dumb_smart
        return {
            "hours_worked": tf,
            "hours_free_today": 24 - tf
        }


def ww(start, end):
    return hoursWorking(start, end)



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'
    
@app.route("/work/<start>/<end>")
def hello(start,end):
    return jsonify(ww(start,end))

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
