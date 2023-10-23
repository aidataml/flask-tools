from flask import Flask, render_template, request, redirect, session, flash
from surveys import satisfaction_survey
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"  

import logging

if __name__ == '__main__':
    logging.basicConfig(filename='error.log',level=logging.DEBUG)
    app.run(debug=True)


@app.route('/')
def show_survey_start():
    return render_template("start.html", survey=satisfaction_survey)


@app.route('/begin', methods=["POST"])
def start_survey():
    session["responses"] = []
    return redirect("/questions/0")


@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get("responses")

    if (responses is None) or (qid != len(responses)):
        flash('Invalid question id.')
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template("question.html", question=question)


@app.route('/answer', methods=["POST"])
def handle_answer():
    responses = session["responses"]
    answer = request.form['answer']
    responses.append(answer)
    session["responses"] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route('/complete')
def complete():
    return render_template("thank_you.html")
