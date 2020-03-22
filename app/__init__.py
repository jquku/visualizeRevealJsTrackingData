from flask import Flask, render_template, redirect, url_for


app = Flask(__name__)
app.config.from_object('config')


from app.modules.Main.controllers import mod_main

app.register_blueprint(mod_main)
