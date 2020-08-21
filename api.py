from pathlib import Path

from flask import Flask, request, send_file
from flask_cors import CORS

from standard import Client, utils, GB
from utils import net_is_used

app = Flask(__name__)
CORS(app)
gb = GB()

# TODO: 支持国标、地标、行标的下载
# TODO: 接口的改造，以便完成下一个 TODO
# TODO: 不再传递文件路径，而是 IO
# TODO: download check的全覆盖


@app.route('/api/search/<t>')
def search(t):
    """搜索功能

    :param t:
    :return:
    """
    q = request.args.get('q')
    client = Client(t).create()
    data = client.format_search_api(key=q, page=1, size=15)
    return data


@app.route('/api/download_check/<t>')
def download_check(t):
    """检查标准能否下载

    :param t:
    :return:
    """
    key = request.args.get('key')
    client = Client(t).create()
    can_download = client.can_download(key)
    if can_download:
        return {"status": 1}
    else:
        return {"status": 0}


@app.route('/api/download/<t>')
def download(t):
    """下载标准

    :param t:
    :return:
    """
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
    if not res['err']:
        path = str(res['path'])
        return send_file(path)
    else:
        return "aaa", 404


def gb_download(hcno, path=Path(".")):
    if not gb.can_download(hcno):
        return {
            "err": "该文件不支持下载",
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
