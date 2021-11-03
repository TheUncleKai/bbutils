#!/bin/bash

f=upload.sh

CURRENT=`pwd`
PASSWORD_FILE=.user_data.sh

error() {
    RC=$?
    if [ ! $RC -eq 0 ] ; then
        echo -e "\e[1;31mERROR:\e[0;0m Error $? ${1:-no error message provided}";
        exit ${$RC};
    fi
}


inform() {
    echo -e "\e[1;32mInfo:\e[0;0m ${1}";
}


warning() {
    echo -e "\e[1;33m*** Warning:\e[0;0m ${1}";
}

create-package() {
    inform "Create"

    rm dist/*
    python setup.py sdist bdist_wheel
}

upload-test() {
    inform "Upload test"

    if [ -z "$PASSWORD_FILE" ]
    then
        echo "Unable to find login data"
        exit 1
    fi
    source $PASSWORD_FILE
    inform "Use $USERNAME_TEST"
}

upload-dist() {
    inform "Upload dist"

    if [ -z "$PASSWORD_FILE" ]
    then
        echo "Unable to find login data"
        exit 1
    fi
    source $PASSWORD_FILE
    inform "Use $USERNAME_DIST"
}


case "$1" in
    create)
        create-package
        ;;

    test)
        upload-test
        ;;

    dist)
        upload-dist
        ;;

    *)
        echo "Usage: $f ( create | test | dist )"
        ;;
esac
