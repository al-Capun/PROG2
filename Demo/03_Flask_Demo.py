from flask import Flask

app = Flask("Demo")


@app.route('/hello/<name>')
def begruessung(name):
    return "Hallo " + name + "!"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
