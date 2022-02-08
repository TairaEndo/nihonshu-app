from flask import Flask, render_template, request
from calculate import recommend

app = Flask(__name__)

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

    # print(taste, flavor, t_f, t_p, f_p)
    # recommend_sake = get_recommend_sake(sake_list, quadrant, [t_f, t_p, f_p])
    recommend_sake = recommend(taste, flavor, t_f, t_p, f_p)
    # print(recommend_sake)

    return render_template("result.html",
                           title='This is Bootstrap sample',
                           message='Hello!',
                           sake_list = recommend_sake ,
                           )

if __name__ == "__main__":
    app.run(debug=True)
