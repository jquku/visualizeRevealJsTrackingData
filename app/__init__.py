from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Default route forwarding to dashboard
@app.route('/')
def default():
    return redirect(url_for('Main.main'))

from app.modules.Main.controllers import mod_main

app.register_blueprint(mod_main)
