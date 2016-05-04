import sys
import os

from flask import Flask, render_template, url_for, send_from_directory
import yaml
import jinja2
import markdown

if sys.version_info < (3, 0):
    raise RuntimeError('You need Python 3.')

app = Flask('pyladies_cz')


########
## Views

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/brno_info')
def brno_info():
    return render_template('brno_info.html')


@app.route('/praha_info')
def praha_info():
    return render_template('praha_info.html')


@app.route('/brno')
def brno():
    return render_template('brno.html', plan=read_yaml('plans/brno.yml'))


@app.route('/praha')
def praha():
    return render_template('praha.html', plan=read_yaml('plans/praha.yml'))


@app.route('/v1/<path:path>')
def v1(path):
    return send_from_directory('original/v1/', path)


##########
## Helpers

md = markdown.Markdown(extensions=['meta'])
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
        return name
    return url_for(name)


@app.context_processor
def inject_context():
    return {
        'pathto': pathto,
    }


#########
## Runner

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port, debug=True)
