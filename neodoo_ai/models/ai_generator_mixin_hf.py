# -*- coding: utf-8 -*-
"""
Extensão do módulo neodoo_ai para usar a API gratuita do Hugging Face
em vez do serviço OLG (Odoo Language Generation) pago via IAP.

Instruções:
1. Instale o pacote 'requests': pip install requests
2. Obtenha um token de API gratuito do Hugging Face: https://huggingface.co/settings/tokens
3. Configure o token em Configurações > Parâmetros do Sistema com a chave "hf_api_token"
4. Coloque este arquivo no diretório /models/ do módulo neodoo_ai
5. Adicione a importação no arquivo __init__.py dos modelos

Autor: Exemplo para Anderson Oliveira
"""

import logging
import json
import requests
import re

from markupsafe import Markup

from odoo import _, models, api
from odoo.exceptions import AccessError, UserError

_logger = logging.getLogger(__name__)

# Constante para o endpoint do Hugging Face
DEFAULT_HF_ENDPOINT = "https://api-inference.huggingface.co/models/"
DEFAULT_HF_MODEL = "google/flan-t5-large"  # Modelo relativamente leve com bom desempenho


class AiGeneratorMixinHF(models.AbstractModel):
    """
    Extensão do mixin AI Generator para usar a API gratuita do Hugging Face.
    Substitui a implementação original que usa a API OLG via IAP.
    """

    _inherit = "ai.generator.mixin"

    def _generate_ai_text(self, prompt, conversation_history=None):
        """
        Sobrescreve o método _generate_ai_text para usar a API do Hugging Face
        em vez da API OLG da Odoo.

        :param prompt: O prompt a ser enviado para a API.
        :param conversation_history: Histórico de conversa (ignorado nesta implementação).
        :return: O texto gerado pela IA.
        :raises: UserError para erros específicos da API, AccessError para problemas de conexão.
        """
        _logger.info("Gerando texto com IA via API Hugging Face")
        if conversation_history is None:
            conversation_history = []

        ir_config_parameter = self.env["ir.config_parameter"].sudo()

        # Obter parâmetros de configuração
        hf_api_token = ir_config_parameter.get_param("hf_api_token")
        hf_model = ir_config_parameter.get_param("hf_model", DEFAULT_HF_MODEL)
        hf_api_endpoint = ir_config_parameter.get_param(
            "hf_api_endpoint", DEFAULT_HF_ENDPOINT
        )

        if not hf_api_token:
            _logger.error(
                "Token de API Hugging Face não está configurado. "
                "Configure o parâmetro 'hf_api_token' nas configurações do sistema."
            )
            raise UserError(
                _(
                    "API Hugging Face não configurada. Adicione o token em "
                    "Configurações > Parâmetros do Sistema com a chave 'hf_api_token'."
                )
            )

        # Preparar a URL da API
        api_url = f"{hf_api_endpoint}{hf_model}"
        
        # Adicionar contexto da conversa ao prompt se disponível
        if conversation_history:
            context = "\n".join([
                f"{'User' if i%2==0 else 'Assistant'}: {msg}" 
                for i, msg in enumerate(conversation_history)
            ])
            full_prompt = f"{context}\nUser: {prompt}\nAssistant:"
        else:
            full_prompt = prompt

        # Preparar os headers e payload
        headers = {
            "Authorization": f"Bearer {hf_api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_length": 500,
                "temperature": 0.7,
                "top_p": 0.9,
                "do_sample": True
            }
        }

        try:
            # Fazer a chamada à API
            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Verificar se a resposta foi bem-sucedida
            if response.status_code == 200:
                try:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "")
                        # Remover o prompt do início da resposta se estiver presente
                        if generated_text.startswith(full_prompt):
                            generated_text = generated_text[len(full_prompt):].strip()
                        return generated_text
                    return str(result)
                except (json.JSONDecodeError, AttributeError) as e:
                    _logger.error(f"Erro ao processar resposta da API: {e}")
                    return response.text
            
            # Tratar códigos de erro comuns
            elif response.status_code == 401:
                raise AccessError(_("Token de API inválido ou expirado."))
            elif response.status_code == 429:
                raise UserError(_("Limite de requisições atingido na API Hugging Face."))
            elif response.status_code == 503:
                raise UserError(_("Serviço temporariamente indisponível. Tente novamente mais tarde."))
            else:
                # Outros códigos de erro
                error_msg = f"Erro na API Hugging Face: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail.get('error', '')}"
                except:
                    error_msg += f" - {response.text[:100]}"
                
                _logger.error(error_msg)
                raise UserError(_(error_msg))
        
        except requests.exceptions.ConnectionError:
            _logger.error("Erro de conexão com a API Hugging Face")
            raise AccessError(_("Não foi possível conectar à API Hugging Face. Verifique sua conexão."))
        
        except requests.exceptions.Timeout:
            _logger.error("Timeout ao conectar à API Hugging Face")
            raise AccessError(_("Timeout ao conectar à API Hugging Face. Tente novamente mais tarde."))
        
        except Exception as e:
            _logger.error(f"Erro inesperado ao chamar API Hugging Face: {e}", exc_info=True)
            raise UserError(_("Erro inesperado ao processar a requisição: %s", str(e)))