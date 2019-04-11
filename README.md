# Calender API

This API will take a given court day and return a word docx file containing the necessary events.

# How to run locally
Make sure python 3 and pip 3 are installed

`cd CalenderApi`

`pip3 install requirements.txt`

`python3 api.py`

# How to deploy
`cd CalenderApi`

`docker build -t api:alpine .`

`docker run -p 4000:4000 api:apline`

Then upload to a docker host
