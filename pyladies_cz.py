"""Create or serve the pyladies.cz website
"""

import sys
if sys.version_info < (3, 0):
    raise RuntimeError('You need Python 3.')

import os
import fnmatch
import datetime

from flask import Flask, render_template, url_for, send_from_directory
from flask import redirect
from flask_frozen import Freezer
import yaml
import jinja2
import markdown

from elsa import cli

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

@app.route('/ostrava_info/')
def ostrava_info():
    return render_template('ostrava_info.html')

@app.route('/praha_course/')
def praha_course():
    return render_template('praha_course.html', meetups=read_meetups_yaml('meetups/praha.yml'))

@app.route('/brno_course/')
def brno_course():
    return render_template('brno_course.html', meetups=read_meetups_yaml('meetups/brno.yml'))

@app.route('/ostrava_course/')
def ostrava_course():
    return render_template('ostrava_course.html', meetups=read_meetups_yaml('meetups/ostrava.yml'))

@app.route('/brno/')
def brno():
    return render_template('brno.html', plan=read_lessons_yaml('plans/brno.yml'))


@app.route('/praha/cznic/')
def praha():
    return render_template('praha.html', plan=read_lessons_yaml('plans/praha.yml'))

@app.route('/praha/msd/')
def praha_msd():
    return render_template('praha_msd.html', plan=read_lessons_yaml('plans/praha_msd.yml'))

@app.route('/ostrava/')
def ostrava():
    return render_template('ostrava.html', plan=read_lessons_yaml('plans/ostrava.yml'))

@app.route('/stan_se/')
def stan_se():
    return render_template('stan_se.html')

@app.route('/faq/')
def faq():
    return render_template('faq.html')

@app.route('/v1/<path:path>')
def v1(path):
    return send_from_directory(v1_path, path)

@app.route('/index.html')
def index_html():
    return redirect(url_for('index'))

@app.route('/course.html')
def course_html():
    return send_from_directory(orig_path, 'course.html')

@app.route('/googlecc704f0f191eda8f.html')
def google_verification():
    # Verification page for GMail on our domain
    return send_from_directory(app.root_path, 'google-verification.html')


##########
## Helpers

md = markdown.Markdown(extensions=['meta', 'markdown.extensions.toc'])

@app.template_filter('markdown')
def convert_markdown(text, inline=False):
    result = jinja2.Markup(md.convert(text))
    if inline and result[:3] == '<p>' and result[-4:] == '</p>':
        result = result[3:-4]
    return result

@app.template_filter('date_range')
def date_range(dates, sep='–'):
    start, end = dates
    pieces = []
    if start != end:
        if start.year != end.year:
            pieces.append('{d.day}. {d.month}. {d.year}'.format(d=start))
        elif start.month != end.month:
            pieces.append('{d.day}. {d.month}.'.format(d=start))
        else:
            pieces.append('{d.day}.'.format(d=start))
        pieces.append('–')
    pieces.append('{d.day}. {d.month}. {d.year}'.format(d=end))

    return ' '.join(pieces)


def read_yaml(filename):
    with open(filename, encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

def read_lessons_yaml(filename):
    data = read_yaml(filename)

    # workaround for http://stackoverflow.com/q/36157569/99057
    # Convert datetime objects to strings
    for lesson in data:
        if 'date' in lesson:
            lesson['dates'] = [lesson['date']]
        if 'description' in lesson:
            lesson['description'] = convert_markdown(lesson['description'],
                                                     inline=True)
        for mat in lesson.get('materials', ()):
            mat['name'] = convert_markdown(mat['name'], inline=True)

    return data


def read_meetups_yaml(filename):
    data = read_yaml(filename)

    today = datetime.date.today()


    for meetup in data:
        if 'frequency' not in meetup:
            # Make sure all mettups have 'date', 'start', and 'end'.
            if 'start' not in meetup:
                meetup['start'] = meetup['date']
            if 'date' not in meetup:
                meetup['date'] = meetup['start']
            if 'end' not in meetup:
                meetup['end'] = meetup['date']

            # Derive a URL for places that don't have one from the location
            if 'place' in meetup:
                if ('url' not in meetup['place']
                        and {'latitude', 'longitude'} <= meetup['place'].keys()):
                    meetup['place']['url'] = (
                        'http://mapy.cz/zakladni?q={p[name]},'
                        '{p[latitude]}N+{p[longitude]}E'.format(p=meetup['place']))

            # Figure out the status of registration
            if 'registration' in meetup:
                if 'end' in meetup['registration']:
                    if meetup['start'] <= today:
                        meetup['registration_status'] = 'meetup_started'
                    elif meetup['registration']['end'] >= today:
                        meetup['registration_status'] = 'running'
                    else:
                        meetup['registration_status'] = 'closed'
                else:
                    meetup['registration_status'] = 'running'
        else:
            meetup['end'] = today

    return {
        'current': [meetup for meetup in data
                if not meetup['end'] or meetup['end'] >= today],
        'past': [meetup for meetup in data
                if meetup['end'] < today],
    }


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
        'today': datetime.date.today(),
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
            if file == '.git':
                continue
            if not any(fnmatch.fnmatch(file, ig) for ig in IGNORE):
                path = os.path.relpath(os.path.join(name, file), v1_path)
                yield {'path': path}

if __name__ == '__main__':
    cli(app, freezer=freezer, base_url='http://pyladies.cz')
