from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = '12345'

# Define los detalles del servidor MySQL, incluyendo host, usuario, contraseña y base de datos a utilizar.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'gestion_proyectos'

mysql = MySQL(app)

# Proyectos
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Proyectos")
    if result_value > 0:
        proyectos = cur.fetchall()
        return render_template('index.html', proyectos=proyectos)
    return render_template('index.html')
# Agregar Proyecto: Navega a la página de proyectos y haz clic en "Agregar Proyecto"
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        project_details = request.form
        nombre = project_details['nombre']
        descripcion = project_details['descripcion']
        fecha_inicio = project_details['fecha_inicio']
        fecha_fin = project_details['fecha_fin']

        # Validación en el lado del servidor
        if datetime.strptime(fecha_fin, '%Y-%m-%d') < datetime.strptime(fecha_inicio, '%Y-%m-%d'):
            flash('La fecha de fin no puede ser menor que la fecha de inicio.', 'danger')
            return redirect(url_for('add_project'))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Proyectos(nombre, descripcion, fecha_inicio, fecha_fin) VALUES(%s, %s, %s, %s)", 
                    (nombre, descripcion, fecha_inicio, fecha_fin))
        mysql.connection.commit()
        cur.close()
        flash('Proyecto Agregado Satisfactoriamente', 'success')
        return redirect(url_for('index'))
    return render_template('add_project.html')
#Editar Proyecto: Haz clic en "Editar" junto a un proyecto para modificar sus detalles.
@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Proyectos WHERE id = %s", [id])
    proyecto = cur.fetchone()

    if request.method == 'POST':
        project_details = request.form
        nombre = project_details['nombre']
        descripcion = project_details['descripcion']
        fecha_inicio = project_details['fecha_inicio']
        fecha_fin = project_details['fecha_fin']

        # Validación en el lado del servidor
        if datetime.strptime(fecha_fin, '%Y-%m-%d') < datetime.strptime(fecha_inicio, '%Y-%m-%d'):
            flash('La fecha de fin no puede ser menor que la fecha de inicio.', 'danger')
            return redirect(url_for('edit_project', id=id))

        cur.execute("""
            UPDATE Proyectos
            SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s
            WHERE id = %s
        """, (nombre, descripcion, fecha_inicio, fecha_fin, id))
        mysql.connection.commit()
        cur.close()
        flash('Proyecto Actualizado Satisfactoriamente', 'success')
        return redirect(url_for('index'))

    return render_template('edit_project.html', proyecto=proyecto)
#Eliminar Proyecto: Haz clic en "Eliminar" junto a un proyecto. Si el proyecto tiene asignaciones, verás una alerta indicando que no se puede eliminar.
@app.route('/delete_project/<int:id>', methods=['POST'])
def delete_project(id):
    cur = mysql.connection.cursor()
    # Verificar si el proyecto tiene asignaciones
    cur.execute("SELECT * FROM Asignaciones WHERE proyecto_id = %s", [id])
    asignacion = cur.fetchone()
    if asignacion:
        flash('No se puede eliminar el proyecto porque tiene asignaciones.', 'danger')
    else:
        cur.execute("DELETE FROM Proyectos WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Proyecto Eliminado Satisfactoriamente', 'success')
    cur.close()
    return redirect(url_for('index'))

# Empleados
@app.route('/empleados')
def empleados():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM Empleados")
    if result_value > 0:
        empleados = cur.fetchall()
        return render_template('empleados.html', empleados=empleados)
    return render_template('empleados.html')
#Agregar Empleado: Navega a la página de empleados y haz clic en "Agregar Empleado".
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        employee_details = request.form
        nombre = employee_details['nombre']
        email = employee_details['email']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Empleados(nombre, email) VALUES(%s, %s)", 
                    (nombre, email))
        mysql.connection.commit()
        cur.close()
        flash('Empleado Agregado Satisfactoriamente', 'success')
        return redirect(url_for('empleados'))
    return render_template('add_employee.html')
#Editar Empleado: Haz clic en "Editar" junto a un empleado para modificar sus detalles.
@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Empleados WHERE id = %s", [id])
    empleado = cur.fetchone()

    if request.method == 'POST':
        employee_details = request.form
        nombre = employee_details['nombre']
        email = employee_details['email']

        cur.execute("""
            UPDATE Empleados
            SET nombre = %s, email = %s
            WHERE id = %s
        """, (nombre, email, id))
        mysql.connection.commit()
        cur.close()
        flash('Empleado Actualizado Satisfactoriamente', 'success')
        return redirect(url_for('empleados'))

    return render_template('edit_employee.html', empleado=empleado)
#Eliminar Empleado: Haz clic en "Eliminar" junto a un empleado. Si el empleado está asignado a un proyecto, verás una alerta indicando que no se puede eliminar.
@app.route('/delete_employee/<int:id>', methods=['POST'])
def delete_employee(id):
    cur = mysql.connection.cursor()
    # Verificar si el empleado tiene asignaciones
    cur.execute("SELECT * FROM Asignaciones WHERE empleado_id = %s", [id])
    asignacion = cur.fetchone()
    if asignacion:
        flash('No se puede eliminar el empleado porque está asignado a un proyecto.', 'danger')
    else:
        cur.execute("DELETE FROM Empleados WHERE id = %s", [id])
        mysql.connection.commit()
        flash('Empleado Eliminado Satisfactoriamente', 'success')
    cur.close()
    return redirect(url_for('empleados'))

# Asignaciones
@app.route('/asignaciones')
def asignaciones():
    cur = mysql.connection.cursor()
    result_value = cur.execute("SELECT A.id, P.nombre as proyecto, E.nombre as empleado, A.fecha_asignacion FROM Asignaciones A JOIN Proyectos P ON A.proyecto_id = P.id JOIN Empleados E ON A.empleado_id = E.id")
    if result_value > 0:
        asignaciones = cur.fetchall()
        return render_template('asignaciones.html', asignaciones=asignaciones)
    return render_template('asignaciones.html')
#Agregar Asignación: Navega a la página de asignaciones y haz clic en "Agregar Asignación".
@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM Proyectos")
    proyectos = cur.fetchall()
    cur.execute("SELECT id, nombre FROM Empleados")
    empleados = cur.fetchall()

    if request.method == 'POST':
        assignment_details = request.form
        proyecto_id = assignment_details['proyecto_id']
        empleado_id = assignment_details['empleado_id']
        fecha_asignacion = assignment_details['fecha_asignacion']

        cur.execute("INSERT INTO Asignaciones(proyecto_id, empleado_id, fecha_asignacion) VALUES(%s, %s, %s)", 
                    (proyecto_id, empleado_id, fecha_asignacion))
        mysql.connection.commit()
        cur.close()
        flash('Asignación Agregada Satisfactoriamente', 'success')
        return redirect(url_for('asignaciones'))

    return render_template('add_assignment.html', proyectos=proyectos, empleados=empleados)
#Editar Asignación: Haz clic en "Editar" junto a una asignación para modificar sus detalles.
@app.route('/edit_assignment/<int:id>', methods=['GET', 'POST'])
def edit_assignment(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Asignaciones WHERE id = %s", [id])
    asignacion = cur.fetchone()

    cur.execute("SELECT id, nombre FROM Proyectos")
    proyectos = cur.fetchall()

    cur.execute("SELECT id, nombre FROM Empleados")
    empleados = cur.fetchall()

    if request.method == 'POST':
        assignment_details = request.form
        proyecto_id = assignment_details['proyecto_id']
        empleado_id = assignment_details['empleado_id']
        fecha_asignacion = assignment_details['fecha_asignacion']

        cur.execute("""
            UPDATE Asignaciones
            SET proyecto_id = %s, empleado_id = %s, fecha_asignacion = %s
            WHERE id = %s
        """, (proyecto_id, empleado_id, fecha_asignacion, id))
        mysql.connection.commit()
        cur.close()
        flash('Asignación Actualizada Satisfactoriamente', 'success')
        return redirect(url_for('asignaciones'))

    return render_template('edit_assignment.html', asignacion=asignacion, proyectos=proyectos, empleados=empleados)
#Eliminar Asignación: Haz clic en "Eliminar" junto a una asignación para eliminarla.
@app.route('/delete_assignment/<int:id>', methods=['POST'])
def delete_assignment(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Asignaciones WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()
    flash('Asignación Eliminada Satisfactoriamente', 'success')
    return redirect(url_for('asignaciones'))
#Correr el proyecto
if __name__ == '__main__':
    app.run(debug=True)
