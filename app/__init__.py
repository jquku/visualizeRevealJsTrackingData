from flask import Flask, render_template

app = Flask(__name__)

from app.modules.Main.controllers import mod_main

app.register_blueprint(mod_main)
