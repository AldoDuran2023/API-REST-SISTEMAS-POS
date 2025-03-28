# API REST - Sistema de Punto de Venta (POS)

## Descripción
Este API REST está destinado a un sistema de punto de venta (POS) con funcionalidades principales como:
- Manejo de los productos ingresantes al almacén.
- Registro de salida de productos.
- Autenticación para las rutas.

El sistema maneja dos roles:
- **Administrador:** Responsable del mantenimiento de los productos.
- **Empleado:** Solo puede realizar ventas.

### Tecnologías utilizadas:
- **Backend:** Python, Flask
- **Base de datos:** MySQL, SQLAlchemy
- **Otros:** CORS, dotenv, mysqlclient

---

## Instalación
### 1. Crear un entorno virtual para Python
```bash
python -m venv venv
```

### 2. Activar el entorno virtual
- En Windows:
```bash
venv\Scripts\activate
```
- En macOS/Linux:
```bash
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
Copiar el archivo `.env.example` como `.env` y modificar los parámetros según la configuración deseada.
```bash
cp .env.example .env
```
Editar el archivo `.env` con los valores correspondientes, como las credenciales de la base de datos.

### 5. Ejecutar el servidor
```bash
python index.py
```

---

## Uso
Puedes realizar peticiones JSON a través de Postman o Thunder Client.

### Registro de usuario
**URL:** `http://127.0.0.1:5000/api/register`

**Ejemplo de solicitud:**
```json
{
  "nombre": "carlitos",
  "email": "carlos@gmail.com",
  "password": "123",
  "rol": "admin"
}
```

### Inicio de sesión
**URL:** `http://127.0.0.1:5000/api/login`

**Ejemplo de solicitud:**
```json
{
  "email": "carlos@gmail.com",
  "password": "123"
}
```

### Obtener listas de entidades
**URL base:** `http://127.0.0.1:5000/api/#name`

Donde `#name` puede ser:
- **marcas:** marca
- **categorías:** categoria
- **productos:** producto
- **proveedores:** proveedor
- **compras:** compra
- **ventas:** venta
- **detalle compras:** detallecompra
- **detalle ventas:** detalleventa

---

## Notas
- Asegúrate de configurar correctamente la base de datos en el archivo `.env`.
- Para pruebas, usa Postman o Thunder Client.
- El sistema requiere autenticación para la mayoría de las rutas.

---

### Autor
Desarrollado por Duran

