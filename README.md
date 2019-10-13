# savedots
Easily and securely store and deploy your dotfiles

`TODO:`

- [ ] - Setup
    - [ ] - create script to gather all dotfiles
    - [ ] - makefile
    - [ ] - documentation
  
- [ ] - Web
    - [ ] - API
       - [x] - login
       - [x] - logout
       - [x] - register
       - [ ] - upload deploy.gpg
       - [ ] - download deploy.gpg
       - [ ] - delete deploy.gpg
       - [ ] - list all deploy.gpg's
       - [ ] - validate email
   - [x] - ~~database~~
       - [x] - model
   - [ ] - frontend
       - [ ] - basic html + js
       - [ ] - css
       - [x] - under dev site
   - [x] - ~~Deploy~~
       - [x] - domain name
       - [x] - hosting
       - [x] - CA


#### Using terminal only
##### Login
`curl -b cookie -c cookie -H 'Content-Type:application/json' savedots.me/api/login -d '{"email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}'`

##### Upload file
`curl -b cookie -c cookie -F "sessionID=YOUR_SESSIONID" -F file=@FILE_PATH savedots.me/api/upload`

##### Logout
`curl -c cookie -b cookie -X GET -F "sessionID=YOUR_SESSIONID" --url savedots.me/api/logout`


##### Functions in script
```sh
# echoes SESSID or 0
login(){
    sessid=$(echo $(curl -b cookie -c cookie -H 'Content-Type:application/json' localhost:5000/api/login -d '{"email":"$1","password":"$2"}' | awk '$1 ~ /sessionID/ {print $2}' | sed s/\'//g) | sed s/\"//g)
    if [ ${#sessid} == 256 ] then 
        echo $sessid
    else
        echo 0
    fi
}
```
```sh
# logout user (needs sessionid as param
logout(){
    curl -c cookie -b cookie -X GET -F "sessionID=$1" --url savedots.me/api/logout
}
```
```sh
# uploads file param1: sessid, param2:file path
upload_file(){
    curl -b cookie -c cookie -F "sessionID=$1" -F file=@$2 savedots.me/api/upload
}
```

