from flask import Flask

app = Flask(__name__)


@app.route('/')
def test_method():
    return "Tested and Trusted!"


if __name__ == '__main__':
    app.run()
