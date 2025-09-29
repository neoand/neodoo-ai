===================================================
🧠 LLM/AI Technical Guide: AI-Powered Odoo Backend
===================================================

This section provides detailed technical information specifically designed for LLMs and AI systems to better understand this module's architecture, implementation, and usage patterns.

## Module Architecture

```
neodoo_ai/
├── models/
│   ├── __init__.py            # Imports ai_generator_mixin
│   └── ai_generator_mixin.py  # Core implementation of AI functionality
├── static/
│   └── src/
│       └── img/               # Contains only ai_button.png
├── __init__.py                # Standard Odoo module entry point
├── __manifest__.py            # Module metadata and dependencies
├── README.rst                 # User documentation (Spanish)
└── readme_en.rst              # User documentation (English)
```

## Core Components

### 1. AI Generator Mixin (`ai.generator.mixin`)

This abstract model serves as the central component of the module. It can be used in two ways:
- Direct invocation via `env['ai.generator.mixin'].generate_ai_text(prompt)`
- Model inheritance: `_inherit = ['your.model', 'ai.generator.mixin']`

**Key Methods:**

```python
# Public method with error handling and text formatting
def generate_ai_text(self, prompt: str, conversation_history: list = None):
    """
    Generates AI text with formatting and error handling.
    
    Args:
        prompt (str): Text prompt for the AI model
        conversation_history (list, optional): Previous conversation turns
        
    Returns:
        Markup: HTML-safe formatted text or None on failure
        
    Raises:
        UserError: For service-specific errors (prompt too long, limits)
        AccessError: For connectivity/authentication issues
    """
    # Implementation details...
    
# Low-level method for direct API communication
def _generate_ai_text(self, prompt, conversation_history=None):
    """
    Core method that communicates with Odoo Language Generation API.
    
    Args:
        prompt (str): Text prompt for the API
        conversation_history (list, optional): Previous exchanges
        
    Returns:
        str: Generated text if successful, None otherwise
        
    Raises:
        UserError: API-specific errors (limits, length)
        AccessError: Connection/authentication errors
        Exception: Other unexpected errors
    """
    # Implementation details...
```

### 2. IAP Integration

The module uses Odoo's IAP (In-App Purchase) system for billing and API access:

```python
# Configuration retrieval
olg_api_endpoint = ir_config_parameter.get_param(
    "web_editor.olg_api_endpoint", DEFAULT_OLG_ENDPOINT
)
database_id = ir_config_parameter.get_param("database.uuid")

# API call
response = iap_tools.iap_jsonrpc(
    api_url,
    params={
        "prompt": prompt,
        "conversation_history": conversation_history,
        "database_uuid": database_uuid,
    },
    timeout=30,
)
```

### 3. Error Management System

The module implements a comprehensive error handling system:

1. **Service-Specific Errors**:
   - `error_prompt_too_long`: Prompt exceeds API limits
   - `limit_call_reached`: API usage quota exceeded

2. **Infrastructure Errors**:
   - `AccessError`: Connection failures, auth issues
   - General exceptions: Unexpected errors

3. **Response Processing**:
   - HTML formatting cleanup
   - Special text formatting (e.g., price formatting)

4. **Duplicate Prevention**:
   - Tracks processed records in `PROCESSED_RECORDS` list
   - Prevents duplicate API calls for same record

## Integration Patterns

### Pattern 1: Direct Invocation

```python
# Best for automated actions, server actions, or crons
def process_records(self, records):
    ai_tool = self.env['ai.generator.mixin']
    for record in records:
        try:
            prompt = f"Generate a summary for: {record.name}\n\nDetails: {record.description}"
            result = ai_tool.generate_ai_text(prompt)
            if result:
                # Handle successful response
                record.message_post(body=f"<b>AI Summary:</b><br/>{result}")
        except Exception as e:
            # Handle errors
            _logger.warning(f"AI text generation failed for record {record.id}: {e}")
```

### Pattern 2: Model Inheritance

```python
# Best for adding AI capabilities directly to a business model
class ProjectTask(models.Model):
    _name = 'project.task'
    _inherit = ['project.task', 'ai.generator.mixin']
    
    def generate_task_summary(self):
        self.ensure_one()
        try:
            prompt = f"""
            Task: {self.name}
            Description: {self.description or ''}
            Assigned to: {self.user_id.name or 'Unassigned'}
            
            Generate a concise professional summary of this task.
            """
            summary = self.generate_ai_text(prompt)
            if summary:
                self.message_post(body=f"<b>AI Task Summary:</b><br/>{summary}")
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {'message': _("Summary generated successfully"), 'type': 'success'}
                }
        except UserError as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {'message': str(e), 'type': 'warning'}
            }
```

### Pattern 3: Automated Actions

```python
# Code block for base.automation record
# Example: Auto-summarize long email conversations
for record in records:
    if len(record.body or '') > 1000:  # Long email
        ai_tool = env['ai.generator.mixin']
        prompt = f"""
        Summarize the following email conversation in a professional, concise way.
        Focus on key points, action items, and deadlines.
        
        EMAIL: {record.body}
        """
        try:
            summary = ai_tool.generate_ai_text(prompt)
            if summary:
                record.message_post(
                    body=f"<b>AI Email Summary:</b><br/>{summary}",
                    subtype_xmlid="mail.mt_note"
                )
        except Exception as e:
            continue  # Skip on error
```

## Common Challenges and Solutions

### 1. Handling API Limits

```python
# Implement rate limiting and batching
def process_with_rate_limiting(self, records, batch_size=5, delay_seconds=2):
    """Process records in batches with delay to respect API limits."""
    ai_tool = self.env['ai.generator.mixin']
    for i, record in enumerate(records):
        # Add delay every batch_size records
        if i > 0 and i % batch_size == 0:
            time.sleep(delay_seconds)
            
        try:
            # AI processing...
            prompt = f"Process record {record.name}"
            ai_tool.generate_ai_text(prompt)
        except UserError as e:
            if "limit_call_reached" in str(e):
                # Handle limit reached
                _logger.warning("API limit reached, stopping batch processing")
                return False
```

### 2. Prompt Engineering for Odoo Context

```python
# Effective prompt structure for Odoo business contexts
def build_effective_prompt(self, record, task_type):
    """
    Build a well-structured prompt with proper context for better AI responses.
    
    Args:
        record: Odoo record to extract data from
        task_type: Type of AI task (summary, response, analysis)
    """
    # Common header with system instructions
    prompt = f"""
    You are an AI assistant helping with Odoo ERP tasks.
    Task: {task_type}
    
    # Context Information
    - Company: {self.env.company.name}
    - Module: {record._name}
    - Record: {record.name or record.display_name}
    """
    
    # Task-specific instructions
    if task_type == "summary":
        prompt += f"""
        # Instructions
        - Summarize the following content in 3-5 bullet points
        - Maintain professional language
        - Focus on key business details
        - Highlight any action items or deadlines
        
        # Content to Summarize
        {record.description or ''}
        """
    
    return prompt
```

### 3. Handling Multi-language Environments

```python
def generate_localized_ai_text(self, record, prompt_template, lang_code=None):
    """Generate AI text respecting Odoo's multi-language environment."""
    # Get language from context, record partner, or company
    if not lang_code:
        lang_code = (
            self.env.context.get('lang') or 
            record.partner_id.lang or 
            self.env.company.partner_id.lang or
            'en_US'
        )
    
    # Load translations if needed
    current_lang = self.env['res.lang']._lang_get(lang_code)
    
    # Add language instruction to prompt
    lang_name = current_lang.name or 'English'
    localized_prompt = prompt_template + f"\n\nRespond in {lang_name}."
    
    return self.generate_ai_text(localized_prompt)
```

## Performance Considerations

1. **Caching Strategy**: The module uses a simple list-based caching mechanism to prevent duplicate processing:
   ```python
   PROCESSED_RECORDS = []  # Module-level cache of processed records
   ```
   
   For production environments with high throughput, consider implementing a more robust caching solution:
   ```python
   # Example of Redis-based caching for distributed environments
   def is_record_processed(self, record):
       """Check if record was already processed using Redis cache."""
       cache_key = f"ai_processed:{record._name}:{record.id}"
       return bool(self.env['redis.cache'].get(cache_key))
       
   def mark_record_processed(self, record, ttl=3600):
       """Mark record as processed with TTL."""
       cache_key = f"ai_processed:{record._name}:{record.id}"
       self.env['redis.cache'].set(cache_key, '1', ttl=ttl)
   ```

2. **API Call Optimization**: Group similar requests when possible:
   ```python
   # Instead of multiple single calls
   def batch_process_descriptions(self, records):
       """Process multiple records in one API call where possible."""
       if not records:
           return
           
       # Collect all descriptions
       descriptions = []
       for record in records:
           descriptions.append(f"- {record.name}: {record.description}")
           
       # Single API call
       prompt = f"""
       Process the following items and generate a summary for each:
       
       {'\n'.join(descriptions)}
       
       Format as JSON with ID as key and summary as value.
       """
       
       try:
           result = self.env['ai.generator.mixin'].generate_ai_text(prompt)
           # Parse JSON result and update records
           # ...
       except Exception as e:
           _logger.error(f"Batch processing failed: {e}")
   ```

## Common Example Implementations

### Email Response Draft Generator

```python
# Add to CRM Lead or Helpdesk Ticket
def generate_response_draft(self):
    """Generate a response draft based on customer inquiry."""
    self.ensure_one()
    
    # Build context from record
    customer_name = self.partner_id.name or "Customer"
    previous_communication = self.description or ""
    
    prompt = f"""
    Generate a professional response draft to the following customer inquiry.
    
    Customer: {customer_name}
    Company: {self.env.company.name}
    
    Previous Communication:
    {previous_communication}
    
    Guidelines:
    - Be professional and courteous
    - Address specific points in the inquiry
    - Use a friendly, helpful tone
    - Keep it concise (max 150 words)
    - Sign as {self.user_id.name or 'Customer Support'}
    """
    
    try:
        response = self.generate_ai_text(prompt)
        if response:
            self.message_post(
                body=f"<b>Draft Response (AI-generated):</b><br/>{response}",
                subtype_xmlid="mail.mt_note"
            )
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': _("Response draft generated successfully"),
                    'type': 'success'
                }
            }
    except UserError as e:
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'message': str(e), 'type': 'warning'}
        }
```

This enhanced technical guide provides LLMs with structured knowledge about the module's architecture, implementation patterns, error handling, and common usage scenarios. It includes concrete code examples and addresses specific challenges related to using the AI capabilities in an Odoo environment.