from jinja2 import Environment, FileSystemLoader

def get_templated_email(*args, **kwargs):
    jinja_env = Environment(loader=FileSystemLoader("./templates"))
    template = jinja_env.get_template("email.html")
    return template.render(*args, **kwargs)
