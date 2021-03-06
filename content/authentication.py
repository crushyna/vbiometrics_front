from flask import request, session, redirect, url_for, render_template, flash

from helpers.config_parser import ConnectionData
from helpers.user_check import AuthenticatingUser
import requests
import gc


class Authentication:

    @staticmethod
    def check_email():
        error = ''
        try:
            if request.method == 'POST':
                form_merchant_id = request.form['merchant_id']
                form_email = request.form['email']
                url = f"{ConnectionData.backend_server_address}/check_if_user_exists/{form_merchant_id}/{form_email}"
                response = requests.get(url)
                if response.status_code not in (200, 201):
                    error = "Email not found! Try again!"
                    return render_template("authenticate.html", error=error)
                else:
                    session['email'] = form_email
                    session['merchant_id'] = form_merchant_id
                    randomText = AuthenticatingUser.get_random_text(session['merchant_id'], session['email'])
                    if randomText['status'] == 'error':
                        error = str(randomText)
                        return render_template("authenticate.html", error=error)
                    else:
                        session['textphrase'] = randomText['message']['data']['textphrase']
                        session['text_id'] = randomText['message']['data']['text_id']
                        session['user_id'] = randomText['message']['data']['user_id']
                        return redirect(url_for("record_voice"))
            gc.collect()
            return render_template("authenticate.html", error=error)
        except Exception as e:
            flash(e)
            error = "Error!"
            return render_template("authenticate.html", error=error)

    @staticmethod
    def record_voice():
        return render_template('record_voice.html')
