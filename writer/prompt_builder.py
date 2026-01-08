from string import Template

def build_prompt(template_path, context):
    template = Template(
        open(template_path, encoding="utf-8").read()
    )
    return template.substitute(context)

