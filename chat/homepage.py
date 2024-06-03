from flask import Flask, Blueprint,send_file,render_template,url_for
from chatgpt import app1
from upload import upload_file
# from post.routes import post_bp

app = Flask(__name__,template_folder='templates')


# @app.route('/')
# def serve_html():
#     return send_file("templates/homepage.html")
#
@app.route('/')
def index():
    return render_template('homepage.html')

# 注册蓝图
app.register_blueprint(app1)

if __name__ == "__main__":
    app.run(debug = True)