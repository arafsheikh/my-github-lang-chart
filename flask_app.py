from flask import Flask, render_template, request, Blueprint
from urllib import urlopen
from bs4 import BeautifulSoup
import chartkick

app = Flask(__name__)
ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(), static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")

def fetch(username):
	lang_dict = {}
	url = "https://github.com/" + username + "?tab=repositories"
	resp = urlopen(url)

	if resp.getcode() == 404:
		return "Username doesn't exist"
	elif resp.getcode() == 200:
		soup = BeautifulSoup(resp, "lxml")

		for repo_details in soup.find_all(class_='repo-list-stats'):
			repo_lang = str(repo_details.contents[0].strip())

			if repo_lang == "":
				repo_lang = "Other"

			if repo_lang in lang_dict:
				lang_dict[repo_lang] += 1
			else:
				lang_dict[repo_lang] = 1

		#return lang_dict
		return render_template("chart.html", user=username, data=lang_dict)
	else:
		return "There was an error"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
    	return fetch(request.form["username"])
    return render_template("index.html")

if __name__ == "__main__":
	app.run(debug=True)