from flask import Flask, render_template, request

# 建立 Flask 應用程式
app = Flask(__name__)

import json

# 從 JSON 檔案讀取百岳資料
def load_mountains():
    with open("mountains.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 首頁：顯示所有山岳清單
@app.route("/")
def index():
    keyword = request.args.get("q", "")
    mountains = load_mountains()

    if keyword:
        result = [m for m in mountains if keyword in m["name"]]
    else:
        result = mountains

    return render_template("index.html", mountains=result, keyword=keyword)

# 詳細頁面：顯示單一山岳資訊
@app.route("/mountain/<name>")
def mountain_detail(name):
    mountains = load_mountains()
    # 用山名找到對應的資料
    mountain = next((m for m in mountains if m["name"] == name), None)
    return render_template("detail.html", mountain=mountain)

if __name__ == "__main__":
    app.run(debug=True)