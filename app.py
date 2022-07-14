import os
from flask import Flask, send_from_directory, request
import requests


app = Flask(__name__)


@app.route("/")
def name():
	return """
	<h1>    Its Working <h1>
	"""
	
@app.route("/help")
def help():
	help_cmd = "python3 main.py run -h"
	text = os.popen(help_cmd).read()
	return text
	
@app.route("/install-requirements")
def install_requirements():
	os.system("pip install -r requirements.txt")
	
	return "   Success Installing requirements"
	
@app.route("/install-checkpoints")
def install_checkpoints():
	os.system("wget -O ./model.zip https://github.com/dreamnettech/dreampower-checkpoints/releases/download/0.0.1/v0.0.1.zip")
	os.system("unzip ./model.zip")
	os.system("rm model.zip")
	return "SUCCESS"
	
	

@app.route('/input-images/<path:filename>')
def download_file(filename):
    root_dir = os.path.abspath(os.curdir)
    return send_from_directory(root_dir + "/input/",filename, as_attachment=False)
    
@app.route("/output-images/<path:filename>")
def output_images(filename):
	root_dir = os.path.abspath(os.curdir)
	return send_from_directory(root_dir + "/output", filename, as_attachment=False)

    
@app.route("/start")
def start():
	url = str(request.args.get('url'))
	img_name = str(request.args.get('img'))
	img = url
	img_data = requests.get(url).content
	root_dir = os.path.abspath(os.curdir)
	with open(root_dir + '/input/' + img_name + '.jpg', 'wb') as handler:
		handler.write(img_data)
	input_path = root_dir + "/input/" + img_name + ".jpg"
	output_path= root_dir + "/output/" + img_name + ".jpg"
	cmd = f"python3 main.py run -i {input_path} -o {output_path} --auto-resize" 
	os.system(cmd)
	
	return f"""
	<img src = {img}> </img>
	"""


if __name__ == "__main__":
	app.run()
	
	
#cmd = "python3 main.py run -i input/test.jpg -o output/test.jpg -a altered -c checkpoints --auto-resize"

#os.system(cmd)
