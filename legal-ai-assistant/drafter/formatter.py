# drafter/formatter.py

import os
from jinja2 import Template
from weasyprint import HTML

class Formatter:
    """Converts clause list and inputs into HTML and PDF."""
    
    def __init__(self, template_dir=None):
        if template_dir is None:
            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.template_dir = template_dir
    
    def render_html(self, agreement_type, clauses, inputs):
        template_path = os.path.join(self.template_dir, f"{agreement_type}.html")
        with open(template_path, 'r', encoding='utf-8') as f:
            template_str = f.read()
        template = Template(template_str)
        html = template.render(clauses=clauses, inputs=inputs)
        return html
    
    def generate_pdf(self, html, output_path=None):
        pdf = HTML(string=html).write_pdf()
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(pdf)
        return pdf