import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth, firestore
from turnos.firebase_config import initialize_firebase

db = initialize_firebase()


class RegistroAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        rol = request.data.get('rol')

        if not email or not password or not rol:
            return Response({"error": "Faltan credenciales"}, status=400)

        # Normalizamos el rol
        rol = str(rol).strip().lower()

        if rol not in ['usuario_base', 'tecnico']:
            return Response({"error": "Rol inválido"}, status=400)

        try:
            user = auth.create_user(email=email, password=password)

            db.collection('perfiles').document(user.uid).set({
                'email': email,
                'rol': rol,
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            return Response({
                "mensaje": "Usuario registrado",
                "uid": user.uid,
                "rol": rol
            }, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class LoginApiView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        api_key = os.getenv('FIREBASE_WEB_API_KEY')

        if not email or not password:
            return Response({"error": "Faltan credenciales"}, status=400)

        if not api_key:
            return Response({"error": "Falta FIREBASE_WEB_API_KEY en el entorno"}, status=500)

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if response.status_code == 200:
                return Response({
                    "mensaje": "Login exitoso",
                    "token": data['idToken'],
                    "uid": data['localId']
                }, status=200)

            error_msg = data.get('error', {}).get('message', 'Error desconocido')
            return Response({"error": error_msg}, status=401)

        except Exception as e:
            return Response({"error": str(e)}, status=500)