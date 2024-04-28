import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Path a tu archivo JSON de configuración
cred_path = 'serviceAccountKey.json'
cred = credentials.Certificate(cred_path)

# Inicializar la aplicación de Firebase
firebase_app = firebase_admin.initialize_app(cred)

# Obtener la referencia a la base de datos
db = firestore.client()
