from fetch_data import save_all,save_topics
from flask import Flask, render_template, send_file, request, url_for, redirect


app = Flask(__name__)

@app.route('/refresh',methods=['GET','POST'])
def refresh_stats():
  save_topics()
  save_all
  return render_template('index.html')


@app.route('/rentByInflation')
def rentByInflation():
  x=''
  return send_file(x, mimetype='image/png')


@app.route('/housing')
def housing():
  x=''
  return send_file(x, mimetype='image/png')





if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)