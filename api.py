from io import BytesIO

from flask import Flask, request, send_file
from flask_cors import CORS

from standard import Client, utils, GB, HDB
from utils import net_is_used

app = Flask(__name__)
CORS(app)
gb = GB()
hb = HDB("hbba")
db = HDB("dbba")


# TODO:支持下载多个
# TODO:支持进度条反馈
# TODO: 支持国标下载重试
@app.route('/api/search/<t>')
def search(t):
    """搜索功能

    :param t:
    :return:
    """
    q = request.args.get('q')
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=15, type=int)
    client = Client(t).create()
    data = client.format_search_api(key=q, page=page, size=size)
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
    name = request.args.get("name", default="")

    if t == 'gb':
        res = gb_download(q)
    elif t in {'hb', 'db'}:
        res = hdb_download(q, name, t)
    else:
        return 404

    if not res['err']:
        return send_file(BytesIO(res["file"]), as_attachment=True, attachment_filename=res["name"], cache_timeout=0,
                         mimetype="application/pdf")
    else:
        return res, 404


def gb_download(hcno):
    g_name, c_name = gb.get_pdf_name(hcno)
    pdf_name = f"{g_name}({c_name})"

    pdf_name = utils.filter_file(pdf_name)

    pdf_bytes = gb.get_bytes(hcno)
    file_name = f"{pdf_name}.pdf"
    return {
        "err": "",
        "file": pdf_bytes,
        "name": file_name
    }


def hdb_download(key, name, t):
    """

    :param t:
    :param name:
    :param key:
    :return:
    """
    if t == "hb":
        bytes_io = hb.download_api(key)
    elif t == "db":
        bytes_io = db.download_api(key)
    else:
        return {
            "err": "参数只允许 hb 和 db两个",
            "file": "pdf_bytes",
            "name": "file_name"
        }
    return {
        "err": "",
        "file": bytes_io,
        "name": name
    }


if __name__ == '__main__':
    PORT = 23439
    if not net_is_used(PORT):
        app.run(port=PORT, debug=True)
    else:
        print("端口被占用")
