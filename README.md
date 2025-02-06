# Instagram Stalker

## What is this ? 

> I wanted to have a OSINT project, so I used burpsuite to map the request from the API and based on it I made the logic to get the following
for a public profile. It will get all the following and add it to a db, when you redo a scan it will tell you the new followings of the target
that we did not see during the previous scan.

## TODO
- A lot more can be improved especially the error handling 
- Loading state after starting scan
- Make a cool huntall page so we can just hunt everyone instead of 1 by 1 


## Usage: 

#### [input]

"targets.txt" contains 1 username for target with each line

#### [How To use it ?] 

1. get cookies from burpsuite and put them in the .env file,  the targets also have to be public for this to work

2. Have a mongoDB instance ready to store the result

3. Start the app and connect to it on localhost

4. Add a target and click on it to start a scan and add all the following in the DB 

5. You can then rescan the target to see if he followed anybody since the last scan


#### [Output]

All the newly following of a given target inside a nice a little page. 
