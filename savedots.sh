###################################
# @author: kelj0
# @github: https://github.com/kelj0
# @year: 2019
###################################

###############################
# Functions
###############################

# logout user
# @param1:sessionID
logout(){
    curl -c cookie -b cookie -X GET -F "sessionID=$1" --url savedots.me/api/logout
}

# uploads file 
# @param1: sessionID, 
# @param2:file path
upload_file(){
    curl -b cookie -c cookie -F "sessionID=$1" -F file=@$2 savedots.me/api/upload
}

# downloads file 
# @param1: sessionID,
# @param2: fileID
download_file(){
    curl -b cookie -c cookie -X GET -F "sessionID=$1" -F "fileID=$2" --url savedots.me/api/download -O
}

# logins user
# return
# [sessionID] if successfull
# [0]         if login failed
login(){
    echo '<Login>' >&2
    echo 'Email: '>&2
    read email 
    echo 'Password: '>&2
    read -s password
    echo "Loging in with $email : $password">&2
    sessid=$(echo $(curl -b cookie -c cookie -H 'Content-Type:application/json' savedots.me/api/login -d "{'email':'$email','password':'$password'}" | awk '$1 ~ /sessionID/ {print $2}' | sed s/\'//g) | sed s/\"//g)
    if [ ${#sessid} == 256 ]; then 
        echo $sessid
    else
        echo 0
    fi
}

# registers new user or stops program execution
register(){
    echo '<Registration>' >&2
    while true; do
        read -p "Please enter your email:"
    done
    echo 'Email: '>&2
}

# downloads your dotfiles, decrypts them, and mv them where needed 
getDots(){
    echo "Getting your dotfiles..."
    echo "Implement me"
}

# collects,encrypts and uploads your dotfiles to server
saveDots(){
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
}

#################
# Program
#################

options=("Saving my dotfiles", "Downloading existing")
PS3="> "
echo "Are you saving your dots or downloading existing?"
select opt in "${options[@]}" "Quit";
do
    case $REPLY in
        1)
            echo "Saving dotifles"
            saveDots
            break
            ;;
        2)
            echo "Downloading existing"
            getDots
            break
            ;;
        3)
            echo "Quiting"
            break
            ;;
        *) echo "Invalid input!"
    esac
done
return 

echo "Thank you for using savedots by @kelj0"

