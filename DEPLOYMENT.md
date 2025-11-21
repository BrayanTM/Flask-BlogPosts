# Notas de Despliegue en Vercel

## ⚠️ Cambios Importantes para Producción

### 1. Configuración de Locale

El código actual en `blogapp/__init__.py` intenta configurar el locale español:

```python
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
```

**Problema**: Vercel no tiene este locale instalado por defecto.

**Solución recomendada**: Modificar para manejar el error:

```python
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    # Usar locale por defecto si el español no está disponible
    pass
```

### 2. Base de Datos PostgreSQL

**En desarrollo**: Docker con PostgreSQL local
**En producción**: Necesitas un servicio de PostgreSQL en la nube

#### Opciones recomendadas:

1. **Neon** (Recomendado - Gratis)
   - URL: https://neon.tech
   - Serverless PostgreSQL
   - Tier gratuito generoso
   - URL de ejemplo: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb`

2. **Supabase** (Gratis con límites)
   - URL: https://supabase.com
   - Incluye más servicios
   - URL de ejemplo: `postgresql://postgres:pass@db.xxx.supabase.co:5432/postgres`

3. **Railway** ($5/mes)
   - URL: https://railway.app
   - Fácil integración
   - URL de ejemplo: `postgresql://postgres:pass@containers-xxx.railway.app:5432/railway`

### 3. Variables de Entorno en Vercel

Configurar en: Dashboard > Settings > Environment Variables

```env
# Flask
SECRET_KEY=<genera-con-secrets.token_hex(32)>
DEBUG=False
FLASK_APP=main.py

# Base de datos (ejemplo con Neon)
DATABASE_URL=postgresql://user:password@host.region.aws.neon.tech/dbname

# PostgreSQL directo (no necesario en Vercel)
# POSTGRES_USER=
# POSTGRES_PASSWORD=
# POSTGRES_DB=
# PORT_DB=

# Cloudinary
CLOUDINARY_URL=cloudinary://123456789012345:abcdefghijklmnopqrstuvwxyz@cloud-name

# Security
CRYPT_METHOD=pbkdf2:sha256
```

### 4. Migraciones en Producción

**Importante**: Debes ejecutar las migraciones en tu base de datos de producción.

#### Opción 1: Desde local (recomendado)

```bash
# 1. Configurar DATABASE_URL de producción en .env.local
DATABASE_URL=postgresql://user:pass@production-host/db

# 2. Ejecutar migraciones
flask db upgrade
```

#### Opción 2: Script de inicialización

Crear `init_db.py`:

```python
from blogapp import create_app
from blogapp.db_con import db

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tablas creadas exitosamente")
```

Ejecutar una vez después del primer despliegue.

### 5. Archivos Estáticos

Los archivos en `blogapp/static/` se servirán automáticamente. Vercel los optimiza.

### 6. Verificación Post-Despliegue

Checklist después de desplegar:

- [ ] Aplicación accesible en la URL de Vercel
- [ ] Página principal carga correctamente
- [ ] CSS y JavaScript funcionan
- [ ] Registro de usuario funciona
- [ ] Login funciona
- [ ] Crear post funciona
- [ ] Subir imagen de avatar funciona (Cloudinary)
- [ ] Búsqueda funciona
- [ ] No hay errores 500 en los logs

### 7. Monitoreo y Logs

Ver logs en tiempo real:

```bash
vercel logs <url-de-tu-proyecto>
```

O desde el dashboard: Deployments > Ver logs

### 8. Dominios Personalizados

Vercel proporciona un dominio: `tu-proyecto.vercel.app`

Para dominio personalizado:
1. Settings > Domains
2. Agregar tu dominio
3. Configurar DNS según las instrucciones

### 9. Límites del Plan Gratuito de Vercel

- **Serverless Function Execution**: 100 GB-Hrs/mes
- **Bandwidth**: 100 GB/mes
- **Builds**: 6000 minutos/mes
- **Función máxima duration**: 10 segundos

Para aplicaciones con tráfico bajo-medio, el plan gratuito es suficiente.

### 10. Alternativas a Vercel

Si encuentras limitaciones:

- **Railway**: Ideal para Flask + PostgreSQL, $5/mes
- **Render**: Similar a Heroku, plan gratuito disponible
- **Fly.io**: Serverless containers, plan gratuito limitado
- **PythonAnywhere**: Específico para Python, plan gratuito básico

## 🔧 Cambios Requeridos en el Código

### Modificar `blogapp/__init__.py`

```python
# Antes
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Después
try:
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except (locale.Error, ValueError):
    # Locale español no disponible, usar el predeterminado
    print("⚠️ Warning: Spanish locale not available, using default")
    pass
```

### Opcional: Crear archivo `runtime.txt`

Si quieres especificar la versión de Python:

```txt
python-3.11
```

## 📝 Comandos Útiles

```bash
# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Desplegar en preview
vercel

# Desplegar en producción
vercel --prod

# Ver logs
vercel logs

# Ver variables de entorno
vercel env ls

# Agregar variable de entorno
vercel env add SECRET_KEY

# Pull variables de entorno localmente
vercel env pull .env.local
```

## ✅ Checklist Final

Antes de hacer el despliegue final:

- [ ] `vercel.json` creado
- [ ] `requirements.txt` creado con `psycopg2-binary`
- [ ] `.vercelignore` creado
- [ ] `main.py` modificado (exporta `app` a nivel de módulo)
- [ ] Variables de entorno configuradas en Vercel
- [ ] Base de datos PostgreSQL en la nube creada
- [ ] Cuenta de Cloudinary activa
- [ ] `DEBUG=False` en producción
- [ ] `SECRET_KEY` generada de forma segura
- [ ] Migraciones ejecutadas en la base de datos de producción
- [ ] Código con manejo de errores de locale

## 🎉 ¡Listo para Desplegar!

Una vez completado todo, ejecuta:

```bash
git add .
git commit -m "Configure project for Vercel deployment"
git push origin main
```

Si tu proyecto está conectado a Vercel, se desplegará automáticamente.
