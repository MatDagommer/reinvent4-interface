from flask import Flask, request, jsonify, send_file, render_template
import toml
import io
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')  # Assure-toi que le nom du fichier correspond

@app.route('/get_reinvent_path')
def get_reinvent_path():
    # Replace this with the actual path to your REINVENT4 folder
    reinvent_path = os.path.abspath('../REINVENT4')
    return jsonify({'path': reinvent_path})

@app.route('/generate-toml', methods=['POST'])
def generate_toml():
    # Récupérer les données envoyées par le formulaire
    data = request.json
    run_type = data.get('run_type')
    json_config = data.get('json_config')
    current_folder = data.get('current_folder', '~/REINVENT4/exps/')

    # Créer la structure TOML
    config = {
        'run_type': run_type,
        'device': data.get('device', 'cuda:0'),
        'json_config': f"{current_folder}{json_config}",
        'output_csv': f"{current_folder}{data.get('output_file', 'sampling.csv')}",
        'parameters': {
            'model_path': f"priors/{data.get('model_file', 'reinvent.prior')}",
            'number_of_molecules': int(data.get('num_molecules', 1000)),
            'unique_molecules': data.get('unique_molecules', 'Yes') == 'Yes',
            'randomize': data.get('randomize_smiles', 'Yes') == 'Yes'
        }
    }

    # Add Mol2Mol specific options if the generator is Mol2Mol
    if data.get('generator') == 'Mol2Mol':
        config['parameters'].update({
            'sample_strategy': data.get('sample_strategy', 'beamsearch'),
            'temperature': float(data.get('temperature', 1.0)),
            'tensorboard_log_dir': data.get('tensorboard_log_dir', 'tb_logs')
        })

    # Add SMILES file for generators other than Reinvent
    if data.get('generator') != 'Reinvent':
        config['parameters']['smiles_file'] = data.get('smiles_file', '')


    # Générer le fichier TOML
    toml_string = toml.dumps(config)
    
    # Sauvegarder dans un fichier temporaire
    file_obj = io.BytesIO(toml_string.encode('utf-8'))
    file_obj.seek(0)

    # Envoyer le fichier TOML au client
    return send_file(file_obj, as_attachment=True, download_name='config.toml', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
