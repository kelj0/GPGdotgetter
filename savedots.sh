# logout user (needs sessionid as param
logout(){
    curl -c cookie -b cookie -X GET -F "sessionID=$1" --url savedots.me/api/logout
}
# uploads file param1: sessid, param2:file path
upload_file(){
    curl -b cookie -c cookie -F "sessionID=$1" -F file=@$2 savedots.me/api/upload
}
# echoes SESSID or 0
login(){
    echo '<Login>' >&2
    echo 'Email: '>&2
    read email 
    echo 'Password: '>&2
    read -s password
    echo "Loging in with $email : $password">&2
    echo 1
    return # for purpuses of testing dont actually login, just test io 
    sessid=$(echo $(curl -b cookie -c cookie -H 'Content-Type:application/json' savedots.me/api/login -d "{'email':'$email','password':'$password'}" | awk '$1 ~ /sessionID/ {print $2}' | sed s/\'//g) | sed s/\"//g)
    if [ ${#sessid} == 256 ]; then 
        echo $sessid>&2
    else
        echo 0
    fi
}
register(){
    echo '<Registration>'
    echo 'register() implement me '
}


echo "Welcome to your one stop to safe dots"
while true; do
    read -p "Do you have account at savedots.me(y/N)?" yn
    case $yn in
        [Yy]* )
            SESSID=$(login)
            if [ $SESSID == 1 ]; then
                echo "Uploading file with SESSID> $SESSID"
            else
                echo "Wrong email or password!"
            fi
            break;;
        [Nn]* )
            register
            break;;
        * ) echo "Please answer y or n.";;
    esac
done
