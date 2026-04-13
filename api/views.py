from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from turnos.firebase_config import initialize_firebase
from datetime import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

db = initialize_firebase()

# Función mejorada para limpiar espacios y mayúsculas
def obtener_rol_usuario(user):
    user_id = getattr(user, 'uid', 'anonimo')
    perfil_doc = db.collection('perfiles').document(user_id).get()
    
    if perfil_doc.exists:
        # .strip() quita espacios accidentales y .lower() ignora Mayúsculas
        rol_valor = str(perfil_doc.to_dict().get('rol', 'usuario_base')).strip().lower()
        return rol_valor, user_id
    
    return 'usuario_base', user_id

class TicketListCreateAPIView(APIView):
    def get(self, request):
        try:
            rol, user_id = obtener_rol_usuario(request.user)
            query = db.collection('tickets')
            
            # Filtro: Si no es tecnico, solo ve lo suyo
            if rol != 'tecnico':
                query = query.where('usuario_id', '==', user_id)
            
            docs = query.get()
            tickets = []
            for doc in docs:
                data = doc.to_dict()
                if 'fecha_creacion' in data:
                    data['fecha_creacion'] = str(data['fecha_creacion'])
                tickets.append({**data, 'id': doc.id})
                
            return Response(tickets, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def post(self, request):
        try:
            data = request.data
            user_id = getattr(request.user, 'uid', 'anonimo')
            new_ticket = {
                'titulo': data.get('titulo'),
                'descripcion': data.get('descripcion'),
                'numero_equipo': data.get('numero_equipo'),
                'estado': 'Pendiente',
                'usuario_id': user_id,
                'fecha_creacion': datetime.now()
            }
            doc_ref = db.collection('tickets').add(new_ticket)
            new_ticket['fecha_creacion'] = str(new_ticket['fecha_creacion'])
            return Response({'id': doc_ref[1].id, **new_ticket}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class TicketDetailUpdateAPIView(APIView):
    def put(self, request, ticket_id):
        try:
            rol, _ = obtener_rol_usuario(request.user)

            # Verificación de rol (Ahora más segura con .lower())
            if rol != 'tecnico':
                return Response({'error': f'Acceso Denegado. Tu rol es: {rol}. Solo técnicos.'}, status=403)

            # Normalizamos el estado para que acepte "resuelto" o "Resuelto"
            estado_input = str(request.data.get('estado', '')).strip()
            
            # Buscamos coincidencias sin importar mayúsculas
            opciones = ['Pendiente', 'En Revisión', 'Resuelto']
            nuevo_estado = next((opt for opt in opciones if opt.lower() == estado_input.lower()), None)

            if not nuevo_estado:
                return Response({'error': f'Estado no válido. Use: {opciones}'}, status=400)

            doc_ref = db.collection('tickets').document(ticket_id)
            doc_ref.update({'estado': nuevo_estado})

            # WebSocket
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'alertas_group',
                {
                    'type': 'enviar_alerta',
                    'mensaje': f"Ticket #{ticket_id} actualizado a {nuevo_estado}"
                }
            )
            return Response({'mensaje': f'Estado actualizado a {nuevo_estado} y alerta enviada'})
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class EstadisticasAPIView(APIView):
    def get(self, request):
        try:
            docs = db.collection('tickets').get()
            total, pendientes, resueltos = 0, 0, 0
            
            for doc in docs:
                total += 1
                est = str(doc.to_dict().get('estado', '')).lower()
                if 'pendiente' in est: pendientes += 1
                elif 'resuelto' in est: resueltos += 1

            return Response({
                'total_tickets': total,
                'pendientes': pendientes,
                'resueltos': resueltos,
                'otros': total - (pendientes + resueltos)
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)