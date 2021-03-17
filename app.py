from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey 

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def survey_home():
    """Create form to initialize survey."""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions


    return render_template("survey_home.html", title=title, instructions=instructions)



@app.route("/begin", methods=["POST"])
def start_survey(): 
    session["responses"] = []
    return redirect("/questions/0")



@app.route("/questions/<int:q>")
def show_question(q):
    """Show current question, and protect from improper access."""

    responses = session.get("responses")

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")

    if (len(responses) != q):
        flash(f"Invalid question id: {q}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[q]
    return render_template("question.html", question_num=q, question=question)



@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    responses = session["responses"]
    responses.append(choice)
    session["responses"] = responses

    

    if (len(responses) == len(satisfaction_survey.questions)):
        # survey complete
        return redirect("/complete")
    else:
        # more questions remain
        return redirect(f"/questions/{len(responses)}")



@app.route("/complete")
def complete():
    """Show final page."""

    return render_template("finished.html")


