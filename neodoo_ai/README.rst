
========================
🚀 AI-Powered Automation
========================
**Integración IA en el Backend Sin Esfuerzo**

.. |badge1| image:: https://img.shields.io/badge/License-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: Licencia: LGPL-3
.. |badge2| image:: https://img.shields.io/badge/Odoo%20Version-18.0-success.png
    :alt: Compatible con Odoo 18.0
.. |badge3| image:: https://img.shields.io/badge/Usa-Motor%20IA%20Odoo%20(IAP)%20o%20APIs%20gratuitas-blue.png
    :alt: Usa el Motor de IA de Odoo vía IAP o APIs gratuitas
.. |badge4| image:: https://img.shields.io/badge/LLM%20Technical%20Guide-Available-green.png
    :target: LLM_TECHNICAL_GUIDE.md
    :alt: LLM Technical Guide
.. |badge5| image:: https://img.shields.io/badge/Free%20APIs-Hugging%20Face%20integration-orange.png
    :target: docs/ALTERNATIVE_API_GUIDE.md
    :alt: Alternative Free APIs Guide

|badge1| |badge2| |badge3| |badge4| |badge5|


**¡Automatización de Tareas, Respuestas y Generación de Texto en el Backend de Odoo Usando IA!**

Odoo incluye un motor de IA (OLG) para generar texto, pero su uso estándar está limitado a editores de texto enriquecido y al **Website**.

.. raw:: html

   <img src="/neodoo_ai/static/src/img/ai_button.png" 
        alt="AI Odoo on Website" 
        style="border: 2px solid rgb(85, 222, 94); width: 200px; border-radius:10px;">



✅ Este módulo **extiende el poder de la IA nativa de Odoo**, 

permitiéndote usarla fácilmente desde el **backend**, en **cualquier modelo** y lo más importante, 

**automatizar tareas inteligentes**.

**¡NUEVO! Ahora con soporte para APIs gratuitas como Hugging Face, como alternativa al servicio OLG que requiere créditos IAP!**

**Imagina generar automáticamente:**

- Respuestas por email
- Recordatorios
- Resúmenes o borradores
- Análisis y gráficas avanzadas
- Y mucho más, directamente desde tus flujos de trabajo.

Este módulo proporciona una forma **robusta, reutilizable y fácil** de conectar con el motor de IA de Odoo (vía IAP), 

ya sea desde código Python personalizado o **directamente desde Acciones Automatizadas**.


✅ Problema Resuelto
---------------------

La integración con IA desde el backend típicamente requiere:

- Escribir código complejo para realizar llamadas IAP.
- Gestionar autenticación y detalles técnicos del endpoint.
- Implementar manejo de errores robusto (límites, disponibilidad).
- Reutilizar la lógica de manera consistente.

**¡Este módulo elimina toda esa complejidad por ti!**


✨ Beneficios y Características Clave ✨
-----------------------------------------

- **Integración Fácil:** Añade la IA a cualquier modelo con `_inherit = ['tu.modelo', 'ai.generator.mixin']`. ¡Listo!
- **Ahorro de Tiempo Masivo:** Olvida el código repetitivo. Desarrolla funciones con IA en minutos, no en días.
- **Automatización Potente:** Usa la IA en **Acciones Automatizadas** (`base_automation`) para:
  
  - Generar borradores de respuesta a emails.
  
  - Resumir textos largos (tareas, notas).
  
  - Crear contenido inicial (marketing, descripciones).
  
  - Personalizar mensajes (seguimientos, recordatorios).

- **Robusto y Fiable:** Maneja errores comunes del servicio OLG (límites, indisponibilidad) con mensajes claros.
- **Código Limpio (DRY):** Centraliza la lógica de IA. Evita duplicación y asegura consistencia.
- **API Sencilla:** `generate_ai_text(prompt)` para resultados formateados, `_generate_ai_text(prompt)` para la respuesta cruda.
- **¡NUEVO! APIs Gratuitas:** Incluye soporte para Hugging Face y otras APIs gratuitas como alternativa al IAP.
- **Estándar Odoo:** Utiliza la infraestructura IAP y parámetros nativos de Odoo, con opciones alternativas.
- **Máximo Potencial:** Extiende fácilmente la IA de Odoo a cualquier proceso de negocio personalizado.


🚀 ¡Potencia Tus Flujos con Acciones Automatizadas! 🚀
-------------------------------------------------------

Integra la IA al motor de automatización de Odoo sin esfuerzo. 

Dispara acciones inteligentes basadas en eventos (creación, actualización), **sin necesidad de desarrollo complejo** para cada caso.

**Ejemplo: Email de Bienvenida en una Lead del CRM (Origen Website)**

1. Ve a `Ajustes > Técnico > Automatización > Acciones Automatizadas`.
2. Crea una nueva acción:
    - **Modelo:** Prospecto/Oportunidad (`crm.lead`)
    - **Activador:** Al Crear (o Después de la Creación con Retraso)
    - **Aplicar en:** Define tus filtros (ej. Origen específico)
    - **Acción a Realizar:** Ejecutar Código
3. En el bloque de **Código**:

.. code-block:: python

    # Ejemplo: Generar bienvenida para leads generados desde el formulario web de contacto
    for lead in records:
        if lead._context.get("website_id"):
            ai_tool = env['ai.generator.mixin']
            prompt = f"""
            Redacta un email de bienvenida amigable y profesional.
            Lead: {lead.name} | Cliente: {lead.contact_name or 'Cliente'}
            Presenta [Tu Compañía] y sugiere una llamada breve.
            Firma: [Tu Equipo].
            """
            try:
                email_draft = ai_tool.generate_ai_text(prompt)
                if email_draft:
                        # Publica el borrador en el chatter para revisión
                        lead.message_post(
                            body=f"<b>Email Bienvenida Sugerido por IA:</b><br/>{email_draft}"
                        )
            except Exception as e:
                _logger.warning(f"Error generando borrador IA para {lead.id}: {e}")


**¡Las posibilidades son enormes!** Auto-respuestas, resúmenes, borradores, comunicaciones personalizadas... todo automático.


💡 Más Ideas de Casos de Uso 💡
-------------------------------

- **Ventas:** Borradores de seguimiento, resúmenes de notas.
- **Proyectos:** Resúmenes de tareas, borradores de informes.
- **Soporte:** Borradores de respuesta, resúmenes de tickets.
- **Marketing:** Borradores de posts, variaciones de asuntos (A/B).
- **Contabilidad:** Borradores de recordatorios de pago.
- **RRHH:** Borradores de descripciones de puestos.


¿Cómo Funciona? (Simplificado)
-------------------------------

El módulo provee un "Modelo Abstracto" (mixin): `ai.generator.mixin`. 

Al heredarlo, tu modelo Odoo obtiene métodos (`generate_ai_text`, etc.) para usar la IA nativa

(servicio OLG) vía el mecanismo estándar IAP. El mixin gestiona la comunicación y los errores técnicos.


🤓 Para Desarrolladores: Extensibilidad y Claridad
---------------------------------------------------

.. note::
    Diseñado para ser fácil de usar y extender.

- **Extensible:** Hereda `ai.generator.mixin` en cualquier modelo junto a su base: `_inherit = ['tu.modelo', 'ai.generator.mixin']`.
- **Personalizable:** Sobrescribe `generate_ai_text` o `_generate_ai_text` en tu modelo (usando `super()`) para adaptar el pre/post-procesamiento.
- **Código Claro:** La lógica del mixin es directa (llamada IAP, manejo de errores), fácil de entender y adaptar por un desarrollador Odoo con experiencia media.
- **Base Sólida:** Construye funcionalidades AI avanzadas sobre este mixin sin preocuparte por la mecánica API subyacente.


Prerrequisitos
--------------

- **Versión Odoo:** 18.0 (Ajustar si aplica a otras)
- **Dependencias:** Módulo `iap` estándar de Odoo instalado.
- **Servicio IA Odoo:** El servicio IAP para **"Generación de Texto por IA (OLG)"** **activo y configurado por defecto** 

  (Este módulo utiliza esa infraestructura nativa.)

- **Módulo** `base_automation` (Opcional si se quiere agregar Acciones automatizadas).


Inicio Rápido / Uso
--------------------

1. **Instala** este módulo.
2. **Elige el método de uso:**
    - **Método Directo:** ✅ No requiere programación, solo debes invocar al método para generar el texto con IA.
    - **Método Extensión:** 🧑🏻‍💻 Requiere conocimientos de programación, ideal para implementar tu propia lógica y ampliar las funciones a tu gusto.

    **Método Directo:**

    .. code-block:: python

        ai_tool = env['ai.generator.mixin']
        # records puede ser cualquier modelo (crm, sale, invoice, picking, task)
        for record in records:
            prompt = f"Responde a este cliente {record.contact_name} la pregunta {record.description} "
            try:
                summary = ai_tool.generate_ai_text(prompt)
                if summary:
                    record.message_post(body=summary)
                    _logger.info(f"AI respuesta: {summary}")
            except Exception as e:
                _logger.warning(f"Resumen IA falló: {e}")

    **Método Extensión:**


    .. code-block:: python

        from odoo import models

        class TuModelo(models.Model):
            _name = 'tu.modelo.nombre'
            _inherit = ['tu.modelo.nombre', 'ai.generator.mixin']

            def tu_metodo_personalizado(self):
                prompt = "Genera algo basado en " + self.name
                try:
                    ai_response = self.generate_ai_text(prompt)
                except Exception as e:
                    pass

**Ejemplo Método directo, Llamando a la IA desde Acciones Automatizadas / Servidor / Cron, etc.:**

.. code-block:: python

    ai_tool = env['ai.generator.mixin']
    for record in records:
        prompt = "Crea un resumen para: " + record.algun_campo

        try:
            summary = ai_tool.generate_ai_text(prompt)
        except Exception as e:
            _logger.warning(f"Resumen IA falló: {e}")


¡Invierte en Eficiencia - Integra la IA de Odoo sin Fricción!
-------------------------------------------------------------

Deja de reinventar la rueda. Aprovecha la IA nativa de Odoo en tus procesos de forma rápida y fiable.

**Añade este módulo esencial a tu Odoo y desbloquea un nuevo nivel de automatización inteligente.**

Ventas y CRM:
-------------

- Generación de propuestas comerciales personalizadas basadas en productos/servicios seleccionados, historial del cliente y plantillas predefinidas.

- Análisis de Oportunidades: Identificar oportunidades de venta cruzada (cross-selling) o venta adicional (upselling) analizando el historial de compras y el perfil del cliente en el CRM.

- Predicción de Cierre: Estimar la probabilidad de cierre de una oportunidad basándose en la etapa actual, interacciones pasadas y datos históricos de ventas similares.

- Priorización de Leads: Sugerir qué leads contactar primero basándose en su puntuación (scoring), interacciones recientes o encaje con el perfil de cliente ideal.

- Resumen de Interacciones: Generar resúmenes concisos de largas cadenas de correos electrónicos o notas de llamadas con un cliente específico.

- Seguimiento Inteligentes: Redactar correos de seguimiento personalizados que hagan referencia a puntos específicos discutidos previamente o al estado actual de la oportunidad.

Compras y Aprovisionamiento:
----------------------------

- Solicitudes de Cotización (RFQ): para proveedores basados en necesidades de producto detectadas (ej. bajo stock) o requisitos de un proyecto.

- Análisis de Rendimiento de Proveedores: Resumir el rendimiento histórico de un proveedor (tiempos de entrega, conformidad de pedidos) basándose en los datos de órdenes de compra pasadas.

- Comparación de Ofertas: Crear tablas comparativas o resúmenes de las respuestas a RFQs de diferentes proveedores, destacando precios, plazos y condiciones.

- Sugerencia de Puntos de Pedido: Analizar niveles de stock, velocidad de ventas y plazos de entrega para sugerir puntos de pedido óptimos para productos clave.

Gestión de Proyectos:
---------------------

- Generación de Informes de Estado: Crear borradores de informes de progreso del proyecto, resumiendo tareas completadas, horas registradas (partes de horas), hitos alcanzados y próximos pasos, basándose en los datos del módulo de Proyectos.

- Identificación de Riesgos: Analizar tareas retrasadas, presupuesto excedido (conectando con Contabilidad) o comentarios en tareas para señalar posibles riesgos del proyecto.

- Resumen de Rentabilidad: Generar un resumen rápido de la rentabilidad estimada de un proyecto comparando horas registradas y gastos vs presupuesto inicial.

- Sugerencia de Asignación de Recursos: Basado en la carga de trabajo actual (tareas asignadas) y disponibilidad (hojas de presencia/ausencias), sugerir miembros del equipo adecuados para nuevas tareas o proyectos.

- Creación de Actas de Reunión: Partiendo de la agenda del proyecto, generar una plantilla para el acta de reunión, incluyendo puntos clave y asistentes.

Fabricación:
------------

- Redacción de Órdenes de Trabajo (OT): Generar instrucciones detalladas para órdenes de trabajo basadas en la Lista de Materiales (BOM) y la ruta de fabricación definida para un producto.

- Análisis de Eficiencia de Producción: Resumir los tiempos de ciclo o la eficiencia de órdenes de fabricación completadas, comparándolos con los tiempos estándar esperados.

- Alerta de Escasez de Materiales: Identificar posibles faltantes de componentes necesarios para las próximas órdenes de fabricación programadas, cruzando datos con el inventario.

- Generación de Reportes de Calidad: Crear borradores de informes de incidencias de calidad basados en los datos introducidos en los puntos de control o en el módulo de Calidad.

Contabilidad y Finanzas:
------------------------

- Borradores de Recordatorios de Pago Avanzados: Generar recordatorios de pago personalizados según la antigüedad de la deuda, el historial de pagos del cliente y adjuntando las facturas pendientes relevantes.

- Análisis de Flujo de Caja: Crear proyecciones básicas de flujo de caja a corto plazo basadas en facturas de cliente pendientes de cobro y facturas de proveedor pendientes de pago.

- Clasificación de Gastos: Sugerir categorías contables para nuevos gastos o líneas de extracto bancario basándose en transacciones pasadas o reglas predefinidas.

- Resumen de Cuentas por Cobrar/Pagar: Generar informes resumidos del estado de las cuentas por cobrar (antigüedad de saldos por cliente) o por pagar.

- Análisis de Rentabilidad por Producto/Servicio: Resumir la rentabilidad bruta de líneas de negocio, productos o servicios específicos cruzando datos de ventas y costes asociados (si están bien estructurados).

Recursos Humanos (RRHH):
------------------------

- Borradores de Descripciones de Puestos: (Ya presente, pero útil) Crear borradores detallados basados en roles similares o plantillas estándar.

- Redacción de Comunicaciones Internas: Generar borradores para anuncios internos sobre nuevas contrataciones, cambios de política o eventos de la empresa.

- Creación de Planes de Onboarding: Generar listas de tareas o checklists estándar para el proceso de incorporación de nuevos empleados basadas en el puesto.

- Análisis de Clima Laboral (si hay datos): Si se realizan encuestas, podría resumir tendencias o puntos clave del feedback recibido (requiere integración específica).

Marketing:
----------

- Generación de Contenido para Productos/Servicios: Crear descripciones de marketing para nuevos productos o servicios basándose en sus características técnicas o especificaciones.

- Segmentación de Audiencias: Sugerir segmentos de clientes para campañas de email marketing específicas basándose en su historial de compras, sector o interacciones (datos del CRM).

- Análisis de Campañas: Resumir el rendimiento de campañas de marketing (tasas de apertura, clics, conversiones) si los datos están integrados en Odoo.

- Variaciones de Contenido (A/B Testing): Generar múltiples versiones de asuntos de correo, llamadas a la acción (CTAs) o pequeños textos para pruebas A/B.

.. _llm_guide:

==================================================
🧠 Guía Técnica para LLMs e Inteligencia Artificial
==================================================

Esta sección proporciona información clave para LLMs y sistemas de IA que necesiten entender este módulo.

Para información técnica detallada, consulta `LLM_TECHNICAL_GUIDE.md <LLM_TECHNICAL_GUIDE.md>`_ con documentación específica.

Arquitectura del Módulo
----------------------

- **ai.generator.mixin**: Modelo abstracto principal (componente central)
- **Integración IAP**: Utiliza el sistema de compras in-app de Odoo para el servicio AI
- **Servicio OLG**: Comunica con Odoo Language Generation a través de endpoints JSON-RPC

Métodos Principales
-----------------

1. **generate_ai_text(prompt, conversation_history=None)**:
   - Método público para generar texto con IA
   - Gestiona errores y formato del texto resultado
   - Retorna objeto Markup seguro para HTML o None en caso de fallo

2. **_generate_ai_text(prompt, conversation_history=None)**:
   - Método de bajo nivel que maneja comunicación directa con API
   - Gestiona casos de error específicos (límites, prompts largos)
   - Utilizado internamente por generate_ai_text

Patrones de Integración
----------------------

1. **Llamada Directa** (sin herencia):
   ```python
   ai_tool = env['ai.generator.mixin']
   texto_ai = ai_tool.generate_ai_text("Mi prompt")
   ```

2. **Herencia de Modelos**:
   ```python
   class MiModelo(models.Model):
       _name = 'mi.modelo'
       _inherit = ['mi.modelo', 'ai.generator.mixin']
   ```

3. **Acciones Automatizadas**:
   ```python
   # En base.automation
   ai_tool = env['ai.generator.mixin']
   for record in records:
       result = ai_tool.generate_ai_text(f"Prompt para {record.name}")
   ```

Consideraciones Técnicas
----------------------

- **Gestión de Errores**: UserError para errores de API, AccessError para problemas de conexión
- **Caché Simple**: Lista global PROCESSED_RECORDS para evitar procesamiento duplicado
- **Configuración**: Usa parámetros de sistema para endpoints (web_editor.olg_api_endpoint)
- **Formateo**: Limpieza de bloques markdown/html y formato especial para precios

Esta sección está diseñada específicamente para ayudar a LLMs a entender la estructura y funcionamiento de este módulo. Para implementaciones recomendadas, consulta la guía técnica completa.

- Análisis de Campañas: Resumir el rendimiento de campañas de marketing (tasas de apertura, clics, conversiones) si los datos están integrados en Odoo.

- Variaciones de Contenido (A/B Testing): (Ya presente) Generar múltiples versiones de asuntos de correo, llamadas a la acción (CTAs) o pequeños textos para pruebas A/B.

🔄 Alternativas a IAP con APIs Gratuitas
----------------------------------------

**¡NUEVO!** Este módulo ahora incluye soporte para usar APIs de IA gratuitas como alternativa al servicio OLG (Odoo Language Generation) que requiere créditos IAP.

- **Hugging Face API**: Implementada con soporte completo
- **OpenAI API**: Ejemplo de integración disponible 
- **Google Gemini API**: Ejemplo de integración disponible
- **Ollama Local**: Para despliegue totalmente gratuito en servidores locales

Para configurar y usar estas alternativas, consulta la `Guía de APIs Alternativas <docs/ALTERNATIVE_API_GUIDE.md>`_.