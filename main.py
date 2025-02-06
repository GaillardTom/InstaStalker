import requests
import time
import database
import csv
import json
from bson import ObjectId
from flask import Flask, redirect, send_from_directory, url_for, request, render_template
from flask_cors import CORS
import os
from dotenv import load_dotenv
app = Flask(__name__, static_folder='static', template_folder='templates')
#Initalizing the CORS module
CORS(app)
#Load the environment variables from the .env file
load_dotenv()
#for the images static folder
IMG_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] =  IMG_FOLDER
proxies = {
    'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080',
}
# request = requests.request()
# victim username
# Get the user id with the inputed username
#TODO PUT THE COOKIES AND HEADERS AND DATA IN THE ENV FILE
burp0_cookies = json.loads(os.environ.get('burp0_cookies'))    
burp0_headers = json.loads(os.environ.get('burp0_headers'))    

# print(f"cookies: {burp0_cookies}")
# print(f"headers: {burp0_headers}")

def loginUser():
    burp0_url = "https://www.instagram.com:443/api/v1/web/accounts/login/ajax/"
    # print(f"cookies: {burp0_cookies}")
    # print(f"headers: {burp0_headers}")
    burp0_data = json.loads(os.environ.get("burp0_data"))   
    print(burp0_data)

    
    requests.post(burp0_url, headers=burp0_headers,
                  cookies=burp0_cookies, data=burp0_data)

def download_image(url, image_path):
    response = requests.get(url, stream=True, headers=burp0_headers, cookies=burp0_cookies)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        file.close()

def convert_object_ids_to_strings(data):
    if isinstance(data, list):
        # If data is a list, iterate through each item in the list
        for i in range(len(data)):
            data[i] = convert_object_ids_to_strings(data[i])
    elif isinstance(data, dict):
        # If data is a dictionary, iterate through key-value pairs
        for key, value in data.items():
            data[key] = convert_object_ids_to_strings(value)
            if isinstance(value, ObjectId):
                # Convert ObjectId to a string
                data[key] = str(value)
    return data


def readTargets():
    file = open('targets.txt', 'r')
    targets = file.readlines()
    return targets


def writeToFile(usersList, file_name: str):
    all_keys = set(key for item in usersList for key in item.keys())

    # print(f"Header Names: {all_keys}")
    with open(file_name, mode="w", newline="", encoding="UTF-8") as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=all_keys)

        writer.writeheader()
        for item in usersList:
            row = {key: json.dumps(item.get(key, ""), ensure_ascii=False)
                   for key in all_keys}
            # print(f"inserting Row: {row}")
            writer.writerow(row)


def getUserID(username: str):
    try:
        burp0_url = f"https://www.instagram.com:443/api/v1/feed/user/{username}/username/?count=6"
        r = requests.get(burp0_url, headers=burp0_headers,
                     cookies=burp0_cookies)
        return r.json().get("user").get("pk_id")
    except Exception as e:
        print(f"Error with user {username}")
        print(e)
        return None

def sec_to_hours(seconds):
    a = str(seconds//3600)
    b = str((seconds % 3600)//60)
    c = str((seconds % 3600) % 60)
    d = ["{}h{}m{}s".format(a, b, c)]
    return d


def PrintingInfo(findings: dict):
    for target in findings.keys():
        print("-------------------------------")
        print(f"For {target}")
        print(f"Time taken: {findings[target]['timeTaken']}")
        if(findings[target]["newUsers"] == "Error"):
            print("There was a problem with this user")
            continue
        if(findings[target]["newUsers"]):
            for newUser in findings[target]["newUsers"]:
                print(f"Found since last Time: {newUser}")
        else:
            print("No new users !")

def GetFollowing():
    findings = {}
    targets = readTargets()
    for target in targets:
        newUsers = []
        target = target.strip()
        print(f"Stalking {target}")
        isFailed = False
        lnum = 0
        retryCount = 0
        try:
            userID = getUserID(target)
            if userID is None:
                print(f"Skipping {target}...")
                isFailed = True
                continue
            startTime = time.time()
            burp0_url = f"https://www.instagram.com:443/api/v1/friendships/{userID}/following/?count=200"

            response = requests.get(
                burp0_url, headers=burp0_headers, cookies=burp0_cookies)

            json_response = response.json()
            users = json_response.get("users")

            no_more_user = False

            while 1:
                if(json_response.get("next_max_id")):
                    next_max_id = json_response.get("next_max_id")

                    burp0_url = f"https://www.instagram.com:443/api/v1/friendships/{userID}/following/?count=200&max_id={next_max_id}"
                    time.sleep(1)
                    response = requests.get(
                        burp0_url, headers=burp0_headers, cookies=burp0_cookies)
                    json_response = response.json()
                    if(json_response.get("users")):
                        users += json_response.get("users")
                    else:
                        print(
                            f"This response was not added {json_response} in loop number {lnum}, \nlogin user and retrying in 2 seconds...")
                        # loginUser()
                        time.sleep(2)
                        while(retryCount <= 3 or retryCount == -1):
                            time.sleep(10)
                            response = requests.get(
                                burp0_url, headers=burp0_headers, cookies=burp0_cookies)
                            print(f"Recalling {burp0_url}")
                            json_response = response.json()
                            print(f"Received: {json_response}")
                            if(json_response.get("next_max_id") and json_response.get("users")):
                                users += json_response.get("users")
                                retryCount = -1
                            retryCount += 1
                    print(f"Loop number: {lnum}")
                    lnum += 1
                else:
                    no_more_user = True
                    break
        except any as e:
            print(
                f"Problem with user {target} at loop #{lnum}  skipping to next user")
            print(e)
            isFailed = True
            continue
        currTime = time.strftime("%Y-%m-%d %H:%M:%S")
        doc, coll = database.fetch(target)
        for user in users:
            # Save to DB if user is not already in
            resp = database.InsertUserIfNotFound(coll, user, currTime)
            if(resp):
                newUsers.append(user['username'])
            # print(f"Is inserted into db: {resp} \n")
            # if(resp == True):
            #     username = user.get("username")
            #     full_name = user.get("full_name")

            #     print(f"username: {username}")
            #     # print(f"full_name: {full_name} \n")

        curr_date = time.strftime("%d_%m_%y")
        # print(f"Current date: {curr_date}")
        file_name = f"./data/{target}_{curr_date}.csv"
        # Iterate through the JSON data and convert ObjectId values to strings
        users = convert_object_ids_to_strings(users)
        # print(f"File outputed: {file_name}")
        writeToFile(users, file_name)
        # print(f"Total following count: {len(users)}")

        endTime = time.time()
        timeTaken = sec_to_hours(round(endTime - startTime))
        # print(f"Time Taken: {sec_to_hours(timeTaken)[0]}")
        # delay between targets
        dataOfTarget = {"timeTaken": timeTaken, "newUsers": newUsers}
        if(isFailed):
            dataOfTarget["newUsers"] = "Error"
        findings[target] = dataOfTarget

        time.sleep(2)
    return findings
def checkExistingUser(username):
    #Check to see if the user actually exists on instagram or not
    #if yes, it will download the profile pic and return true else false
    try:
        userID = getUserID(username)
        if userID is None:
            print(f"Skipping {username}...")
            return False

        #now that we have the userID we will fetch the profile pic
        burp0_url = f"https://www.instagram.com:443/api/v1/users/{userID}/info/"
        response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
        json_response = response.json()
        user = json_response.get("user")
        #download the profile pic
        download_image(user['hd_profile_pic_url_info']['url'], f"static/images/{username}.jpg")
        return True
    except Exception as e:
        print(e)
        return False
def getFollowingForUser(username):
    findings = {}
    newUsers = []
    target = username.strip()
    testDict = {}
    print(f"Stalking {target}")
    isFailed = False
    lnum = 0
    retryCount = 0
    try:
        userID = getUserID(target)
        if userID is None:
            print(f"Skipping {target}...")
            isFailed = True
        # print("Got User ID...")
        startTime = time.time()
        # print("Timer started...")
        burp0_url = f"https://www.instagram.com:443/api/v1/friendships/{userID}/following/?count=200"

        # print(f"cookies: {request.cookies.get_dict()}")
        time.sleep(1)
        response = requests.get(
            burp0_url, headers=burp0_headers, cookies=burp0_cookies)

        json_response = response.json()
        # print(json_response)
        users = json_response.get("users")
        # for user in users:
        no_more_user = False

        while 1:
            if(json_response.get("next_max_id")):
                next_max_id = json_response.get("next_max_id")

                burp0_url = f"https://www.instagram.com:443/api/v1/friendships/{userID}/following/?count=200&max_id={next_max_id}"
                time.sleep(1)
                response = requests.get(
                    burp0_url, headers=burp0_headers, cookies=burp0_cookies)
                json_response = response.json()
                if(json_response.get("users")):
                    users += json_response.get("users")
                    # testDict[user['username']] = [user['full_name'], user['profile_pic_url'], user['is_private'], user['is_verified']]
                else:
                    print(
                        f"This response was not added {json_response} in loop number {lnum}, \nlogin user and retrying in 2 seconds...")
                    # loginUser()
                    time.sleep(2)
                    while(retryCount <= 3 or retryCount == -1):
                        time.sleep(10)
                        response = requests.get(
                            burp0_url, headers=burp0_headers, cookies=burp0_cookies)
                        print(f"Recalling {burp0_url}")
                        json_response = response.json()
                        print(f"Received: {json_response}")
                        if(json_response.get("next_max_id") and json_response.get("users")):
                            users += json_response.get("users")
                            retryCount = -1
                        retryCount += 1
                print(f"Loop number: {lnum}")
                lnum += 1
            else:
                no_more_user = True
                break
    except any as e:
        print(
            f"Problem with user {target} at loop #{lnum}  skipping to next user")
        print(e)
        isFailed = True
        
    currTime = time.strftime("%Y-%m-%d %H:%M:%S")
    doc, coll = database.fetch(target)
    for user in users:
        # Save to DB if user is not already in
        resp = database.InsertUserIfNotFound(coll, user, currTime)
        if(resp):
            newUsers.append(user['username'])
            download_image(user['profile_pic_url'], f"static/images/{user['username']}.jpg")
            testDict[user['username']] = [user['full_name'], f"/images/{user['username']}.jpg", user['is_private'], user['is_verified']]
        # print(f"Is inserted into db: {resp} \n")
        # if(resp == True):
        #     username = user.get("username")
        #     full_name = user.get("full_name")

        #     print(f"username: {username}")
        #     # print(f"full_name: {full_name} \n")
    curr_date = time.strftime("%d_%m_%y")
    # print(f"Current date: {curr_date}")
    file_name = f"./data/{target}_{curr_date}.csv"
    # Iterate through the JSON data and convert ObjectId values to strings
    users = convert_object_ids_to_strings(users)
    # print(f"File outputed: {file_name}")
    writeToFile(users, file_name)
    # print(f"Total following count: {len(users)}")

    endTime = time.time()
    timeTaken = sec_to_hours(round(endTime - startTime))
    # print(f"Time Taken: {sec_to_hours(timeTaken)[0]}")
    # delay between targets
    dataOfTarget = {"timeTaken": timeTaken, "newUsers": newUsers}
    # testDict["timeTaken"] = timeTaken
    if(isFailed):
        dataOfTarget["newUsers"] = "Error"
    findings[target] = testDict
    return findings


@app.route("/")
def home(): 
    return render_template("index.html", targets=readTargets())
@app.route("/deleteTarget/<target>", methods=["POST"])
def deleteTarget(target):
    print(f'Deleting {target}')
    with open("targets.txt", "r") as file:
        lines = file.readlines()
    with open("targets.txt", "w") as file:
        for line in lines:
            print(f"Line: {line}")
            if line.strip("\n") != target.strip():
                file.write(line)
            else:
                print(f"Deleted {line}")
    return redirect(url_for("home"))
@app.route("/hunt/<target>", methods=["GET", "POST"])
def huntSingleTarget(target): 
    if request.method == "POST":
        try:
            following = getFollowingForUser(target)
        
            for item in following.keys():
                print(f"Item: {item}")
                print(f"Following: {following[item]}") 
            return render_template("hunt.html", following=following, target=target)
        except Exception as e:
            print(e)
            return redirect(url_for("home"))
   
@app.route("/hunt")
def startHunt(): 
    # GetFollowing()
    return render_template("hunt.html")
@app.route("/hunt/all")
def huntAll():
    all_following = GetFollowing()  # This function should return a dictionary
    return render_template("hunt_all.html", all_following=all_following)
@app.route("/addTarget", methods=["POST"])
def addTarget():
    target = request.form["target"].strip()
    check = checkExistingUser(target)
    if check == False:
        print("User does not exist")
        return redirect(url_for("home"))
    with open("targets.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.strip("\n") == target.strip():
                print("Target already exists")
                return redirect(url_for("home"))
    with open("targets.txt", "a") as file:
        file.write(target + "\n")
    return redirect(url_for("home"))
@app.route('/static/<path:filename>')
def staticfiles(filename):
    return send_from_directory(app.static_folder, filename)
if __name__ == "__main__":
    app.run(debug=True)