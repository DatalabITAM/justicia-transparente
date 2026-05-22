# Justicia Transparente

[**English**](#english) | [**Español**](#español)

---

## English

### Project Overview
**Justicia Transparente** is a project by **Datalab ITAM**, an interdisciplinary group of students from the **Instituto Tecnológico Autónomo de México (ITAM)**. This initiative promotes access to justice through transparency and the structured analysis of public court rulings. 

This repository maintains a centralized database designed to extract, organize, and analyze rulings published by the Judiciary across all Mexican States. Our objective is to audit how justice is administered in Mexico and identify data-driven improvements for the national legal system.

### Technical Documentation & Data Acquisition
The data collection lifecycle is managed via automated web scraping. Implementation details, logic, and source code are documented in the following resource:
* [**Web Scraping Implementation (Jupyter Notebook)**](https://github.com/DatalabITAM/justicia-transparente/blob/gh-pages/webScraping/webScrap.ipynb)

### Repository Assets
* [**GitHub Interactive Page**](https://datalabitam.github.io/justicia-transparente/): Project visualization and frontend.
* [**Main Dataset (CSV)**](https://github.com/DatalabITAM/justicia-transparente/blob/gh-pages/web_poder_judicial_por_estado.csv): Core database containing URLs and judicial metadata.

#### Database Schema
The dataset is structured according to the **State Geostatistical Areas (AGEE)** index by INEGI.

| Column Name | Description | Data Type |
| :--- | :--- | :--- |
| **Clave de AGEE** | Unique numeric identifier for the state (INEGI). | Integer |
| **Nombre de AGEE** | Official name of the Mexican State. | String |
| **Website** | Official State Government URL. | URL |
| **Website del Poder Judicial** | Specific Judiciary portal URL for scraping. | URL |
| **Población** | State population context. | Integer |
| **Última actualización** | Timestamp of the last verified record update. | Date (YYYY-MM-DD) |

### Collaborative Maintenance & Version Control
To maintain data integrity, all contributors must follow these protocols when identifying inconsistencies or outdated records:
1. Submit a **Pull Request (PR)** titled: `Solicitación para actualizar información`.
2. Ensure the `Última actualización` column is updated to the current date for all modified rows.
3. Provide a technical description of the changes in the PR comments.

### Team & Credits
* **Project Lead & Admin:** [Leslie Brenes](mailto:leslie.brenes@itam.mx)
* **Lead Scraping Contributor:** Federico Domínguez
* **Conceptual Design:** Valentina Mancera
* **Data Research:** [Emilio Camargo Espinosa](mailto:emilio.camargo@itam.mx)
* **Technical Contributors:** [David Veloz](mailto:david.velozs@outlook.com), [Arturo Lier](mailto:lierarturo@gmail.com), [Fernando Gómez](mailto:fernadogomez210398@gmail.com), [Ricardo](mailto:ricardobenacres@gmail.com), [Victor Amaya](mailto:amayalvictor@hotmail.com), Yosshua Cisneros, svillarreal98, and Raquel.

### License & Ownership
Property of **ITAM**. Free for public and academic use, provided credit is attributed to **DataLab ITAM - Justicia Transparente Team**.

---

## Español

### Descripción del Proyecto
**Justicia Transparente** es un proyecto del **Datalab ITAM**, un grupo interdisciplinario conformado por estudiantes del **Instituto Tecnológico Autónomo de México (ITAM)**. Buscamos fomentar el acceso a la justicia a través de la transparencia y el análisis de sentencias públicas. 

A través de esta base de datos, pretendemos extraer, organizar y analizar las sentencias publicadas por los Poderes Judiciales de cada Estado de la República para entender cómo se juzga en México y qué se tiene que mejorar para crear un país más justo.

### Documentación Técnica y Adquisición de Datos
El proceso de recopilación de datos se realiza mediante web scraping. Puedes consultar los detalles de la arquitectura, lógica e implementación en el siguiente archivo:
* [**Documentación de Web Scraping (Jupyter Notebook)**](https://github.com/DatalabITAM/justicia-transparente/blob/gh-pages/webScraping/webScrap.ipynb)

### Recursos del Repositorio
* [**GitHub Page**](https://datalabitam.github.io/justicia-transparente/): Interfaz interactiva del proyecto.
* [**Base de Datos (CSV)**](https://github.com/DatalabITAM/justicia-transparente/blob/gh-pages/web_poder_judicial_por_estado.csv): Archivo `web_poder_judicial_por_estado.csv` con los registros maestros.

#### Estructura de la Base de Datos (Schema)
Esta base de datos sigue el índice de **Áreas Geoestadísticas Estatal (AGEE)** del INEGI.

| Nombre de Columna | Descripción | Tipo de Dato |
| :--- | :--- | :--- |
| **Clave de AGEE** | Identificador numérico único del estado (INEGI). | Entero |
| **Nombre de AGEE** | Nombre oficial de la entidad federativa. | Texto |
| **Website** | URL oficial del Gobierno del Estado. | URL |
| **Website del Poder Judicial** | URL del portal judicial para la extracción de datos. | URL |
| **Población** | Contexto demográfico del estado. | Entero |
| **Última actualización** | Fecha de la última verificación o cambio en el registro. | Fecha (AAAA-MM-DD) |

### Gestión de Colaboración y Control de Versiones
Para garantizar la persistencia y veracidad de la información a través del tiempo, cualquier modificación debe seguir este flujo:
1. Solicitar un **Pull Request (PR)**.
2. El PR debe contar obligatoriamente con la fecha actualizada en la columna `Última actualización`. 
3. El título debe ser: `Solicitación para actualizar información`, incluyendo una descripción técnica de los cambios.

### Equipo y Créditos
* **Líder de Proyecto y Admin:** [Leslie Brenes](mailto:leslie.brenes@itam.mx)
* **Contribuidor Principal (Scraping):** Federico Domínguez
* **Diseño Conceptual:** Valentina Mancera
* **Investigación de Datos:** [Emilio Camargo Espinosa](mailto:emilio.camargo@itam.mx)
* **Colaboradores Técnicos:** [David Veloz](mailto:david.velozs@outlook.com), [Arturo Lier](mailto:lierarturo@gmail.com), [Fernando Gómez](mailto:fernadogomez210398@gmail.com), [Ricardo](mailto:ricardobenacres@gmail.com), [Victor Amaya](mailto:amayalvictor@hotmail.com), Yosshua Cisneros, svillarreal98 y Raquel.

### Licencia y Propiedad
Este proyecto es propiedad del **ITAM**. Su uso es libre siempre y cuando se otorguen los créditos correspondientes al **DataLab ITAM - Equipo de Justicia Transparente**.
