# SousMot

Wordle-like game in multiplayer developped in django.

Website : [SousMot](https://motus.srvz-webapp.he-arc.ch/)

## Requirements

Python 3.6+ (See [Django doc](https://docs.djangoproject.com/en/3.2/releases/3.2/#python-compatibility) for more infos)

All the other requirements are in the `requirements.txt` file.

## Installation

1. Clone the repository
2. (Optional) Create a virtual environment
```bash
python3 -m venv .venv
```
3. (Optional) Activate the virtual env
```bash
source .venv/bin/activate 
```
4. Install the dependance in the `requirements.txt` file
```
pip3 install -r requirements.txt
```
5. Run the server
```
python3 manage.py runserver
```
6. ???
7. Profit !

### Continuous Deployment

This project use [Capistrano](https://capistranorb.com/) for continuous deployment.

Every commit on `master` publish it on the production server via GitHub Action