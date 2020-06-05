import yaml


def test_feedbacks_yml_loading(feedbacks_for_city):
    city, feedback_yml = feedbacks_for_city
    with open(feedback_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)


def test_min_number_of_feedbacks(feedbacks_all, n=3):
    """
    Check that we have at least n feedbacks to be able to display
    index page properly.
    """
    feedbacks = []
    for feedback_yml in feedbacks_all.values():
        with open(feedback_yml) as f:
            feedbacks.extend(yaml.load(f.read(), Loader=yaml.SafeLoader))
    assert len(feedbacks) >= n


def test_max_content_length_of_feedbacks(feedbacks_for_city):
    city, feedback_yml = feedbacks_for_city
    with open(feedback_yml) as f:
        feedbacks = yaml.load(f.read(), Loader=yaml.SafeLoader)
    for f in feedbacks:
        assert len(f['content']) < 1000
