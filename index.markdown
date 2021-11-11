---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---
Octubre de 2021

> Debemos acometer una evolución profunda. No queremos un proceso de apertura simulada, sino ejercicios de justicia abierta que ayuden a este país a resolver conflictos. -- Edna Jaime

# ¿Quiénes somos?

Justicia Transparente es un proyecto del DataLab, un grupo interdisciplinario conformado por estudiantes del Instituto Tecnológico Autónomo de México. Buscamos fomentar el acceso a la justicia a través de la transparencia y el análisis de sentencias públicas. A través de esta base de datos, pretendemos extraer, organizar, y analizar las sentencias publicadas por los Poderes Judiciales de cada Estado de la República. El análisis de sentencias nos permitirá dar cuenta de cómo se juzga en México y qué se tiene que mejorar para crear un México más justo. 

# ¿Por qué lo hacemos?

La longitud y el tipo de lenguaje utilizado en las sentencias es un obstáculo para el acceso y análisis del sistema de justicia en México. Creemos que sistematizar las sentencias permitirá que los particulares puedan acceder a las sentencias públicas de una forma más eficiente, y, por lo tanto, más transparente. Por otro lado, extraer datos de las sentencias será una forma de obtener información de estas sin tener que enfrentarse al lenguaje jurídico complejo empleado por los juzgadores. Actualmente, se tiene poca información acerca de las prácticas de cada juzgado de México. Estamos convencidos de que es necesario tener esta información para lograr exigir un México más justo y transparente. 

# Nuestro proceso 

Como primer paso, evaluamos qué estados estaban cumpliendo con su obligación de publicas sus sentencias. Como resultado, optamos por trabajar con las sentencias del estado de Nuevo León, y específicamente, decidimos hacer un análisis de sus sentencias en materia penal. Se comenzó por webscrappear (con Python y librerías) la captura de sentencias e información del sitio web gubernamental. Hemos conseguido recopilar, a través de nuestro web scraping, sentencias del estado de Coahuila y Nuevo León sin ningún tipo de problema. El principal reto es que cada estado tiene una forma diferente de presentar información, lo cual implica que se debe un algoritmo específico por sitio. 

A la par, preparamos las herramientas que serían necesarias para hacer el análisis de las sentencias. De tal forma que, cada integrante del equipo leyó numerosas sentencias para dar cuenta de la información importante que debíamos extraer de cada una. Para complementar esto, también se consultó a abogados y académicos. Una vez terminada esta etapa investigamos qué herramientas de programación serían las óptimas para extraer esta información de forma eficaz.

Actualmente, estamos utilizando el procesamiento de lenguaje natural y el aprendizaje automático para extraer datos de las sentencias en materia penal del estado de Nueo León. Tenemos como objetivo presentar esta información a través de visualizaciones y su interpretación. Buscamos que los usuarios que hagan uso de la información publicada en Justicia Transparente puedan usarla y construir sobre ella.  

***

### Descarga nuestra base de datos aquí:
[bd_sentencias_nuevo_leon.csv](https://github.com/DatalabITAM/justicia-transparente/files/7229974/bd_sentencias_nuevo_leon.csv)

![Cuenta de delitos en materia penal Nuevo León 2016 - 2021](https://user-images.githubusercontent.com/23329703/139119172-2a077e6d-40f1-4714-b848-c1339226086a.png)
![Cuenta de delitos en materia penal (ajustada sin robo ni violencia) Nuevo León 2016 - 2021](https://user-images.githubusercontent.com/23329703/139119185-b1321d03-86c5-4247-9b1c-f2ab31ec990d.png)

<div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%;
 padding-bottom: 48px; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAEuE9bMehc&#x2F;view?embed">
  </iframe>
</div>
<a href="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAEuE9bMehc&#x2F;view?utm_content=DAEuE9bMehc&amp;utm_campaign=designshare&amp;utm_medium=embeds&amp;utm_source=link" target="_blank" rel="noopener">sentencias por estado</a> by Leslie Brenes

[sentencias por estado.pdf](https://github.com/DatalabITAM/justicia-transparente/files/7517862/sentencias.por.estado.pdf)
