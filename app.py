from flask import Flask, render_template, request, session, redirect, url_for
from calculate import recommend

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route("/form_submit", methods=["POST"])
def form_submit():
    taste = request.form['taste']
    flavor = request.form['flavor']
    t_f = request.form['taste_flavor']
    t_p = request.form['taste_popularity']
    f_p = request.form['flavor_popularity']

    recommend_sake_list = recommend(taste, flavor, t_f, t_p, f_p)
    session["recommend_sake_list"] = recommend_sake_list

    return redirect(url_for('result'))


@app.route('/result', methods=["GET"])
def result():
    if 'recommend_sake_list' not in session:
        return redirect(url_for('index'))

    return render_template("result.html", sake_list=session["recommend_sake_list"])


if __name__ == "__main__":
    app.run(debug=True)
