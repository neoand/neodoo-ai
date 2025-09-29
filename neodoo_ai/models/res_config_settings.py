# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    use_huggingface_api = fields.Boolean(
        string="Use Hugging Face API",
        help="Enable this to use Hugging Face API instead of Odoo OLG service"
    )
    hf_api_token = fields.Char(
        string="Hugging Face API Token",
        help="API token for Hugging Face"
    )
    hf_model = fields.Char(
        string="Hugging Face Model",
        help="Model to use for text generation (e.g., google/flan-t5-large)"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        
        res.update(
            use_huggingface_api=ir_config.get_param('use_huggingface_api', 'False').lower() == 'true',
            hf_api_token=ir_config.get_param('hf_api_token', False),
            hf_model=ir_config.get_param('hf_model', 'google/flan-t5-large')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ir_config = self.env['ir.config_parameter'].sudo()
        
        ir_config.set_param('use_huggingface_api', str(self.use_huggingface_api))
        ir_config.set_param('hf_api_token', self.hf_api_token or '')
        ir_config.set_param('hf_model', self.hf_model or 'google/flan-t5-large')