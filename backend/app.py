from flask import Flask, request, jsonify, render_template
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
import hfapi

# define a variable to hold you app
app = Flask(__name__)

# Perform summerization

client = hfapi.Client()

def get_summary(text):
    initial_len = len(text.split())
    desired_len = initial_len//3

    json = {
        "inputs": text,
        "parameters": {
            "min_length": desired_len,
            "max_length": initial_len,
        }
    }
    summary = client.summarization(json, model='sshleifer/distilbart-cnn-12-6')[0]['summary_text']
    return summary

# function which return Transcript
def get_trans(video_id):
    trans = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US','en'])
    text = ""
    for t in trans:
        text += (t['text']+" ")
        if len(text.split()) > 1000:
            break
    return text

# define your resource endpoints
@app.route('/')
def index_page():
    return "Hello world you can use this app now!"

@app.route('/time', methods=['GET'])
def get_time():
    return str(datetime.datetime.now())

@app.route('/trans', methods=['POST','GET'])
# Example GET localhost:5000/trans?v=AbCTlemwZ1k
def trans_print():
    id = request.args.get('v')
    transcript = get_trans(id)
    summary = get_summary(transcript)
    json = {
        "trans": transcript,
        "summary": summary
    }
    return render_template('index.html',video_id=id, summary=json['summary'], transcript=json['trans'], link_url='https://www.youtube.com/embed/'+id)

# server the app when this file is run
if __name__ == '__main__':
    app.run()