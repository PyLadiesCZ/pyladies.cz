
import os
import random
from sh import git, make, ghp_import, touch


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT_DIR, '_build', 'dirhtml')

COMMIT_EMOJIS = [
    ':sunglasses:', ':two_hearts:', ':sparkles:', ':star2:', ':star:',
    ':blue_heart: :yellow_heart:', ':raised_hands:', ':ok_hand:', ':ok_woman:',
    ':dancer:', ':raising_hand:', ':woman:', ':girl:', ':princess:', ':sunny:',
    ':cat:', ':koala:', ':snake:', ':paw_prints:', ':four_leaf_clover:',
    ':octocat:', ':gift_heart:', ':tada:', ':balloon:', ':cake:', ':rocket:',
]


def deploy():
    print('Generating HTML...')
    make('dirhtml')
    touch(os.path.join(OUTPUT_DIR, '.nojekyll'))

    if os.environ.get('TRAVIS'):  # Travis CI
        print('Setting up Git...')
        git.config('user.name', git('show', format='%cN', s=True))
        git.config('user.email', git('show', format='%cE', s=True))

        github_token = os.environ.get('GITHUB_TOKEN')  # encrypted in .travis.yml
        repo_slug = os.environ.get('TRAVIS_REPO_SLUG')
        origin = 'https://{}@github.com/{}.git'.format(github_token, repo_slug)
        git.remote('set-url', 'origin', origin)

    print('Rewriting gh-pages branch...')
    commit_message = 'Deploying {}'.format(random.choice(COMMIT_EMOJIS))
    ghp_import('-m', commit_message, OUTPUT_DIR)

    print('Pushing to GitHub...')
    git.push('origin', 'gh-pages:gh-pages', force=True)


if __name__ == '__main__':
    deploy()
