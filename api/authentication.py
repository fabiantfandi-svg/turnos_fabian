from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
from turnos.firebase_config import initialize_firebase

# Inicializamos la base de datos de esta app
db = initialize_firebase()

class FirebaseUser:
    def __init__(self, uid, email, rol):
        self.uid = uid
        self.email = email
        self.rol = rol
        self.is_authenticated = True

    def __str__(self):
        return f"{self.email} ({self.rol})"

class FirebaseAuthentication(BaseAuthentication):
    """
    Valida el Token de Firebase y extrae el rol desde la colección 'perfiles' de Firestore.
    """
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION') or request.headers.get('Authorization')
        
        if not auth_header:
            return None 

        partes = auth_header.split()
        if len(partes) != 2 or partes[0].lower() != 'bearer':
            return None
        
        token = partes[1]

        try:
            # 1. Verificar el token con Google
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')

            # 2. Buscar el rol en Firestore (Colección 'perfiles')
            # Si el documento no existe, le asignamos 'usuario_base' por defecto
            user_profile = db.collection('perfiles').document(uid).get()
            
            if user_profile.exists:
                data = user_profile.to_dict()
                # Ajustamos los roles a los del requerimiento del SENA
                rol = data.get('rol', 'usuario_base')
            else:
                rol = 'usuario_base'

            # 3. Retornar el usuario y el token validado
            return (FirebaseUser(uid, email, rol), decoded_token)
        
        except Exception as e:
            raise AuthenticationFailed(f"Token inválido o expirado: {str(e)}")