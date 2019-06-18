#!/usr/bin/env python
"""
Documentation

See also https://www.python-boilerplate.com/flask
"""
import os
import requests
import hashlib
import redis
import html

from flask import Flask, Response, request, jsonify
from flask_cors import CORS

def create_app(config=None):
    app = Flask(__name__)
    salt = 'UNIQUE SALT'
    default_name = 'Hello Arturo Blogs'
    cache = redis.Redis(host='redis', port=6379, db=0)

    # See http://flask.pocoo.org/docs/latest/config/
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    # Setup cors headers to allow all domains
    # https://flask-cors.readthedocs.io/en/latest/
    CORS(app)

    # Definition of the routes. Put them into their own file. See also
    # Flask Blueprints: http://flask.pocoo.org/docs/latest/blueprints
    @app.route("/hello")
    def hello_world():
        return "Hello World"

    @app.route("/foo/<someId>")
    def foo_url_arg(someId):
        return jsonify({"echo": someId})

    @app.route('/', methods=['GET', 'POST'])
    def mainpage():
        name = default_name

        if request.method == 'POST':
            name = html.escape(request.form['name'], quote=True)

        salted_name = salt + name
        name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

        header = '<html><head><title>Identidock</title></head><body>'
        body = '''<form method="POST">
        Hello <input type="text" name="name" value="{0}">
        <input type="submit" value="submit">
        </form>
        <p>You like a:
        <img src="/monster/{1}" />
        '''.format(name, name_hash)
        footer = '</body></html>'
        return header + body + footer


    @app.route('/monster/<name>')
    def get_identicon(name):

        name = html.escape(name, quote=True)
        image = cache.get(name)
        if image is None:
            print('Cache miss', flush=True)
            r = requests.get('http://dnmonster:8080/monster/' + name + '?size=80')
            image = r.content
            cache.set(name, image)

        return Response(image, mimetype='image/png')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", debug=True)