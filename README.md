# Instagram Stalker for myself 

## What is this ? 

> I wanted to have a OSINT project, so I used burpsuite to map the request from the API and based on it I made the logic to get the following
for a public profile. It will get all the following and add it to a db, when you redo a scan it will tell you the new followings of the target
that we did not see during the previous scan.

## TODO
- A lot more can be improved especially the error handling 
- Loading state after starting scan
- Make a cool huntall page so we can just hunt everyone instead of 1 by 1 


## Usage: 

[input] "targets.txt" contains 1 username for target with each line

[How To use it ?] get cookies from burpsuite and put them in the .env file,  the targets also have to be public for this to work

[Output] "data/{name}_{curr_date}" with every following that the user has 
