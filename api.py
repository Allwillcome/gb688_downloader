from pathlib import Path

from flask import Flask, request, send_file
from flask_cors import CORS
from utils import net_is_used
from standard import Client, utils, GB

app = Flask(__name__)
CORS(app)
gb = GB()


@app.route('/api/search/<t>')
def search(t):
    q = request.args.get('q')
    client = Client(t).create()
    data = client.format_search_api(key=q, page=1, size=15)
    return data


@app.route('/api/download_check/<t>')
def download_check(t):
    key = request.args.get('key')
    client = Client(t).create()
    can_download = client.can_download(key)
    if can_download:
        return {"status": 1}
    else:
        return {"status": 0}


@app.route('/api/download/<t>')
def download(t):
    q = request.args.get('key')
    if t == 'gb':
        res = gb_download(q)
        # res = {
        #     "err": "",
        #     "path": "gui.py",
        #     "sasa": "adsa"
        # }
    # elif t == 'hb':
    #     data = hb.download(q)
    # elif t == 'db':
    #     data = db.download(q)
    else:
        return "bbb", 404
    print(res['err'])
    if not res['err']:
        print("aa", res['path'])
        path = str(res['path'])
        return send_file(path)
    else:
        return "aaa", 404


def gb_download(hcno, path=Path(".")):
    if not gb.can_download(hcno):
        return {
            "err": "该文件不支持下载",
            "path": ""
        }

    g_name, c_name = gb.get_pdf_name(hcno)
    pdf_name = f"{g_name}({c_name})"

    pdf_name = utils.filter_file(pdf_name)

    pdf_bytes = gb.get_bytes(hcno)

    file_path = path / f"{pdf_name}.pdf"
    with open(file_path, "wb") as f:
        f.write(pdf_bytes)
    return {
        "err": "",
        "path": file_path
    }


if __name__ == '__main__':
    PORT = 23439
    if not net_is_used(PORT):
        app.run(port=PORT)
    else:
        print("端口被占用")
