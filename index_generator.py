from jinja2 import Environment, FileSystemLoader
import os

def generate_index_html(categories, template_path="templates/index-template.html", output_path="index.html"):
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)

    rendered = template.render(categories=categories)

    # Ensure output folder exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ {output_path} generated successfully.")
