from flask import Flask, jsonify
import pandas as pd

# Initialiser Flask
app = Flask(__name__)

# Charger les données CSV au démarrage
try:
    df = pd.read_csv("data.csv")
except FileNotFoundError:
    df = pd.DataFrame()  # CSV non trouvé → DataFrame vide

# Endpoint : récupérer toutes les données
@app.route("/data", methods=["GET"])
def get_all_data():
    return jsonify(df.to_dict(orient="records"))

# Endpoint : récupérer une ligne par ID
@app.route("/data/<int:item_id>", methods=["GET"])
def get_item(item_id):
    if "id" not in df.columns:
        return jsonify({"error": "La colonne 'id' n'existe pas dans data.csv"}), 400

    item = df[df["id"] == item_id]

    if item.empty:
        return jsonify({"error": "ID introuvable"}), 404

    return jsonify(item.to_dict(orient="records")[0])

# Lancer le serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
