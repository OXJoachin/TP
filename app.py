from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

taches = []
prochain_id = 1


@app.route("/")
def accueil():
    """Affiche toutes les tâches."""
    return render_template("index.html", taches=taches)


@app.route("/ajouter", methods=["POST"])
def ajouter():
    """Ajoute une tâche à la liste en mémoire."""
    global prochain_id

    titre = request.form.get("titre", "").strip()
    description = request.form.get("description", "").strip()

    if titre:
        taches.insert(0, {
            "id": prochain_id,
            "titre": titre,
            "description": description,
            "terminee": False
        })
        prochain_id += 1

    return redirect(url_for("accueil"))


@app.route("/tache/<int:tache_id>")
def detail_tache(tache_id):
    """Affiche le détail d'une tâche selon son identifiant."""
    tache = next((t for t in taches if t["id"] == tache_id), None)
    if tache is None:
        return "Tâche introuvable", 404
    return render_template("detail.html", tache=tache)


@app.route("/terminer/<int:tache_id>", methods=["POST"])
def terminer(tache_id):
    """Inverse l'état terminé/en cours."""
    tache = next((t for t in taches if t["id"] == tache_id), None)
    if tache is not None:
        tache["terminee"] = not tache["terminee"]
    return redirect(url_for("accueil"))


@app.route("/supprimer/<int:tache_id>", methods=["POST"])
def supprimer(tache_id):
    """Supprime une tâche de la liste en mémoire."""
    global taches
    taches = [t for t in taches if t["id"] != tache_id]
    return redirect(url_for("accueil"))


if __name__ == "__main__":
    app.run(debug=True)
