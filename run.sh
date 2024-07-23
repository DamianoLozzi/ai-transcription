#!/bin/bash


UPDATED=0

# update the package list
update_package_list() {
    if [ $UPDATED -eq 0 ]; then
        echo -e "\e[36mUpdating package list\e[0m"
        sudo apt update -y && echo -e "Package list updated" || (echo -e "\e[31mFailed to update package list\e[0m" && exit 1)
        UPDATED=1
    fi
}

setup(){
# if ffmpeg is not installed, install it
if ! [ -x "$(command -v ffmpeg)" ]; then
    echo -e "\e[36mInstalling ffmpeg\e[0m"
    update_package_list
    sudo apt install ffmpeg -y && echo -e "ffmpeg installed" || (echo -e "\e[31mFailed to install ffmpeg\e[0m" && exit 1)
else 
    echo -e "\e[32mffmpeg already installed\e[0m"
fi

# if python3 is not installed, install it
if ! [ -x "$(command -v python3)" ]; then
    echo -e "\e[36mInstalling python3\e[0m"
    update_package_list
    sudo apt install python3 -y && echo -e "python3 installed" || (echo -e "\e[31mFailed to install python3\e[0m" && exit 1)
else
    echo -e "\e[32mpython3 already installed\e[0m"
fi

# if python3-venv is not installed, install it
if !  dpkg -s python3-venv &> /dev/null ; then
    echo -e "\e[36mInstalling python3-venv\e[0m"
    update_package_list
    sudo apt install python3-venv -y && echo -e "python3-venv installed" || (echo -e "\e[31mFailed to install python3-venv\e[0m" && exit 1)
else
    echo -e "\e[32mpython3-venv already installed\e[0m"
fi

# if pip is not installed, install it
if ! [ -x "$(command -v pip)" ]; then
    echo -e "\e[36mInstalling pip\e[0m"
    update_package_list
    sudo apt install python3-pip -y && echo -e "pip installed" || (echo -e "\e[31mFailed to install pip\e[0m" && exit 1)
else
    echo -e "\e[32mpip already installed\e[0m"
fi

# if git is not installed, install it
if ! [ -x "$(command -v git)" ]; then
    echo -e "\e[36mInstalling git\e[0m"
    update_package_list
    sudo apt install git -y && echo -e "git installed" || (echo -e "\e[31mFailed to install git\e[0m" && exit 1)
else
    echo -e "\e[32mgit already installed\e[0m"
fi

# create a virtual environment if it does not exist
if [ ! -d "venv" ]; then
    echo -e "\e[36mCreating virtual environment\e[0m"
    python3 -m venv venv && echo -e "\e[32mVirtual environment created\e[0m" || (echo -e "\e[31mFailed to create virtual environment\e[0m" && exit 1)
else
    echo -e "\e[32mVirtual environment already exists\e[0m"
fi

# activate the virtual environment
source venv/bin/activate && echo -e "\e[32mVirtual environment activated\e[0m" || (echo -e "\e[31mFailed to activate virtual environment\e[0m" && exit 1)

# install requirements if not already installed
if [ ! -f ".install_done" ]; then
    echo -e "\e[36mInstalling requirements\e[0m"
    pip install -r requirements.txt && touch .install_done && echo -e "\e[32mRequirements installed\e[0m" || (echo -e "\e[31mFailed to install requirements\e[0m" && exit 1)
else
    echo -e "\e[32mRequirements already installed\e[0m"
fi
}

echo -e "\e[36mSetting up the environment\e[0m"
setup && echo -e "\e[32mSetup complete\e[0m" || (echo -e "\e[31mSetup failed\e[0m" && exit 1)


# run the flask app
echo -e "\e[36mRunning the flask app\e[0m"
flask run && echo -e "\e[32mExited successfully\e[0m" || echo -e "\e[31mExited with error code $?\e[0m"