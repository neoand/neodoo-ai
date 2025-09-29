========================================================
🚀 Unlock Odoo's Native AI: Text Generation & Automation
========================================================
**Effortless Backend Integration**

.. |badge1| image:: https://img.shields.io/badge/License-LGPL--3-blue.png
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |badge2| image:: https://img.shields.io/badge/Odoo%20Version-18.0-success.png
    :alt: Compatible with Odoo 18.0
.. |badge4| image:: https://img.shields.io/badge/LLM%20Technical%20Guide-Available-green.png
    :target: LLM_TECHNICAL_GUIDE.md
    :alt: LLM Technical Guide
.. |badge3| image:: https://img.shields.io/badge/Uses-Odoo%20AI%20Engine%20(IAP)-blue.png
    :alt: Uses Odoo AI Engine via IAP

|badge1| |badge2| |badge3| |badge4|


**Automate Tasks, Responses, and Text Generation in Odoo Backend Using AI!**

Odoo includes an AI engine (OLG) for text generation, but its standard use is limited to rich text editors and the **Website**.

.. raw:: html

   <img src="/neodoo_ai/static/src/img/ai_button.png"
        alt="AI Odoo on Website"
        style="border: 2px solid rgb(85, 222, 94); width: 200px; border-radius:10px;">


👌 This module **extends the power of Odoo's native AI**,

enabling you to easily use it from the **backend**, in **any model**, and most importantly,

**automate intelligent tasks**.

**Imagine automatically generating:**

- Email responses
- Reminders
- Summaries or drafts
- Advanced analytics and charts
- And much more, directly from your workflows.

This module provides a **robust, reusable, and easy** way to connect with Odoo's AI engine (via IAP),

whether from custom Python code or **directly from Automated Actions**.

👌 Problem Solved
---------------------

AI integration from the backend typically requires:

- Writing complex code to make IAP calls.
- Managing authentication and technical endpoint details.
- Implementing robust error handling (limits, availability).
- Reusing logic consistently.

**This module removes all that complexity for you!**


🌟 Key Benefits & Features 🌟
-----------------------------------------

- **Easy Integration:** Add AI to any model with `_inherit = ['your.model', 'ai.generator.mixin']`. Done!
- **Massive Time Savings:** Forget repetitive code. Develop AI-powered functions in minutes, not days.
- **Powerful Automation:** Use AI in **Automated Actions** (`base_automation`) to:

  - Generate email draft replies.

  - Summarize long texts (tasks, notes).

  - Create initial content (marketing, descriptions).

  - Personalize messages (follow-ups, reminders).

- **Reliable & Robust:** Handles common OLG service errors (limits, unavailability) with clear messages.
- **Clean Code (DRY):** Centralizes AI logic. Avoids duplication and ensures consistency.
- **Simple API:** `generate_ai_text(prompt)` for formatted results, `_generate_ai_text(prompt)` for raw response.
- **Odoo Standard:** Uses IAP infrastructure and native Odoo parameters.
- **Maximum Potential:** Easily extend Odoo's AI to any custom business process.


🚀 Supercharge Your Flows with Automated Actions! 🚀
-------------------------------------------------------

Integrate AI into Odoo's automation engine effortlessly.

Trigger smart actions based on events (creation, update), **without complex development** for each case.

**Example: Welcome Email for a CRM Lead (Website Source)**

1. Go to `Settings > Technical > Automation > Automated Actions`.
2. Create a new action:
    - **Model:** Lead/Opportunity (`crm.lead`)
    - **Trigger:** On Creation (or After Creation with Delay)
    - **Apply On:** Define your filters (e.g., Specific Source)
    - **Action To Perform:** Execute Code
3. In the **Code** block:

.. code-block:: python

    # Example: Generate a welcome email for leads from the web contact form
    for lead in records:
        if lead._context.get("website_id"):
            ai_tool = env['ai.generator.mixin']
            prompt = f"""
            Draft a friendly and professional welcome email.
            Lead: {lead.name} | Client: {lead.contact_name or 'Client'}
            Introduce [Your Company] and suggest a short call.
            Signature: [Your Team].
            """
            try:
                email_draft = ai_tool.generate_ai_text(prompt)
                if email_draft:
                        # Post the draft in the chatter for review
                        lead.message_post(
                            body=f"<b>AI Suggested Welcome Email:</b><br/>{email_draft}"
                        )
            except Exception as e:
                _logger.warning(f"AI draft generation failed for {lead.id}: {e}")


**The possibilities are endless!** Auto-replies, summaries, drafts, personalized communications... all automatic.


💡 More Use Case Ideas 💡
-------------------------------

- **Sales:** Follow-up drafts, note summaries.
- **Projects:** Task summaries, report drafts.
- **Support:** Response drafts, ticket summaries.
- **Marketing:** Post drafts, subject line variations (A/B testing).
- **Accounting:** Payment reminder drafts.
- **HR:** Job description drafts.


How It Works (Simplified)
-------------------------------

The module provides an "Abstract Model" (mixin): `ai.generator.mixin`.

By inheriting it, your Odoo model gains methods (`generate_ai_text`, etc.) to use the native AI

(OLG service) via the standard IAP mechanism. The mixin handles communication and technical errors.


🤓 For Developers: Extensibility & Clarity
---------------------------------------------------

.. note::
    Designed to be easy to use and extend.

- **Extensible:** Inherit `ai.generator.mixin` in any model along with its base: `_inherit = ['your.model', 'ai.generator.mixin']`.
- **Customizable:** Override `generate_ai_text` or `_generate_ai_text` in your model (using `super()`) to adjust pre/post-processing.
- **Clear Code:** The mixin's logic is straightforward (IAP call, error handling), easy to understand and adapt for a mid-level Odoo developer.
- **Solid Foundation:** Build advanced AI functionalities on top of this mixin without worrying about the underlying API mechanics.


Prerequisites
--------------

- **Odoo Version:** 18.0 (Adjust if applicable to others)
- **Dependencies:** Odoo standard `iap` module installed.
- **Odoo AI Service:** IAP service for **"AI Text Generation (OLG)"** **active and configured by default**.

  (This module uses that native infrastructure.)

- **Module** `base_automation` (Optional if adding Automated Actions).


Quick Start / Usage
--------------------

1. **Install** this module.
2. **Choose your usage method:**
    - **Direct Method:** ✅ No coding required, just invoke the AI text generation method.
    - **Extension Method:** 🧑🏻‍‍💻 Requires coding skills, ideal for implementing custom logic and extending functions as desired.

    **Direct Method:**

    .. code-block:: python

        ai_tool = env['ai.generator.mixin']
        for record in records:
            prompt = f"Respond to this client {record.contact_name} for the question {record.description} "
            try:
                summary = ai_tool.generate_ai_text(prompt)
                if summary:
                    record.message_post(body=summary)
            except Exception as e:
                _logger.warning(f"AI summary failed: {e}")
                
.. _llm_guide_en:

==================================================
🧠 Technical Guide for LLMs and AI Systems
==================================================

This section provides key information for LLMs and AI systems that need to understand this module.

For detailed technical documentation, refer to `LLM_TECHNICAL_GUIDE.md <LLM_TECHNICAL_GUIDE.md>`_.

Module Architecture
----------------------

- **ai.generator.mixin**: Main abstract model (core component)
- **IAP Integration**: Uses Odoo's In-App Purchase system for AI service access
- **OLG Service**: Communicates with Odoo Language Generation through JSON-RPC endpoints

Key Methods
-----------------

1. **generate_ai_text(prompt, conversation_history=None)**:
   - Public method to generate AI text
   - Handles errors and formats the result text
   - Returns HTML-safe Markup object or None on failure

2. **_generate_ai_text(prompt, conversation_history=None)**:
   - Low-level method handling direct API communication
   - Manages specific error cases (limits, long prompts)
   - Used internally by generate_ai_text

Integration Patterns
----------------------

1. **Direct Call** (without inheritance):
   ```python
   ai_tool = env['ai.generator.mixin']
   ai_text = ai_tool.generate_ai_text("My prompt")
   ```

2. **Model Inheritance**:
   ```python
   class MyModel(models.Model):
       _name = 'my.model'
       _inherit = ['my.model', 'ai.generator.mixin']
   ```

3. **Automated Actions**:
   ```python
   # In base.automation
   ai_tool = env['ai.generator.mixin']
   for record in records:
       result = ai_tool.generate_ai_text(f"Prompt for {record.name}")
   ```

Technical Considerations
----------------------

- **Error Handling**: UserError for API errors, AccessError for connection issues
- **Simple Cache**: Global PROCESSED_RECORDS list to avoid duplicate processing
- **Configuration**: Uses system parameters for endpoints (web_editor.olg_api_endpoint)
- **Formatting**: Cleans up markdown/HTML blocks and special formatting for prices

This section is specifically designed to help LLMs understand the structure and operation of this module. For recommended implementations, please refer to the complete technical guide.

📈 Invest in Efficiency - Integrate Odoo's AI Seamlessly! 📈
