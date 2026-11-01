# Acceso a Datos · RA3 · ORM ITC

Unidad 3, herramientas de mapeo objeto relacional. Continúa clientes y proyectos
de RA2, con SQLAlchemy y una ventana sencilla de gestión.

Instalar: `python -m pip install -r requirements.txt`.
Desde `02-proyecto-unidad`, ejecutar `python app.py` y probar con
`python -m unittest -v`.

Para abrir la base creada por C++: `python app.py --base RUTA_A_LA_SQLITE_RA2`.
Se recomienda trabajar sobre una copia local de la SQLite de RA2. El mapeo
conserva nombres, claves y relaciones; no sustituye las tablas existentes.
La ventana da de alta cliente y proyecto en una sola transacción y consulta
objetos relacionados. La prueba demuestra actualización y rollback por email
duplicado. `resumen_sql` ejecuta SQL explícito.

Es un prototipo académico para ITC con datos ficticios, sin conexión a producción.
Una integración empresarial requeriría revisar permisos y migraciones.

## Uso de IA

Se ha utilizado asistencia de IA para implementar y revisar esta práctica.
Antes de entregarla, el alumno debe ejecutar las pruebas y comprender los
mapeos, las sesiones y las transacciones; esa revisión sigue pendiente.
