import logging
import re

from markupsafe import Markup

from odoo import _, models
from odoo.exceptions import AccessError, UserError

from odoo.addons.iap.tools import iap_tools

_logger = logging.getLogger(__name__)

# Constante para el endpoint por defecto
DEFAULT_OLG_ENDPOINT = "https://olg.api.odoo.com"
PROCESSED_RECORDS = []


class AiGeneratorMixin(models.AbstractModel):
    """
    Abstract Mixin Model providing reusable AI text generation functionality
    by calling the Odoo Language Generation (OLG) API via IAP.
    """

    _name = "ai.generator.mixin"
    _description = "AI Text Generator Mixin"

    def generate_ai_text(self, prompt: str, conversation_history: list = None):
        """
        Public wrapper method to generate AI text and perform basic formatting.

        Calls the core _generate_ai_text method and applies simple regex
        substitutions (removes ```html``` blocks and bolds prices like $XX.YY).

        :param prompt: str: The input text/question for the AI.
        :param conversation_history:list:  Optional list of previous exchanges.
        :return: Markup object with the formatted AI response, or None if no
                 response or error during generation.
        :raises: Can re-raise UserError or AccessError from _generate_ai_text.
        """
        if not prompt:
            _logger.warning("generate_ai_text called with an empty prompt.")
            return None
        if self._context.get("active_model") and self._context.get("active_id"):
            act_rec = f"{self._context['active_model']}.{self._context['active_id']}"
            if act_rec not in PROCESSED_RECORDS:
                PROCESSED_RECORDS.append(act_rec)
                _logger.warning(f"Processing record: {act_rec}")
            else:
                _logger.warning(f"Skipping already processed record: {act_rec}")
                return False
        if PROCESSED_RECORDS and len(PROCESSED_RECORDS) > 50:
            _logger.info("Clearing processed records list.")
            PROCESSED_RECORDS.clear()

        # Llama al método principal que maneja la llamada a la API y los errores
        try:
            prompt += "\n **Remember to send the response in HTML format!**"
            _logger.warning(f"******** Generating AI text: {prompt}")
            raw_response = self._generate_ai_text(prompt, conversation_history)
        except (UserError, AccessError):
            # Re-raise known handled errors if needed by the caller
            raise
        except Exception:
            # Log unexpected errors from _generate_ai_text but return None here
            # to simplify caller logic (they might not want to handle all errors)
            _logger.error(
                "Unexpected error from _generate_ai_text caught in wrapper.",
                exc_info=True,
            )
            return None  # Indicate failure without raising unexpected exceptions

        if raw_response:
            _logger.debug("AI raw response received, applying formatting.")
            # Regex para limpiar ```html y ``` (más robusto)
            html_tag_pattern = r"^\s*```html\s*\n?|\n?\s*```\s*$"
            message = re.sub(
                html_tag_pattern, "", raw_response, flags=re.MULTILINE | re.IGNORECASE
            ).strip()

            # Regex para poner en negrita precios como $00,00
            price_format_pattern = r"(\$\d+\.\d{2})\b"
            formatted_message = re.sub(
                price_format_pattern, r"<strong>$\1</strong>", message
            )

            # Devolver como Markup para renderizado HTML seguro
            return Markup(formatted_message)
        else:
            _logger.warning("No AI response generated (raw_response was empty/None).")
            return None

    def _generate_ai_text(self, prompt, conversation_history=None):
        """
        Core method to get a response from the Odoo Language Generation API (OLG).

        Handles the IAP call and specific API error statuses. Uses system
        parameter 'web_editor.olg_api_endpoint' if set, otherwise falls back
        to the default constant endpoint.

        :param prompt: The prompt string to send to the API.
        :param conversation_history: List of dicts for previous turns. Defaults to [].
        :return: The generated text content string if successful, otherwise None
                 (specifically if config is missing).
        :raises UserError: For specific API errors (prompt too long, limit reached).
        :raises AccessError: If the IAP endpoint is unreachable or auth fails.
        :raises Exception: For other unexpected IAP/network errors.
        """
        _logger.info("Attempting to generate AI text via OLG API.")
        if conversation_history is None:
            conversation_history = []

        ir_config_parameter = self.env["ir.config_parameter"].sudo()

        # Obtener parámetro o usar default
        olg_api_endpoint = ir_config_parameter.get_param(
            "web_editor.olg_api_endpoint", DEFAULT_OLG_ENDPOINT
        )

        database_id = ir_config_parameter.get_param("database.uuid")

        if not database_id:
            _logger.error(
                "OLG API Database ID is not configured in system parameters. "
                "Cannot generate AI text."
            )
            # Devolver None si la configuración esencial falta
            return None

        _logger.debug(f"Using OLG API Endpoint: {olg_api_endpoint}")
        _logger.debug(f"Database ID for OLG call: {database_id}")

        api_url = f"{olg_api_endpoint}/api/olg/1/chat"
        params = {
            "prompt": prompt,
            "conversation_history": conversation_history,
            "database_id": database_id,
        }

        try:
            response = iap_tools.iap_jsonrpc(
                api_url,
                params=params,
                timeout=30,  # Considera si 30s es suficiente
            )
            _logger.debug(f"OLG API response status: {response.get('status')}")

        except AccessError as e:
            # Error de IAP (servicio no disponible, créditos, config incorrecta)
            _logger.error(f"AccessError calling OLG API: {e}", exc_info=True)
            # Mensaje más específico para AccessError
            raise AccessError(
                _(
                    "AI Service Unreachable. Check IAP configuration, credits, "
                    "or Odoo's service status."
                )
            ) from e

        # --- Procesar la respuesta ---
        status = response.get("status")
        if status == "success":
            return response.get("content")
        elif status == "error_prompt_too_long":
            raise UserError(
                _("Sorry, your prompt is too long. " "Try to say it in fewer words.")
            )
        elif status == "limit_call_reached":
            raise UserError(
                _(
                    "You have reached the maximum number of requests for this "
                    "service. Try again later."
                )
            )
        else:
            # Capturar otros errores reportados por el servicio
            error_message = response.get("error_message", "Unknown error")
            _logger.error(
                f"OLG API returned error: status='{status}', "
                f"message='{error_message}'"
            )
            raise UserError(
                _(
                    "Sorry, we could not generate a response. Error: %s. "
                    "Please try again later.",
                    error_message,
                )
            )
