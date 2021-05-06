### Projects specs


#### Routes
- /login
- /logout
- /register
- /user
- /script/download
- /dots/download/<id>
- /dots/<id>
- /upload
- /dots/edit

#### Models (approx)
* user
    * id
    * username
    * email
    * password
* dotfile
    * name
    * owner

`dotfile m<->n user`, but owner is the one that uploaded it and can change it


