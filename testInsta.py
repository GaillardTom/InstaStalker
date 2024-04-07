import requests
import time
import database
import csv
import json
from bson import ObjectId
proxies = {
    'http': 'http://127.0.0.1:8080',
            'https': 'http://127.0.0.1:8080',
}
# request = requests.request()
# victim username
# Get the user id with the inputed username
burp0_cookies = {"ig_nrcb": "1", "datr": "WLn8ZBm86Ka8e5nrn9GXVRRA", "fbm_124024574287414": "base_domain=.instagram.com", "ig_did": "B5932375-531C-4AA5-B533-70C4EF9DC931", "mid": "ZP6WIAALAAFH5myY8ePsssbQ-UMm", "ps_n": "0", "ps_l": "0", "csrftoken": "FjErNlkKlYcWW9cgoHLLO1b3NqsT7EWD", "ds_user_id": "3609105746", "shbid": "\"8559\\0543609105746\\0541743209213:01f71dd551208034480d829e88b532abaad24d13abdf8b82b2130d7e0f45c530a4711061\"", "shbts": "\"1711673213\\0543609105746\\0541743209213:01f76a4bca1092dafe175b84222eae1fdd6110b5bd50c6540dc22cbdae9c40e26cc2774f\"", "sessionid": "3609105746%3AzdyHKf5nf7A5P2%3A10%3AAYeiv6dkTUG6xH8ECwn3uOu6NXUYyM-gWtj1uUpbAQ", "fbsr_124024574287414": "HAfrr1-zmg5tSKLl3E0wEBknOLNrExUBOgz-A3a4LX4.eyJ1c2VyX2lkIjoiMTAwMDA2ODc0NDUxODU0IiwiY29kZSI6IkFRQmFRTllWeEFBNklmLXRlN3BOaVNfaVQ1VE5TOHlSWUVtTDlMV0p6QmlXR2ZzdzdleWd1d0tPRUVsSmtEU20zN1Z4elB0LWNnOWRJQkRENm44YVhoVEp5endvTEpSeXFpbHdaSmVoLTBQOGo4Q0dibGY5bjBjMUhjWmg3dTEzQ2ZTV28zaFFNeFFNQThTRk5xcjlOVFFDZWEwODdLVW1mbjNSRXJudzdRMWIwanRxQWU0amR1SXhCb0R6VDBIOVRKNDJtaEdVYU9jVEZ2YnIzY1d6NUs0aFM4OW96cFNaUTUwYXZobkFNZm15T0VtQnFXaVZ3ckprMmdhTzF4S3pqM281OUM1c281WnUzWkJOTTRfNlZrcEFNVVotSDBuX3FwaHpoOGtXSDlMeTg4NURLN09oTUVrQTQ2eXhheVJnODY0MmxNeUt3bmlfNUcxeVIxQ2JoMy1HIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCTzZXNXJZQXoyY2txZXNQVEdTWGdRRnhHUGh5VTRCUFh1S0pnaFMwWE1zUGxySWhnRlpDclFWNnlKSVFvc0ZPcE1razJqUWMwS1J4YXd6TzZBUmYxcjh4eHY1aXJqUFNMc0NrVXpsdENGOVpDWkJSVExROFlNRlhldm4wWTNiZ3ZCbkgzd3VCM0EzSG5lMnZISVBBaHdaQXUzc0RHUThSWkFub3lHWkNjSlNtaHpVVktLOWcwSWE2M3daRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzExODIzMzcwfQ", "fbsr_124024574287414": "HAfrr1-zmg5tSKLl3E0wEBknOLNrExUBOgz-A3a4LX4.eyJ1c2VyX2lkIjoiMTAwMDA2ODc0NDUxODU0IiwiY29kZSI6IkFRQmFRTllWeEFBNklmLXRlN3BOaVNfaVQ1VE5TOHlSWUVtTDlMV0p6QmlXR2ZzdzdleWd1d0tPRUVsSmtEU20zN1Z4elB0LWNnOWRJQkRENm44YVhoVEp5endvTEpSeXFpbHdaSmVoLTBQOGo4Q0dibGY5bjBjMUhjWmg3dTEzQ2ZTV28zaFFNeFFNQThTRk5xcjlOVFFDZWEwODdLVW1mbjNSRXJudzdRMWIwanRxQWU0amR1SXhCb0R6VDBIOVRKNDJtaEdVYU9jVEZ2YnIzY1d6NUs0aFM4OW96cFNaUTUwYXZobkFNZm15T0VtQnFXaVZ3ckprMmdhTzF4S3pqM281OUM1c281WnUzWkJOTTRfNlZrcEFNVVotSDBuX3FwaHpoOGtXSDlMeTg4NURLN09oTUVrQTQ2eXhheVJnODY0MmxNeUt3bmlfNUcxeVIxQ2JoMy1HIiwib2F1dGhfdG9rZW4iOiJFQUFCd3pMaXhuallCTzZXNXJZQXoyY2txZXNQVEdTWGdRRnhHUGh5VTRCUFh1S0pnaFMwWE1zUGxySWhnRlpDclFWNnlKSVFvc0ZPcE1razJqUWMwS1J4YXd6TzZBUmYxcjh4eHY1aXJqUFNMc0NrVXpsdENGOVpDWkJSVExROFlNRlhldm4wWTNiZ3ZCbkgzd3VCM0EzSG5lMnZISVBBaHdaQXUzc0RHUThSWkFub3lHWkNjSlNtaHpVVktLOWcwSWE2M3daRCIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNzExODIzMzcwfQ", "rur": "\"NCG\\0543609105746\\0541743359588:01f715430a693ed1104a7a1f1d9d47d8dab66c251da5b071e1b5d72ac254fb6ee98810da\""}
burp0_headers = {"Sec-Ch-Ua": "\"Not A(Brand\";v=\"99\", \"Opera\";v=\"107\", \"Chromium\";v=\"121\"", "X-Ig-Www-Claim": "hmac.AR3pZeONZ4nl1NcNUm8StrWuQipRnWCr0Jf2u-ogNsEZGI5x", "Sec-Ch-Ua-Platform-Version": "\"10.0.0\"", "X-Requested-With": "XMLHttpRequest", "Dpr": "1", "Sec-Ch-Ua-Full-Version-List": "\"Not A(Brand\";v=\"99.0.0.0\", \"Opera\";v=\"107.0.5045.36\", \"Chromium\";v=\"121.0.6167.186\"", "Sec-Ch-Prefers-Color-Scheme": "dark", "X-Csrftoken": "FjErNlkKlYcWW9cgoHLLO1b3NqsT7EWD", "Sec-Ch-Ua-Platform": "\"Windows\"", "X-Ig-App-Id": "936619743392459", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0", "Viewport-Width": "1918", "Accept": "*/*", "X-Asbd-Id": "129477", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.instagram.com/rose.dunnigan/following/", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9", "Dnt": "1", "Sec-Gpc": "1"}


def loginUser():
    burp0_url = "https://www.instagram.com:443/api/v1/web/accounts/login/ajax/"

    burp0_data = {"enc_password": "#PWD_INSTAGRAM_BROWSER:10:1694402217:AVNQAKPngNCN0T45KHkLtItoUNh1x2AhvQexOqeGSC97N20+Ms+zcsbHLXSGRKFYMmiIOOqE/90PvgteUYM3MpSaaLmhWb5LOr0TFuUB7+3JR4Dl42Ae2YdH1/d6CvOyFLXf+yueY9BczLaRYMTkEQ==",
                  "optIntoOneTap": "false", "queryParams": "{}", "trustedDeviceRecords": "{}", "username": "tom.gaming700@gmail.com"}
    requests.post(burp0_url, headers=burp0_headers,
                  cookies=burp0_cookies, data=burp0_data)


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


# Print all of the info
PrintingInfo(findings)
