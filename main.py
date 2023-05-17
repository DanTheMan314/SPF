from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from googleapiclient.discovery import build, HttpError
from comment_scraper import get_comments, comment_printer
from comment_scraper import api_key
from preprocessor import preprocess_tool
from predict import spredicter,opredicter,rpredicter

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        try:
            temp = url.split("=")
            id = temp[1]
        except:
            temp = url.split("/")
            id = temp[-1]
        return redirect(url_for('loading', video_id=id))
    else:
        return render_template('home.html')

@app.route("/+<video_id>")
def loading(video_id):
    global api_key
    yt_object = build('youtube', 'v3', developerKey=api_key)
    try:
        get_comments(yt_object, video_id, '')
        comments = comment_printer()
        comments = preprocess_tool(comments)
        sentiments = []
        offensive = []
        relevance = []
        for i in range(len(comments)):
            value = spredicter(comments[i][0])
            sentiments.append([value,[]])
            for j in range(len(comments[i][1])):
                value  = spredicter(comments[i][1][j])
                sentiments[i][1].append(value)
        for i in range(len(comments)):
            value = opredicter(comments[i][0])
            offensive.append([value,[]])
            for j in range(len(comments[i][1])):
                value  = opredicter(comments[i][1][j])
                offensive[i][1].append(value)
        for i in range(len(comments)):
            value = rpredicter(comments[i][0])
            relevance.append([value,[]])
            for j in range(len(comments[i][1])):
                value  = rpredicter(comments[i][1][j])
                relevance[i][1].append(value)
        return render_template('loading.html', comment=comments,sentiment=sentiments,offend=offensive,relevant=relevance)
    except HttpError:
        return f"<h1>Comment has been turned off or wrong url</h1>"

if __name__ == "__main__":
    app.run(debug=True)