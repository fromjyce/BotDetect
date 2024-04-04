from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from databootstrap import DataBootstrap
from graphfeatures import GraphFeatures
from preprocessing import DataPreprocessing
from predictionmodel import PredictionModel

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
CSV_FOLDER = 'csv'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(CSV_FOLDER):
    os.makedirs(CSV_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CSV_FOLDER'] = CSV_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'pcap_file' not in request.files:
        return 'No file part'
    file = request.files['pcap_file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        pcap_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(pcap_path)
        df, graph = DataBootstrap(pcap_path).run()
        prop_df = GraphFeatures(graph).run()
        cleaned_df = DataPreprocessing(prop_df).run()
        csv = PredictionModel(cleaned_df, prop_df).run()
        return render_template('index.html', csv_file=csv)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)