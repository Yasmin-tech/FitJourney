#!/usr/bin/env python3
"""
    Flask app for the frontend
    """

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/signup', methods=['GET'], strict_slashes=False)
def signup_form():
    return render_template('signup_form.html')

# @app.route('/signup', methods=['POST'], strict_slashes=False)
# def sign_up():

if __name__ == "__main__":
    app.run(host="localhost", port=5002)
    