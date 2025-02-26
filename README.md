Vulnerabilities Platform - DevSecOps

Este repositorio contiene una plataforma para la gestión y análisis de vulnerabilidades en aplicaciones, integrando prácticas de DevSecOps para garantizar la seguridad en el ciclo de vida del desarrollo de software.

Descripción:

El proyecto tiene como objetivo proporcionar una plataforma automatizada para la detección, análisis y gestión de vulnerabilidades en aplicaciones. Utiliza herramientas de integración continua (CI) y entrega continua (CD) para garantizar que la seguridad sea una parte integral del proceso de desarrollo.
Herramientas y Tecnologías

    Lenguajes de programación: Python, JavaScript, TypeScript

    Frameworks: Flask, React

    Herramientas de seguridad:

        OWASP Dependency-Check

        SonarQube

        Snyk

        Trivy

        Gitleaks (para detección de secretos en repositorios)

    CI/CD: GitHub Actions, Jenkins

    Infraestructura como código (IaC): AWS CDK, AWS CloudFormation

    Contenedores: Docker, Kubernetes

    Base de datos: PostgreSQL

 Estructura del Repositorio




🚨 Detección de Vulnerabilidades

El proyecto integra las siguientes herramientas para la detección de vulnerabilidades:

    OWASP Dependency-Check: Escanea las dependencias del proyecto en busca de vulnerabilidades conocidas.

    SonarQube: Realiza análisis estático de código para detectar problemas de seguridad y calidad.

    Snyk: Identifica vulnerabilidades en dependencias y contenedores.

    Trivy: Escanea imágenes de Docker en busca de vulnerabilidades.

    Gitleaks: Detecta secretos y credenciales expuestas en el repositorio.

Configuración del Entorno
Requisitos Previos

    Docker

    AWS CDK

    Html y CSS (para el frontend)

    Python 3.x (para el backend)

    Cuenta en AWS (para despliegue en la nube)

Pasos para Configurar el Proyecto

    Clona el repositorio:
    bash
    Copy

    git clone https://github.com/DrSiker/Vulnerabilities-Platform-DevSecOps.git
    cd Vulnerabilities-Platform-DevSecOps

    Configura las variables de entorno:

        Crea un archivo .env en la raíz del proyecto y agrega las variables necesarias.

    Instala las dependencias:

        Para el backend:
        bash
        Copy

        cd backend
        pip install -r requirements.txt

        Para el frontend:
        bash
        Copy

        cd frontend
        npm install

    Despliega la infraestructura con AWS CDK:
    bash
    Copy

    cd cdk
    cdk bootstrap
    cdk deploy

    Ejecuta el proyecto:

        Backend:
        bash
        Copy

        cd backend
        python app.py

        Frontend:
        bash
        Copy

        cd frontend
        npm start

 Prácticas de Seguridad

    Integración continua de seguridad: Uso de GitHub Actions para ejecutar escaneos de seguridad en cada push.

    Análisis estático de código: Integración con SonarQube para detectar problemas de seguridad.

    Escaneo de dependencias: Uso de OWASP Dependency-Check y Snyk para identificar vulnerabilidades en dependencias.

    Escaneo de contenedores: Uso de Trivy para escanear imágenes de Docker.

    Detección de secretos: Uso de Gitleaks para identificar credenciales expuestas en el repositorio.

Resultados y Reportes

Los resultados de los escaneos de seguridad se generan en formato JSON y HTML. Puedes encontrar los reportes en las siguientes rutas:

    Dependency-Check: reports/dependency-check-report.json

    SonarQube: reports/sonarqube-report.html

    Trivy: reports/trivy-report.json

    Gitleaks: reports/gitleaks-report.json

Contribución

¡Las contribuciones son bienvenidas! Si deseas contribuir al proyecto, sigue estos pasos:

    Haz un fork del repositorio.

    Crea una rama con tu feature o corrección: git checkout -b mi-feature.

    Realiza tus cambios y haz commit: git commit -m "Añade mi feature".

    Haz push a la rama: git push origin mi-feature.

    Abre un Pull Request.

Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.


Si tienes alguna pregunta o sugerencia, no dudes en contactar al mantenedor del proyecto:

    Nombre: Didier Alexander Rendón Chaverra

    GitHub: DrSiker


¡Gracias por visitar el repositorio! Esperamos que esta plataforma sea útil para mejorar la seguridad de tus aplicaciones. 🚀

Si necesitas más ajustes o detalles adicionales, ¡avísame! 😊
New chat
