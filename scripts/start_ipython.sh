#!/bin/bash


docker run --rm -t -i \
-e "IPYTHON_COOKIE_SECRET=foobar" \
-e "IPYTHON_PASSWORD=sha1:2154cbd5c738:fccbb56b217a0057e3550c3087da4712da6dbaa4" \
-e "GITHUB_USER=foobar" \
-e "IPYTHON_REPO_URL=https://github.com/SDRDLAnalysts/ericbusboom.git" \
-e "IPYTHON_REPO_AUTH=$IPYTHON_REPO_AUTH" \
ipynb_ipython /bin/bash


