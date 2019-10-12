# savedots
Easily and securely store and deploy your dotfiles

#### Using terminal only
##### Login
`curl -b cookie -c cookie -H 'Content-Type:application/json' savedots.me/api/login -d '{"email":"YOUR_EMAIL","password":"YOUR_PASSWORD"}'`

##### Upload file
`curl -b cookie -c cookie -F file=@FILE_PATH  savedots.me/api/upload`

##### Logout
`curl -c cookie -b cookie savedots.me/api/logout`

`TODO:`
-[ ] - Setup
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
