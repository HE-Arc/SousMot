# SousMot

Wordle-like game in multiplayer developped in django.

Website : [SousMot](https://motus.srvz-webapp.he-arc.ch/)

## Requirements

Python 3.8+ (See [Django doc](https://docs.djangoproject.com/en/4.0/releases/4.0/#python-compatibility) for more infos)

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
5. Copy the `.env` file ! (It's in the `sousmot` folder)
```
cp sousmot/.env.example sousmot/.env
```
6. Generate a secret key to put into the `.env` file (`SOUSMOT_SECRET_KEY`)
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
7. Run the server
```
python3 manage.py runserver
```
8. ???
9. Profit !

### Continuous Deployment

This project use [Capistrano](https://capistranorb.com/) for continuous deployment.

Every commit on `master` publish it on the production server via GitHub Action

### Load words

In file `link.txt`, you found a link to download words.json. It's a file with all french words. 

To load data in your app, use command : `python manage.py loaddata words.json`