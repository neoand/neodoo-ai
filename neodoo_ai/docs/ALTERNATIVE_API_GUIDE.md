# Usando APIs de IA Alternativas

Este guia mostra como você pode usar APIs gratuitas ou alternativas em vez do serviço OLG (Odoo Language Generation) padrão que requer créditos IAP pagos.

## 1. Hugging Face API (Implementada)

A API do Hugging Face oferece um plano gratuito com limites generosos e acesso a milhares de modelos de IA.

### Configuração:

1. **Instale o pacote Python necessário**:
   ```
   pip install requests
   ```

2. **Obtenha um token de API gratuito**:
   - Crie uma conta em [Hugging Face](https://huggingface.co/)
   - Acesse [Settings > Access Tokens](https://huggingface.co/settings/tokens)
   - Crie um token com permissão de leitura

3. **Configure no Odoo**:
   - Vá para Configurações > Técnico > Parâmetros > Parâmetros do Sistema
   - Ative a opção "Usar API Hugging Face"
   - Insira seu token de API
   - Opcionalmente, modifique o modelo (padrão: google/flan-t5-large)

## 2. Outras APIs Alternativas

Você pode adaptar o código para usar outras APIs seguindo o mesmo padrão:

### OpenAI API

```python
# Exemplo de adaptação para API OpenAI (não implementada)
import openai

def _generate_ai_text_openai(self, prompt, conversation_history=None):
    openai.api_key = self.env["ir.config_parameter"].sudo().get_param("openai_api_key")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    return response.choices[0].message.content
```

### Google Gemini API

```python
# Exemplo de adaptação para API Gemini (não implementada)
import google.generativeai as genai

def _generate_ai_text_gemini(self, prompt, conversation_history=None):
    api_key = self.env["ir.config_parameter"].sudo().get_param("gemini_api_key")
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    
    return response.text
```

### Ollama (Local)

Para uma opção totalmente gratuita, você pode executar modelos localmente com Ollama:

```python
# Exemplo de adaptação para Ollama local (não implementada)
import requests

def _generate_ai_text_ollama(self, prompt, conversation_history=None):
    ollama_endpoint = self.env["ir.config_parameter"].sudo().get_param(
        "ollama_endpoint", "http://localhost:11434/api/generate"
    )
    ollama_model = self.env["ir.config_parameter"].sudo().get_param(
        "ollama_model", "llama2"
    )
    
    response = requests.post(
        ollama_endpoint,
        json={"model": ollama_model, "prompt": prompt}
    )
    
    return response.json().get("response", "")
```

## Guia de Implementação

Para implementar uma nova API:

1. Crie um arquivo em `models/ai_generator_mixin_NOME.py`
2. Herde o modelo `ai.generator.mixin` 
3. Sobrescreva o método `_generate_ai_text`
4. Atualize `models/__init__.py` para importar seu arquivo
5. Adicione configurações no painel de administração

## Observações de Performance

- Modelos locais são mais lentos, mas não têm custos contínuos
- As APIs gratuitas geralmente têm limites de uso
- Compare a qualidade das respostas entre diferentes modelos para o seu caso de uso específico