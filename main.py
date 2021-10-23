from flask import Flask, render_template, request, redirect, url_for, Response, send_file
import os
from os.path import join, dirname, realpath
from model import write_code, run_code, show_df, show_plot
import pandas as pd
import numpy as np
from os import listdir
from IPython.core.display import display


import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure



app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/tool")
def tool():
    pd.options.display.width = 0
    filename = listdir("static/files")
    df = pd.read_csv(f'static/files/{filename[0]}_copy')
    text = write_code("Show the first 10 rows")
    exec(f"res = " +  text)
    df_preview =  eval(f"res")
    return render_template("tool.html", df_preview=df_preview)


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
    
    try:
        # get the uploaded file
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            uploaded_file.save(file_path)
                # save the file
            
            filename = listdir("static/files")
            df_copy = pd.read_csv(f'static/files/{filename[0]}')
            df_copy.to_csv(f'static/files/{filename[0]}_copy')

            return redirect(url_for('tool'))

        else:
            return render_template("home_error.html")
    
    except Exception as error:
	    return render_template("home_error.html")

@app.route('/tool', methods=['POST'])
def df_manipulation():

    try: 

        text = request.form['text']
        output = run_code(text)
        dataframe = show_df()
        code = write_code(text)

        pd.options.display.width = 0
        filename = listdir("static/files")
        df = pd.read_csv(f'static/files/{filename[0]}_copy')
        text = write_code("Show the first 10 rows")
        exec(f"res = " +  text)
        df_preview =  eval(f"res")

        return render_template("tool.html", output=output, dataframe=dataframe, code=code, df_preview=df_preview)

    except Exception as error:
	    return render_template("tool_error.html")

@app.route("/save_as_csv/", methods=['POST'])
def save_as_csv():
    csv_file = pd.read_csv(f'static/files/{listdir("static/files")[0]}')
    return Response(
       csv_file.to_csv(),
       mimetype="text/csv",
       headers={"Content-disposition":
       "attachment; filename=dscodex_file.csv"})


if __name__ == "__main__":
    app.run(debug=True)