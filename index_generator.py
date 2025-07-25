import os
from jinja2 import Environment, FileSystemLoader

def generate_index_html(categories, template_name="index-template.html", output_path="docs/index.html"):
    # Define local Jinja2 environment
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    rendered = template.render(categories=categories)

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write the rendered HTML to the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"✅ {output_path} generated successfully.")
