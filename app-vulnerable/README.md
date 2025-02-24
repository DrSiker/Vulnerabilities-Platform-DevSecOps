# Aplicación Vulnerable

Esta aplicación contiene vulnerabilidades intencionadas para pruebas de seguridad.

## Vulnerabilidades Intencionadas:
1. **SQL Injection** - No se usa `?` o parámetros seguros en las consultas SQL.
2. **Exposición de Información Sensible** - El endpoint `/debug` revela información del sistema.
