import os

from flask import render_template


def check_key(key):
    return key == os.getenv('API_KEY')


def page_error_handling(render_flow):
    def wrapper(*args, **kwargs):
        try:
            return render_flow(*args, **kwargs)
        except Exception as e:
            return render_template('error.pug', title="Error", code=400, msg=str(e))
    wrapper.__name__ = render_flow.__name__
    return wrapper
