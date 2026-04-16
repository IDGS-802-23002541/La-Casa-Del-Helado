# 🍦 La Casa del Helado

Proyecto desarrollado durante el **8° Cuatrimestre**, enfocado en la construcción de un sistema integral para la gestión de una heladería, incluyendo punto de venta, administración de inventario, producción y seguridad de acceso.

---

## 📌 Descripción General

**La Casa del Helado** es una aplicación web que permite gestionar las operaciones principales de una heladería, tales como:

* Registro y control de ventas
* Registro de pedidos en línea
* Gestión de usuarios y roles
* Registro de compras por parte de proveedores
* Administración de inventarios y recetas
* Manejo de solicitudes de producción
* Control de producción
* Dashboard financiero
* Seguridad mediante autenticación y verificación en dos pasos


---

## 👩‍💻 Desarrollado por

* Aideé Vanessa Casillas Tapia
* Vannesa Yassmin Rea Muñoz
* Antonio Damián Rodriguez Alarcón
* Raúl Flores Arredondo

---

## 📚 Materias Involucradas

* **Desarrollo Web Profesional**
  *Roberto Cardiel Rodriguez*
  📧 [rcardiel@utleon.edu.mx](mailto:rcardiel@utleon.edu.mx)

* **Seguridad de Aplicaciones**
  *Ismael Perez Mena*
  📧 [iperez@utleon.edu.mx](mailto:iperez@utleon.edu.mx)

* **Administración de Base de Datos**
  *Roberto Eduardo Ruiz Gonzalez*
  📧 [reruiz@utleon.edu.mx](mailto:reruiz@utleon.edu.mx)

---

## ⚙️ Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/IDGS-802-23002541/La-Casa-Del-Helado.git
cd La-Casa-Del-Helado
```

### 2. Crear y activar entorno virtual

```bash
py -m venv .venv
```

Activar entorno:

* En Windows:

```bash
.venv\Scripts\activate
```

* En Mac/Linux:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

Desde la raíz del proyecto:

```bash
py app.py
```

---

## 🔐 Acceso al Sistema

### 👤 Usuarios por rol

* **Administrador**
  Usuario: `vcruz`
  Contraseña: `123`

* **Producción**
  Usuario: `mramirez`
  Contraseña: `123`

* **Mostrador**
  Usuario: `lgonzalez`
  Contraseña: `123`

---

### 🧾 Cliente

* Correo: `aideecasillas@gmail.com`
* Contraseña: `1234`

---

## 🔒 Autenticación en Dos Factores

El sistema implementa verificación en dos pasos:

* El **token de verificación** se imprime en la consola del servidor al momento de iniciar sesión.
* Este token debe ingresarse para completar el acceso al sistema.

---

## 🛠️ Tecnologías Utilizadas

* Python (Flask)
* MySQL
* HTML, CSS, JavaScript
* SQLAlchemy
* Flask-Security
* Flask-Login
* Flask-Migrate

---

## 📌 Notas Adicionales

* Asegúrate de tener configurada correctamente la base de datos antes de ejecutar el sistema.
* El proyecto está orientado a fines académicos.
* El sistema puede requerir variables de entorno dependiendo de la configuración local.

---

## 📄 Licencia

Proyecto académico sin fines de lucro.
