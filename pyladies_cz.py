"""Create or serve the pyladies.cz website
"""

import sys
if sys.version_info < (3, 0):
    raise RuntimeError('You need Python 3.')

import os
import fnmatch
import urllib.parse

from flask import Flask, render_template, url_for, send_from_directory
from flask import redirect
from flask_frozen import Freezer
import yaml
import jinja2
import markdown
import click

app = Flask('pyladies_cz')
app.config['TEMPLATES_AUTO_RELOAD'] = True

orig_path = os.path.join(app.root_path, 'original/')
v1_path = os.path.join(orig_path, 'v1/')

########
## Views

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/brno_info/')
def brno_info():
    return render_template('brno_info.html')


@app.route('/praha_info/')
def praha_info():
    return render_template('praha_info.html')

@app.route('/praha_course/')
def praha_info():
    return render_template('praha_course.html')

@app.route('/brno_course/')
def praha_info():
    return render_template('brno_course.html')

@app.route('/brno/')
def brno():
    return render_template('brno.html', plan=read_yaml('plans/brno.yml'))


@app.route('/praha/')
def praha():
    return render_template('praha.html', plan=read_yaml('plans/praha.yml'))

@app.route('/stan_se/')
def stan_se():
    return render_template('stan_se.html')

@app.route('/v1/<path:path>')
def v1(path):
    return send_from_directory(v1_path, path)

@app.route('/index.html')
def index_html():
    return redirect(url_for('index'))

@app.route('/course.html')
def course_html():
    return send_from_directory(orig_path, 'course.html')

@app.route('/CNAME')
def cname():
    return app.config['SERVER_NAME']


##########
## Helpers

md = markdown.Markdown(extensions=['meta', 'markdown.extensions.toc'])

@app.template_filter('markdown')
def convert_markdown(text, inline=False):
    result = jinja2.Markup(md.convert(text))
    if inline and result[:3] == '<p>' and result[-4:] == '</p>':
        result = result[3:-4]
    return result


def read_yaml(filename):
    with open(filename, encoding='utf-8') as file:
        data = yaml.safe_load(file)

    # workaround for http://stackoverflow.com/q/36157569/99057
    # Convert datetime objects to strings
    for lesson in data:
        if 'date' in lesson:
            lesson['date'] = str(lesson['date'])
        if 'description' in lesson:
            lesson['description'] = convert_markdown(lesson['description'],
                                                     inline=True)
        for mat in lesson['materials']:
            mat['name'] = convert_markdown(mat['name'], inline=True)

    return data


def pathto(name, static=False):
    if static:
        prefix = '_static/'
        if name.startswith(prefix):
            return url_for('static', filename=name[len(prefix):])
        prefix = 'v1/'
        if name.startswith(prefix):
            return url_for('v1', path=name[len(prefix):])
        return name
    return url_for(name)


@app.context_processor
def inject_context():
    return {
        'pathto': pathto,
    }


##########
## Freezer

freezer = Freezer(app)

@freezer.register_generator
def v1():
    IGNORE = ['*.aux', '*.out', '*.log', '*.scss', '.travis.yml', '.gitignore']
    for name, dirs, files in os.walk(v1_path):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if not any(fnmatch.fnmatch(file, ig) for ig in IGNORE):
                path = os.path.relpath(os.path.join(name, file), v1_path)
                yield {'path': path}


def freeze_app(path, base_url):
    app.config['FREEZER_DESTINATION'] = path
    app.config['FREEZER_BASE_URL'] = base_url
    app.config['SERVER_NAME'] = urllib.parse.urlparse(base_url).netloc
    freezer.freeze()


#########
## Runner


def main():
    return cli(obj={})


@click.group(context_settings=dict(help_option_names=['-h', '--help']),
             help=__doc__)
def cli():
    pass


@cli.command()
@click.option('--port', type=int, default=8003,
              help='Port to listen at')
def serve(port):
    """Run a debug server"""
    app.run(host='0.0.0.0', port=port, debug=True)

@cli.command()
@click.option('--path', default=os.path.join(app.root_path, '_build'),
              help='Output path')
@click.option('--base-url', default='http://pyladies.cz/',
              help='URL for the application, used for external links')
@click.option('--serve/--no-serve',
              help='After building the site, run a server with it')
@click.option('--port', default=8003,
              help='Port used for --serve')
def freeze(path, base_url, serve, port):
    """Build a static site"""
    freeze_app(path, base_url)
    if serve:
        freezer.serve(port=port)

if __name__ == '__main__':
    cli()
