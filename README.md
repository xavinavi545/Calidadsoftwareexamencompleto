# Sistema de Gestión de Proyectos

Este es un sistema de gestión de proyectos desarrollado con Flask y MySQL. Permite gestionar proyectos, empleados y asignaciones de una manera sencilla.

## Requisitos

- Python 3.7 o superior
- MySQL
- pip (gestor de paquetes de Python)

## Instalación de Dependencias

Primero, clona el repositorio en tu máquina local:

```bash
git clone https:github.com/xavinavi545/CalidaddesoftwareExamen
```

## Crea y activa un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```
## Instala las dependencias necesarias
pip install flask 
pip install flask-mysqldb

## Configuración de la Base de Datos 
```sql
CREATE DATABASE gestion_proyectos;
USE gestion_proyectos;
CREATE TABLE Proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);

CREATE TABLE Empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE Asignaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    proyecto_id INT NOT NULL,
    empleado_id INT NOT NULL,
    fecha_asignacion DATE NOT NULL,
    FOREIGN KEY (proyecto_id) REFERENCES Proyectos(id),
    FOREIGN KEY (empleado_id) REFERENCES Empleados(id)
);

```
## Configuración de la Aplicación
1. app.config['MYSQL_HOST'] = 'localhost'
2. app.config['MYSQL_USER'] = 'root'
3. app.config['MYSQL_PASSWORD'] = '12345'  # Reemplaza esto con tu contraseña de MySQL
4. app.config['MYSQL_DB'] = 'gestion_proyectos'

## Ejecución de la Aplicación
```bash
flask run
```
## Uso de la Aplicación
1. Gestión de Proyectos
* Agregar Proyecto: Navega a la página de proyectos y haz clic en "Agregar Proyecto". Completa el formulario y asegúrate de que la fecha de fin no sea menor que la fecha de inicio.
* Editar Proyecto: Haz clic en "Editar" junto a un proyecto para modificar sus detalles. La validación de fechas también se aplica aquí.
* Eliminar Proyecto: Haz clic en "Eliminar" junto a un proyecto. Si el proyecto tiene asignaciones, verás una alerta indicando que no se puede eliminar.
2. Gestión de Empleados
* Agregar Empleado: Navega a la página de empleados y haz clic en "Agregar Empleado". Completa el formulario con el nombre y el correo electrónico del empleado.
* Editar Empleado: Haz clic en "Editar" junto a un empleado para modificar sus detalles.
* Eliminar Empleado: Haz clic en "Eliminar" junto a un empleado. Si el empleado está asignado a un proyecto, verás una alerta indicando que no se puede eliminar.
3. Gestión de Asignaciones
* Agregar Asignación: Navega a la página de asignaciones y haz clic en "Agregar Asignación". Selecciona un proyecto, un empleado y la fecha de asignación.
* Editar Asignación: Haz clic en "Editar" junto a una asignación para modificar sus detalles.
* Eliminar Asignación: Haz clic en "Eliminar" junto a una asignación para eliminarla.
