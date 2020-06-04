import pytest
import yaml

# workaroud fixture within parametrize call
from tests.conftest import feedbacks_yamls_dict


def test_min_number_of_feedbacks(feedbacks, n=3):
    """
    Check that we have at least n feedbacks to be able to display
    pages properly.
    """
    assert len(feedbacks) >= n


@pytest.mark.parametrize('city', feedbacks_yamls_dict)
def test_feedbacks_yml_loading(city):
    feedback_yml = feedbacks_yamls_dict[city]
    with open(feedback_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)
