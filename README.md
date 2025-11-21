# Flask-BlogPosts 📝

Una aplicación web completa para gestionar publicaciones de blog desarrollada con Flask, PostgreSQL y Cloudinary.

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Modelos de Base de Datos](#modelos-de-base-de-datos)
- [Rutas y Endpoints](#rutas-y-endpoints)
- [Migraciones](#migraciones)
- [Licencia](#licencia)

## 📖 Descripción

Flask-BlogPosts es una aplicación web moderna para la creación y gestión de blogs. Permite a los usuarios registrarse, crear publicaciones con un editor de texto enriquecido, gestionar perfiles con avatares almacenados en la nube, y buscar contenido dentro del blog.

## ✨ Características

- **Autenticación de usuarios**: Registro, login y logout seguros
- **Gestión de perfiles**: 
  - Actualización de información personal
  - Carga de avatares mediante Cloudinary
  - Cambio de contraseña
- **Gestión de publicaciones**:
  - Creación de posts con editor CKEditor
  - Edición y eliminación de posts propios
  - URLs amigables personalizables
- **Búsqueda**: Sistema de búsqueda por título y contenido
- **Panel de administración**: Vista privada para gestionar posts propios
- **Responsive design**: Interfaz adaptable con Bootstrap

## 🛠 Tecnologías

### Backend
- **Flask 3.1.2**: Framework web principal
- **Flask-SQLAlchemy 3.1.1**: ORM para gestión de base de datos
- **Flask-Migrate 4.1.0**: Gestión de migraciones de base de datos
- **Flask-WTF 1.2.2**: Manejo de formularios y validación
- **Flask-CKEditor 1.0.0**: Editor de texto enriquecido

### Base de Datos
- **PostgreSQL 18**: Base de datos relacional
- **psycopg2 2.9.11**: Adaptador de PostgreSQL para Python

### Almacenamiento en la Nube
- **Cloudinary 1.44.1**: Gestión y almacenamiento de imágenes

### Seguridad
- **Werkzeug**: Hashing de contraseñas con `pbkdf2:sha256`
- **python-dotenv 1.2.1**: Gestión de variables de entorno

### Frontend
- **Bootstrap 5**: Framework CSS
- **CKEditor**: Editor WYSIWYG para contenido

## 📦 Requisitos Previos

- Python 3.14 o superior
- PostgreSQL 18
- Docker y Docker Compose (opcional)
- Cuenta de Cloudinary
- uv (gestor de paquetes) o pip

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/BrayanTM/Flask-BlogPosts.git
cd Flask-BlogPosts
```

### 2. Instalar dependencias

**Usando uv (recomendado):**
```bash
uv sync
```

**Usando pip:**
```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos con Docker

```bash
docker-compose up -d
```

Esto iniciará un contenedor PostgreSQL con la configuración especificada en tu archivo `.env`.

## ⚙️ Configuración

### 1. Crear archivo `.env`

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Flask Configuration
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True

# Database Configuration
DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_db
POSTGRES_USER=usuario
POSTGRES_PASSWORD=password
POSTGRES_DB=nombre_db
PORT_DB=5432

# Cloudinary Configuration
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

# Security
CRYPT_METHOD=pbkdf2:sha256
```

### 2. Inicializar la base de datos

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 🎯 Uso

### Ejecutar la aplicación

**Modo desarrollo:**
```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5000`

### Crear un usuario administrador

1. Accede a `/auth/register`
2. Completa el formulario de registro
3. Inicia sesión en `/auth/login`
4. Accede al panel de administración en `/post/posts`

## 📁 Estructura del Proyecto

```
Flask-BlogPosts/
│
├── blogapp/                    # Paquete principal de la aplicación
│   ├── __init__.py            # Inicialización de la app Flask
│   ├── auth.py                # Blueprint de autenticación
│   ├── home.py                # Blueprint de página principal
│   ├── post.py                # Blueprint de gestión de posts
│   ├── models.py              # Modelos de base de datos
│   ├── db_con.py              # Configuración de SQLAlchemy
│   ├── static/                # Archivos estáticos
│   │   ├── css/               # Hojas de estilo
│   │   ├── js/                # Scripts JavaScript
│   │   └── img/               # Imágenes
│   └── templates/             # Plantillas HTML
│       ├── base.html          # Plantilla base
│       ├── index.html         # Página principal
│       ├── blog.html          # Vista de post individual
│       ├── auth/              # Templates de autenticación
│       └── admin/             # Templates de administración
│
├── migrations/                 # Migraciones de base de datos
├── config.py                  # Configuración de la aplicación
├── main.py                    # Punto de entrada
├── docker-compose.yml         # Configuración de Docker
├── pyproject.toml            # Dependencias del proyecto
└── README.md                  # Este archivo
```

## 🗃 Modelos de Base de Datos

### User (Usuario)
```python
- id: Integer (PK)
- username: String(20) - Único
- email: String(150) - Único
- password: Text - Hash
- avatar: String(256) - Public ID de Cloudinary
- avatar_url: String(256) - URL completa del avatar
- created_at: DateTime
```

### Post (Publicación)
```python
- id: Integer (PK)
- author: Integer (FK -> users.id)
- url: String(100) - URL amigable única
- title: String(100)
- info: Text - Descripción corta
- content: Text - Contenido HTML del editor
- created_at: DateTime
```

## 🛣 Rutas y Endpoints

### Rutas Públicas

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET/POST | `/` | Página principal con listado de posts |
| GET | `/blog/<url>` | Ver post individual |
| GET/POST | `/auth/register` | Registro de usuario |
| GET/POST | `/auth/login` | Inicio de sesión |
| GET | `/auth/logout` | Cerrar sesión |

### Rutas Protegidas (requieren autenticación)

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/post/posts` | Panel de administración - Lista de posts propios |
| GET/POST | `/post/create` | Crear nuevo post |
| GET/POST | `/post/update/<post_id>` | Editar post |
| POST | `/post/delete/<post_id>` | Eliminar post |
| GET/POST | `/auth/profile/<user_id>` | Ver y editar perfil |

## 🔄 Migraciones

### Crear una nueva migración

```bash
flask db migrate -m "Descripción del cambio"
```

### Aplicar migraciones

```bash
flask db upgrade
```

### Revertir migración

```bash
flask db downgrade
```

## 🔒 Seguridad

- Las contraseñas se almacenan hasheadas con `pbkdf2:sha256`
- Protección CSRF en formularios con Flask-WTF
- Rutas protegidas con decorador `@login_required`
- Validación de permisos para edición/eliminación de posts
- Variables sensibles en archivo `.env` (no versionado)

## 🧪 Características Adicionales

- **Localización**: Fechas en español (`es_ES.UTF-8`)
- **Editor rico**: CKEditor con paquete completo
- **Gestión de imágenes**: Integración completa con Cloudinary
- **URLs amigables**: Conversión automática de espacios a guiones
- **Flash messages**: Notificaciones para el usuario
- **Docker**: Contenedor PostgreSQL preconfigurado

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo [LICENSE](LICENSE).

---

**Desarrollado por BrayanTM**