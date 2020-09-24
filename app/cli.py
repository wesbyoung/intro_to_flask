import click, os

def register(app):
    @app.cli.group()
    def blueprint():
        """Blueprint creation commands"""
        pass

    @blueprint.command()
    @click.argument('name')
    def create(name):
        """Create new Flask Blueprint"""
        basedir = os.path.abspath(os.path.dirname(__name__)) + f'/app/blueprints/{name}'
        static_folder = os.path.abspath(os.path.dirname(__name__)) + f'/app/blueprints/{name}/static'
        css_folder = os.path.abspath(os.path.dirname(__name__)) + f'/app/blueprints/{name}/static/css'
        js_folder = os.path.abspath(os.path.dirname(__name__)) + f'/app/blueprints/{name}/static/js'
        templates_folder = os.path.abspath(os.path.dirname(__name__)) + f'/app/blueprints/{name}/templates/{name}'

        try:
            if not os.path.exists(basedir):
                os.makedirs(basedir)
                os.makedirs(static_folder)
                os.makedirs(css_folder)
                os.makedirs(js_folder)
                os.makedirs(templates_folder)
                init_file = open(f'{basedir}/__init__.py', 'w')
                init_file.close()
                routes_file = open(f'{basedir}/routes.py', 'w')
                routes_file.close()
        except Exception as error:
            print(f'Something went wrong with creating the Blueprint called {name}')
            print(error)
        return print("Blueprint created successfully")