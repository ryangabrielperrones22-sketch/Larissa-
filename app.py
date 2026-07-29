"""
NEXUS Platform — Unified futuristic dashboard
Serve os módulos HTML + memória de arquivos Excel por módulo.
Run:  python app.py
Then open http://127.0.0.1:5000  (ou 0.0.0.0 para celular)
"""

from flask import Flask, render_template, send_from_directory, request, jsonify, send_file
import os
import json
from datetime import datetime

app = Flask(__name__)
BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")
DATA = os.path.join(BASE, "data")
META_FILE = os.path.join(DATA, "meta.json")

ALLOWED_MODULES = {
    "planner": "planner.html",
    "meta": "meta_ads.html",
    "extrato": "extrato.html",
    "notas": "notes.html",
    "agenda": "agenda.html",
}

os.makedirs(DATA, exist_ok=True)


def load_meta():
    if not os.path.exists(META_FILE):
        return {}
    try:
        with open(META_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_meta(meta):
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/module/<name>")
def module(name):
    if name not in ALLOWED_MODULES:
        return "Módulo não encontrado", 404
    return send_from_directory(STATIC, ALLOWED_MODULES[name])


@app.route("/health")
def health():
    return {"status": "ok", "platform": "NEXUS"}


@app.route("/api/status")
def api_status():
    """Quais módulos têm arquivo salvo."""
    meta = load_meta()
    out = {}
    for mod in ALLOWED_MODULES:
        info = meta.get(mod)
        if info and os.path.exists(os.path.join(DATA, info.get("stored_name", ""))):
            out[mod] = {
                "filename": info.get("original_name"),
                "saved_at": info.get("saved_at"),
                "size": info.get("size"),
            }
        else:
            out[mod] = None
    return jsonify(out)


@app.route("/api/save/<module>", methods=["POST"])
def api_save(module):
    """Salva o Excel do módulo em disco (memória persistente)."""
    if module not in ALLOWED_MODULES:
        return jsonify({"ok": False, "error": "módulo inválido"}), 400

    if "file" not in request.files:
        return jsonify({"ok": False, "error": "nenhum arquivo"}), 400

    f = request.files["file"]
    if not f.filename:
        return jsonify({"ok": False, "error": "nome vazio"}), 400

    # extensão segura
    original = f.filename
    ext = os.path.splitext(original)[1].lower()
    if ext not in (".xlsx", ".xls", ".csv"):
        ext = ".xlsx"

    stored_name = f"{module}{ext}"
    path = os.path.join(DATA, stored_name)
    f.save(path)

    meta = load_meta()
    meta[module] = {
        "original_name": original,
        "stored_name": stored_name,
        "saved_at": datetime.now().isoformat(timespec="seconds"),
        "size": os.path.getsize(path),
    }
    save_meta(meta)

    return jsonify({"ok": True, "module": module, "filename": original})


@app.route("/api/load/<module>")
def api_load(module):
    """Baixa o último Excel salvo do módulo."""
    if module not in ALLOWED_MODULES:
        return jsonify({"ok": False, "error": "módulo inválido"}), 400

    meta = load_meta()
    info = meta.get(module)
    if not info:
        return jsonify({"ok": False, "error": "nada salvo"}), 404

    path = os.path.join(DATA, info["stored_name"])
    if not os.path.exists(path):
        return jsonify({"ok": False, "error": "arquivo sumiu"}), 404

    return send_file(
        path,
        as_attachment=False,
        download_name=info.get("original_name") or info["stored_name"],
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@app.route("/api/meta/<module>")
def api_meta(module):
    if module not in ALLOWED_MODULES:
        return jsonify({"ok": False}), 400
    meta = load_meta()
    info = meta.get(module)
    if not info:
        return jsonify({"ok": False, "saved": False})
    path = os.path.join(DATA, info.get("stored_name", ""))
    if not os.path.exists(path):
        return jsonify({"ok": False, "saved": False})
    return jsonify({
        "ok": True,
        "saved": True,
        "filename": info.get("original_name"),
        "saved_at": info.get("saved_at"),
        "size": info.get("size"),
    })


@app.route("/api/clear/<module>", methods=["POST", "DELETE"])
def api_clear(module):
    if module not in ALLOWED_MODULES:
        return jsonify({"ok": False}), 400
    meta = load_meta()
    info = meta.pop(module, None)
    save_meta(meta)
    if info:
        path = os.path.join(DATA, info.get("stored_name", ""))
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
    return jsonify({"ok": True})


if __name__ == "__main__":
    print("\\n  ╔══════════════════════════════════════════╗")
    print("  ║   NEXUS PLATFORM  •  Futuristic Suite    ║")
    print("  ║   http://127.0.0.1:5000                  ║")
    print("  ║   Memória de arquivos: pasta data/       ║")
    print("  ╚══════════════════════════════════════════╝\\n")
    # 0.0.0.0 = acessível no celular (mesma rede)
    app.run(host="0.0.0.0", port=5000, debug=False)
