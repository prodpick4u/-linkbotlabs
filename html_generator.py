from jinja2 import Environment, FileSystemLoader, select_autoescape

def render_html_from_template(template_name, context, output_path, template_dir="templates"):
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template(template_name)
    html = template.render(context)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
