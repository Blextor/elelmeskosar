from flask import Flask, render_template_string, send_file

app = Flask(__name__)

# Az a fájl, amit letölthetővé szeretnél tenni
FAJL_UTVONAL = "D:/night/Elden Ring Nightreign update 1.01 - 1.01.1.exe"  # legyen ugyanebben a mappában

# Üres oldal sablon egy letöltés gombbal
HTML = """
<!DOCTYPE html>
<html lang="hu">
<head>
    <meta charset="UTF-8">
    <title>Letöltés</title>
</head>
<body style="display:flex;justify-content:center;align-items:center;height:100vh;">
    <form action="/download">
        <button type="submit">📥 Letöltés</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/download")
def download():
    return send_file(FAJL_UTVONAL, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
