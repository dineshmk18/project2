from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# Configure your Azure Key Vault details
key_vault_url = 'https://kvdinesh007.vault.azure.net/'
secret_name_db_username = 'username'
secret_name_db_password = 'user-password'

# Initialize Azure Key Vault client using client secret credentials
credential = ClientSecretCredential(
    tenant_id='62c65783-e48b-4438-8d2a-50fb84685b6e',
    client_id='03419e06-5829-452e-8059-1d65510e77f0',
    client_secret='3KM8Q~~EUhyil1vCDtnQEzPbbnWi3pk9jrGxxbSB'
)
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

# Function to retrieve secrets from Azure Key Vault
def get_secret(secret_name):
    secret = secret_client.get_secret(secret_name)
    return secret.value

# Configure your MySQL database connection using secrets from Azure Key Vault
username = get_secret(secret_name_db_username)
password = get_secret(secret_name_db_password)


                                                               
db_uri = f'mysql+mysqlconnector://{username}:{password}@db-server:3306/dineshdb'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri


db = SQLAlchemy(app)

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)

# Create the table
with app.app_context():
    db.create_all()



@app.route('/', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # fetch the form data
        userDetails = request.form
        name = userDetails['name']
        age = userDetails['age']
        gender = userDetails['gender']
        symptoms = userDetails['symptoms']

        new_patient = Patient(name=name, age=age, gender=gender, symptoms=symptoms)

        # Add the patient to the database
        with app.app_context():
          db.session.add(new_patient)
          db.session.commit()

        return redirect('/patient_list')
    
    return render_template('patient_form.html')

@app.route('/patient_list', methods=['GET'])
def patient_list():
    patients = Patient.query.all()
    return render_template('patient_list.html', patients=patients)

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)
