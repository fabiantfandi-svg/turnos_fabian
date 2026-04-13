# 🗳️ Sistema de Gestión de Tickets - API Votación Online

Este proyecto es una API REST profesional desarrollada con **Django** y **Django Rest Framework**, diseñada para la gestión de tickets técnicos. Integra **Firebase Firestore** para el almacenamiento de datos en la nube y **Django Channels** para notificaciones en tiempo real mediante WebSockets.

## 🚀 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.10** o superior.
- **Git** para el control de versiones.
- Una cuenta de **Firebase** con un proyecto activo y el archivo de credenciales.

---

## 🛠️ Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto en tu máquina local:

### 1. Clonar el repositorio

```bash
git clone <https://github.com/fabiantfandi-svg/turnos_fabian>
cd crisss
```

### 2. Configurar el Entorno Virtual

Es fundamental usar un entorno virtual para mantener las dependencias aisladas.

**En Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar Dependencias

Una vez activado el entorno virtual, instala todas las librerías necesarias:

```bash
pip install -r requirements.txt
```

### 4. Credenciales de Firebase

Asegúrate de que el archivo `serviceAccountKey.json` (descargado desde la consola de Firebase) esté ubicado en la raíz del proyecto para que la configuración en `firebase_config.py` pueda inicializar el SDK correctamente.

### 5. Aplicar Migraciones

Django requiere preparar la base de datos interna para el manejo de sesiones y autenticación:

```bash
python manage.py migrate
```

---

## 🏃 Ejecución del Proyecto

Para iniciar el servidor de desarrollo con soporte para WebSockets (Daphne):

```bash
python manage.py runserver
```

El servidor estará escuchando en:  
http://127.0.0.1:8000/

---

## 📄 Documentación de la API (Swagger)

La API cuenta con documentación interactiva autogenerada para facilitar las pruebas de los endpoints:

- Swagger UI (Visual): http://127.0.0.1:8000/api/docs/
- Esquema OpenAPI (JSON/YAML): http://127.0.0.1:8000/api/schema/

---

## 📡 Endpoints Principales

| Método | Endpoint | Descripción |
|--------|---------|------------|
| GET | /api/tickets/ | Lista tickets (Filtra por usuario si no es técnico). |
| POST | /api/tickets/ | Crea un nuevo ticket de soporte. |
| PUT | /api/tickets/<id>/ | Actualizar estado (Solo permitido para el rol técnico). |
| GET | /api/tickets/estadisticas/ | Devuelve métricas globales de los tickets. |

---

## 🔔 Notificaciones en Tiempo Real (WebSockets)

El sistema emite una alerta global cada vez que se actualiza el estado de un ticket.

Para realizar pruebas de conexión (usando Postman o un cliente WebSocket):

- URL de conexión:  
ws://127.0.0.1:8000/ws/alertas/

---

## 👥 Colaboradores

- Fabian Torres - Aprendiz ADSO 
