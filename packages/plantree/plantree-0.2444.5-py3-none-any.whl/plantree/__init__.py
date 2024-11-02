from os import environ

from pybrary import Config

from plantree.config import defaults


app = 'plantree'
ext = environ.get(f'{app}_ext', 'json')
config = Config(app, defaults, ext)

