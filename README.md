Django project, that helps parse and sort Atlassian addons from https://marketplace.atlassian.com/addons/top-selling

1) Create virtualenv
2) Install requirements.txt
3) Run ./manage.py migrate
4) Run ./manage.py parse to get all items into DB
5) Run ./manage.py export to get csv file with sorted by download count items

Enjoy!