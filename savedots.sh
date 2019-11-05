#!/usr/bin/env bash

###################################
# @author: kelj0
# @github: https://github.com/kelj0
# @year: 2019
###################################
# Globals #
###########
URL="localhost:5000"
###############################
# Functions #
#############

# logout user
# @param1:sessionID
logout(){
    curl -c cookie -b cookie -X GET -F "sessionID=$1" --url $URL/api/logout
}

# uploads file 
# @param1: sessionID, 
# @param2:file path
upload_file(){
    curl -b cookie -c cookie -F "sessionID=$1" -F file=@$2 $URL/api/upload
}

# downloads file 
# @param1: sessionID,
# @param2: fileID
download_file(){
    curl -b cookie -c cookie -X GET -F "sessionID=$1" -F "fileID=$2" --url $URL/api/download -O
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
    sessid=$(echo $(curl -s -b cookie -c cookie -H 'Content-Type:application/json' $URL/api/login -d "{'email':'$email','password':'$password'}" | awk '$1 ~ /sessionID/ {print $2}' | sed s/\'//g) | sed s/\"//g)
    if [ ${#sessid} == 256 ]; then 
        echo $sessid
    else
        echo 0
    fi
}

# registers new user or stops program execution
register(){
    echo '<Registration>' >&2
    echo 'Email:'>&2
    read email
    echo 'Password:'>&2
    read -s password
    echo 'Repeat password:'>&2
    read -s rpassword
    if [ $password != $rpassword ]; then
        echo 'Your passwords dont match!'>&2
        register
    else
        resp=$(curl -b -c -H 'Content-Type:application/json' $URL/api/register -d "{'email': '$email', 'password': '$password', 'rpassword': '$rpassword'}") 
        if [ $(echo $resp | awk '$1 ~ /code/ {print $2}') != 201 ]; then
            echo $resp >&2 
            register
        else
            echo 'Successfully created new account'>&2
        fi
    fi
    
}

gatherAndCompressDots(){
    cd ~
    mkdir $1"_TEMP_/"
    mkdir $1"_TEMP_/.config/"
    for f in ./.config/*
    do
        echo "[+] Backuping $f"
        if [[ $(du -cs $f | awk '$2 ~ /total/ {print $1}') -gt 10000 ]]; then
            read -p "[!] $f is bigger than 10000 do you really want to backup that?" yn;
            case $yn in
                [Yy]* )
                    cp -r ./config/$f $1"_TEMP_/.config/"
                    ;;
                [Nn]* )
                    echo -e "[ \e[32mOK\e[0m ] skipping $f"
                    ;;
            esac
        fi;
    done
    while true; do
        read -p "[?] Do you want to backup your ssh keys?(y/N)" yn
        case $yn in
            [Yy]* )
                if [ -d "./.ssh"  ]; then
                    cp -r ./.ssh $1"_TEMP_/" 
                else
                    echo "[!] Cant find your .ssh folder, im skipping"
                fi
                ;;
            [Nn]* )
                echo -e "[ \e[32mOK\e[0m ] skipping .ssh"
                break
                ;;
            * )
                echo "[!] Please answer y or n" ;;
        esac
    done
    7z a $1".7z" $1"_TEMP_/"
    gpg -c --cipher-algo AES256 $1".7z"
    rm -rf $1"_TEMP_"
    rm -rf $1".7z"
}

# downloads your dotfiles, decrypts them, and mv them where needed 
getDots(){
    echo '<Get Dots>' # TODO
    res=$(echo $(curl -b cookie -c cookie -X GET -F "sessionID=$1" --url $URL/api/list_files))
    res=$(echo $res | tail -n +2 | head -n -2) # clear from brackets and status code
    downloadTokens=$(echo $res | awk '{print $1}' | set 's/://g;s/"//g')
    downloadNames=$(echo $res | awk '{print $1}' | set 's/://g;s/"//g')
    readarray -t y <<<$(echo $res | tail -n +2 | head -n -2 | awk '{print $1}' | sed 's/://g;s/"//g')
    # TODO: choose dots to save and unpack them
    # while true; do
    #     read -p "[?] Choose dots to restore"
    #     case $yn in
    #      

    # done
}

# collects,encrypts and uploads your dotfiles to server
saveDots(){
    echo '<Save dots>'
    read -p "[?] How do you want to call your dots: " gpgName
    gatherAndCompressDots $gpgName
    upload_file $1 $gpgName".7z.gpg"
}

# echoes your package manager
getPackageManager(){
    declare -A osInfo;
    osInfo[/etc/redhat-release]=yum
    osInfo[/etc/arch-release]=pacman
    osInfo[/etc/gentoo-release]=emerge
    osInfo[/etc/SuSE-release]=zypp
    osInfo[/etc/debian_version]=apt-get
    for f in ${!osInfo[@]}
    do
        if [[ -f $f ]]; then
            echo ${osInfo[$f]}
        fi
    done
}

###########################
# Entry point #
###############
echo "Checking if you are root(needed if you dont have gpg installer on system)"
if [ $(whoami) != "root" ]; then 
    echo "[!] You are not root"; 
else 
    echo "[+] You are root"; 
fi;
PACKAGE_MANAGER=$(getPackageManager)
echo "Your package manager is $PACKAGE_MANAGER"
echo "Installing gpg and 7z"
sudo $PACKAGE_MANAGER install gpg p7zip-full -y
echo "Now you're good to go"

echo "Welcome to your one stop to safe dots"
while true; do
    read -p "[?] Do you have account at $URL(y/N)?" yn
    case $yn in
        [Yy]* )
            SESSID=$(login)
            if [ $SESSID == 0 ]; then
                echo "[!] Wrong email or password!"
            else
                echo -e "[ \e[32mOK\e[0m ] Successfully logged in"
                break
            fi
            ;;
        [Nn]* )
            register
            SESSID=$(login)
            if [ $SESSID == 0 ]; then
                echo "[!] Wrong email or password!"
            else
                echo -e "[ \e[32mOK\e[0m ] Successfully logged in"
                break
            fi
            ;;
        * ) echo "[!] Please answer y or n.";;
    esac
done
options=("Saving my dotfiles", "Downloading existing")
PS3="> "
echo "[?] Are you saving your dots or downloading existing?"
select opt in "${options[@]}" "Quit";
do
    case $REPLY in
        1)
            echo "Saving dotifles"
            saveDots $SESSID
            break
            ;;
        2)
            echo "Downloading existing"
            getDots $SESSID
            break
            ;;
        3)
            echo "Quiting"
            break
            ;;
        *) echo "Invalid input!"
    esac
done

echo "Thank you for using savedots by @kelj0"

