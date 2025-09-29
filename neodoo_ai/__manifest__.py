{
    "name": "🤖 NeoDoo AI - Automation Tool for Odoo Backend",
    "version": "18.0.1.0.1",
    "summary": """
    Automate Business Processes with Odoo's AI in the Backend
    """,
    "author": "OdooErpCloud",
    "website": "https://odooerpcloud.com",
    "category": "Technical/Tools",
    "license": "LGPL-3",
    "depends": [
        "iap",
    ],
    "data": [
        "views/hf_settings_views.xml",
    ],
    "external_dependencies": {
        "python": ["requests"],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "description": """
    This module allows you to leverage AI capabilities in your Odoo backend.
    
    New Feature:
    - Integration with Hugging Face's free API service as an alternative to Odoo's OLG
    - Support for custom AI models
    
    Installation:
    1. Install the Python package: pip install requests
    2. Install this module
    3. Configure your Hugging Face API token in Settings > Technical > Parameters > System Parameters
    """
}
