# drafter/formatter.py
import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")


class Formatter:
    def __init__(self):
        if os.path.isdir(TEMPLATE_DIR):
            self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        else:
            self.env = None
            print(f"⚠️ Template directory not found at {TEMPLATE_DIR}")

    def render_html(self, agreement_type, clauses, inputs):
        """Render HTML using Jinja2 template"""
        template_file = f"{agreement_type}.html"

        if self.env:
            try:
                template = self.env.get_template(template_file)
                return template.render(clauses=clauses, inputs=inputs)
            except Exception as e:
                print(f"Template error: {e}")

        # Fallback HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><title>{agreement_type}</title></head>
        <body>
            <h1>{agreement_type.replace('_', ' ').upper()}</h1>
        """
        for clause in clauses:
            html += f"<h2>{clause['title']}</h2><p>{clause['text']}</p>"
        html += "</body></html>"
        return html

    def generate_pdf(self, html):
        """Return HTML as bytes (since WeasyPrint is not working)"""
        return html.encode('utf-8')