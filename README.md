# savedots
Easily and securely store and deploy your dotfiles

`TODO:`

- [ ] new app in django

- [ ] - Setup
    - [x] - create script to gather all dotfiles
    - [ ] - makefile
    - [ ] - documentation
  
- [ ] - Web
    - [ ] - API
       - [x] - login
       - [x] - logout
       - [x] - register
       - [x] - upload deploy.gpg
       - [x] - download deploy.gpg
       - [x] - delete deploy.gpg
       - [x] - list all deploy.gpg's
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

##### List all your files
`curl -b cookie -c cookie -X GET -F "sessionID=YOUR_SESSIONID" --url savedots.me/api/list_files`

##### Download file(use key returned from /api/list_files
`curl -b cookie -c cookie -X GET -F "sessionID=YOUR_SESSIONID" -F "fileID=KEY_FROM_list_files" --url savedots.me/api/download -o FILENAME`

##### Delete file(using key returned from /api/list_files)
`curl -b cookie -c cookie -X POST -F "sessionID=YOUR_SESSIONID" -F "fileID=KEY_FROM_list_files" savedots.me/api/remove_file`

##### Logout
`curl -c cookie -b cookie -X GET -F "sessionID=YOUR_SESSIONID" --url savedots.me/api/logout`
