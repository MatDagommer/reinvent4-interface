from flask import Flask, request, jsonify, send_file, render_template
import toml
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')  # Assure-toi que le nom du fichier correspond

@app.route('/generate-toml', methods=['POST'])
def generate_toml():
    # Récupérer les données envoyées par le formulaire
    data = request.json
    option1 = data.get('option1')
    option2 = data.get('option2')

    # Créer la structure TOML
    config = {
        'settings': {
            'option1': option1,
            'option2': option2
        }
    }

    # Générer le fichier TOML
    toml_string = toml.dumps(config)
    
    # Sauvegarder dans un fichier temporaire
    file_obj = io.BytesIO(toml_string.encode('utf-8'))
    file_obj.seek(0)

    # Envoyer le fichier TOML au client
    return send_file(file_obj, as_attachment=True, download_name='config.toml', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
