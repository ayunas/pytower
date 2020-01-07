import os

HEROKU = os.environ.get('HEROKU', 'false')

if HEROKU == 'true':
    from .production import *
else:
    from .development import *