#!/usr/bin/env python3

"""Create or serve the pyladies.cz website
"""

import sys
if sys.version_info < (3, 0):
    raise RuntimeError('You need Python 3.')

import os
import fnmatch
import time
import datetime
import collections
from urllib.parse import urlencode

from flask import Flask, render_template, url_for, send_from_directory
from flask_frozen import Freezer
import yaml
import jinja2
import markdown
import random

from elsa import cli
from functools import lru_cache

app = Flask('pyladies_cz')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_loader = jinja2.FileSystemLoader(['cities/', 'templates/'])

orig_path = os.path.join(app.root_path, 'original/')
v1_path = os.path.join(orig_path, 'v1/')
MISSING = object()

def redirect(url):
    """Return a response with a Meta redirect"""

    # With static pages, we can't use HTTP redirects.
    # Return a page wit <meta refresh> instead.
    #
    # When Frozen-Flask gets support for redirects
    # (https://github.com/Frozen-Flask/Frozen-Flask/issues/81),
    # this should be revisited.

    return render_template('meta_redirect.html', url=url)


########
## Views

@app.route('/')
def index():
    news = read_news_yaml('news.yml')
    partners = read_yaml('partners.yml')
    return render_template(
        'index.html', news=news, partners=partners,
        feedbacks=get_random_feedbacks(ttl=round(time.time() / 30)))  # cache for 30 secs


@app.route('/<city_slug>/')
def city(city_slug):
    cities = get_cities()
    city = cities.get(city_slug)
    if city is None:
        abort(404)
    meetups = read_meetups_yaml(os.path.join('cities', city_slug, 'meetups.yml'))
    current_meetups = [m for m in meetups if m['current']]
    past_meetups = [m for m in meetups if not m['current']]
    registration_meetups = [
        m for m in current_meetups if m.get('registration_status')=='running']
    return render_template(
        'city.html',
        city_slug=city_slug,
        city_title=city['title'],
        newsletter=city.get('newsletter'),
        current_meetups=current_meetups,
        past_meetups=past_meetups,
        registration_meetups=registration_meetups,
        contacts=city.get('contacts'),
        team=read_yaml(os.path.join('cities', city_slug, 'team.yml'), default=()),
    )

@app.route('/<city>_course/')
def course_redirect(city):
    return redirect(url_for('city', city_slug=city, _anchor='meetups'))

@app.route('/<city>_info/')
def info_redirect(city):
    return redirect(url_for('city', city_slug=city, _anchor='city-info'))

@app.route('/praha-cznic/')
def praha_cznic():
    return redirect('https://naucse.python.cz/2018/pyladies-praha-jaro-cznic/')

@app.route('/praha-ntk/')
def praha_ntk():
    return redirect('https://naucse.python.cz/2018/pyladies-praha-jaro-ntk/')

@app.route('/stan_se/')
def stan_se():
    return render_template('stan_se.html')

@app.route('/faq/')
def faq():
    return render_template('faq.html')

@app.route('/v1/<path:path>')
def v1(path):
    if path in REDIRECTS:
        return redirect(REDIRECTS[path])
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
## Template variables

@app.context_processor
def inject_cities():
    cities = {}
    for city_name, city_info in get_cities().items():
        meetups = read_meetups_yaml(f'cities/{city_name}/meetups.yml')
        meetups_nonpermanent = [m for m in meetups if m.get('start')]
        cities[city_name] = {
            **city_info,
            'active_registration': any(m.get('registration_status') == 'running' for m in meetups_nonpermanent),
        }
    return dict(cities=cities)


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


@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y'):
    return value.strftime(format)


def get_cities():
    """
    Returns {'cityY': <loaded_cityY_yaml_data>,
             'cityX': <loaded_cityX_yaml_data>,
             ...}
    by order specified in the YAML
    """

    cities_yamls = {d: os.path.join('cities', d, 'city.yml')
                    for d in os.listdir('cities')
                    if os.path.isdir(os.path.join('cities', d))}
    cities = {d: read_yaml(y) for d, y in cities_yamls.items()}
    cities_sorted = collections.OrderedDict(sorted(cities.items(), key=lambda x: x[1]['order']))
    return cities_sorted


@lru_cache(maxsize=1)
def get_random_feedbacks(n=3, ttl=None):
    """
    Returns list of n random feedbacks from various cities.

    This can be quite expensive when too many requests need to be handled (e.g. if used on index
    page), so let's provide some simple caching feature using `ttl' which would change
    e.g. once a 30 seconds or so, when calling this function.
    """

    cities = get_cities()
    feedbacks_yamls = {d: os.path.join('cities', d, 'feedbacks.yml')
                       for d in os.listdir('cities')
                       if os.path.isfile(os.path.join('cities', d, 'feedbacks.yml'))}
    city_feedbacks = {cities[d]['title']: read_yaml(y) for d, y in feedbacks_yamls.items()}
    feedbacks = list()
    for city_title, feedback_list in city_feedbacks.items():
        feedbacks.extend([(city_title, i) for i in feedback_list])
    random_feedbacks = random.sample(feedbacks, n)
    random.shuffle(random_feedbacks)
    random_feedbacks = [{'city-title': f[0], **f[1]} for f in random_feedbacks]
    return random_feedbacks


def read_yaml(filename, default=MISSING):
    try:
        file = open(filename, encoding='utf-8')
    except FileNotFoundError:
        if default is MISSING:
            raise
        return default
    with file:
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

        # If lesson has no `done` key, add them according to lesson dates
        # All lesson's dates must be in past to mark it as done
        done = lesson.get('done', None)
        if done is None and 'dates' in lesson:
            all_done = []
            for date in lesson['dates']:
                all_done.append(datetime.date.today() > date)
            lesson['done'] = all(all_done)

    return data


def read_meetups_yaml(filename):
    data = read_yaml(filename)

    if data is None:
        # Treat an empty YAML file as no courses.
        # (Otherwise, the file would have to contain [])
        data = []

    today = datetime.date.today()

    for meetup in data:
        # 'date' means both start and end
        if 'date' in meetup:
            meetup['start'] = meetup['date']
            meetup['end'] = meetup['date']

        # Derive a URL for places that don't have one from the location
        if 'place' in meetup:
            if ('url' not in meetup['place']
                    and {'latitude', 'longitude'} <= meetup['place'].keys()):
                place = meetup['place']
                place['url'] = 'http://mapy.cz/zakladni?' + urlencode({
                    'y': place['latitude'],
                    'x': place['longitude'],
                    'z': '16',
                    'id': place['longitude'] + ',' + place['latitude'],
                    'source': 'coor',
                    'q': place['name'],
                })

        # Figure out the status of registration
        if 'registration' in meetup:
            if 'start' in meetup and meetup['start'] <= today:
                meetup['registration_status'] = 'meetup_started'
            elif 'end' in meetup['registration'] and meetup['registration']['end'] < today:
                meetup['registration_status'] = 'closed'
            else:
                meetup['registration_status'] = 'running'

        meetup['current'] = ('end' not in meetup) or (meetup['end'] >= today)

    return list(reversed(data))

def read_news_yaml(filename):
    data = read_yaml(filename)
    today = datetime.date.today()
    news = []

    for new in data:
        if new['expires'] >= today:
            news.append(new)

    return news

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


############
## Redirects

REDIRECTS_DATA = read_yaml('redirects.yml')

REDIRECTS = {}
for directory, pages in REDIRECTS_DATA['naucse-lessons'].items():
    for html_filename, lesson in pages.items():
        new_url = 'http://naucse.python.cz/lessons/{}/'.format(lesson)
        REDIRECTS['{}/{}'.format(directory, html_filename)] = new_url


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
    for path in REDIRECTS:
        yield url_for('v1', path=path)

OLD_CITIES = 'praha', 'brno', 'ostrava'

@freezer.register_generator
def course_redirect():
    for city in OLD_CITIES:
        yield {'city': city}

@freezer.register_generator
def info_redirect():
    for city in OLD_CITIES:
        yield {'city': city}

if __name__ == '__main__':
    cli(app, freezer=freezer, base_url='http://pyladies.cz')
