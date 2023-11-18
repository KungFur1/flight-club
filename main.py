from flask import Flask, render_template, request, redirect, url_for
import flight_entry
import database_manager
from apscheduler.schedulers.background import BackgroundScheduler
import flight_search_logic
import config


app = Flask("Flight Club Website")


if database_manager.connectToDatabase():
    print("Successfully connected to DB")
else:
    print("Failed to connect to DB. Quiting")
    quit(123)


# Every 143 hours check every entry for available flights.
scheduler = BackgroundScheduler()
job = scheduler.add_job(lambda: flight_search_logic.checkEveryFlight(), 'interval', hours=71)
scheduler.start()


@app.route("/")
def home():
    return render_template("index.html")


# This is a secret api endpoint used for testing
@app.route("/secret_38913405ty27sdgl83aq4z597")
def secret_check_every_flight_call():
    flight_search_logic.checkEveryFlight()
    return "Every flight checked successfully!"


@app.route("/unsubscribe/<string:email>/<int:secret>")
def unsubscribe(email:str, secret:int):
    # Find email secret entry in database
    # Check if secret matches
    # Delete all things from database with this email
    if database_manager.emailAndSecretMatch(email, secret):
        database_manager.deleteAllDataWithEmail(email)
        return redirect(url_for("unsub"))
    else:
        print("Attempt to unsubscribe with wrong secret. Or a critical error!")
        return "Hey! That`s illegal."


@app.route("/unsub")
def unsub():
    return render_template("unsubscribe.html")


@app.route("/flight_form", methods=["GET", "POST"])
def flightForm():

    if request.method == "GET":
        return render_template("flight_form.html")

    elif request.method == "POST":
        try:
            entry = flight_entry.checkFormMakeFlightEntry(request.form)
        except NameError as error:
            print(error.args)
            return redirect(url_for("flightFormIATAError"))
        except Exception as error:
            print(error.args)
            return redirect(url_for("flightFormInputError"))

        try:
            database_manager.insertFlightEntry(entry)
        except BaseException as error:
            print("CRITICAL ERROR!")
            print(f"When trying to insert flight entry into database some exception occurred. Exception message: \n"
                  f"{error.args}")
            entry.print()
            return redirect(url_for("flightFormInputError"))

        print(f"New entry from {request.remote_addr} \n")
        entry.print()
        return redirect(url_for("flightFormSuccess"))


# Errors and success pages should all be in flight_form page
@app.route("/flight_form_iata_error")
def flightFormIATAError():
    return render_template("flight_form_error.html", error_message="Failed to find airport for your input city. Maybe "
                                                                   "the city you entered doesnt have an airport? If "
                                                                   "you are sure that there is an airport, you can "
                                                                   "always use the airports IATA code, which is made "
                                                                   "out of three capital letters eg. VNO for Vilnius "
                                                                   "airport.")


@app.route("/flight_form_input_error")
def flightFormInputError():
    return render_template("flight_form_error.html", error_message="Something went wrong while processing your form "
                                                                   "input. Make sure all the dates are correct.")


@app.route("/flight_form_success")
def flightFormSuccess():
    return render_template("flight_form_success.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)

    database_manager.discconectFromDatabase()
    print("Disconnected from DB")






