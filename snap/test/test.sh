#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR"

vagrant up
vagrant upload ../../story_0.14.3_amd64.snap
vagrant ssh -c "sudo snap install --dangerous story_0.14.3_amd64.snap && story"
vagrant halt
