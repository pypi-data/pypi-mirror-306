from contentgrid_application_client import ContentGridApplicationClient, Profile
from contentgrid_hal_client.exceptions import NotFound
from fixtures import cg_client


def test_get_profile(cg_client: ContentGridApplicationClient):
    profile = cg_client.get_profile()
    assert type(profile) == Profile
    assert len(profile.get_entity_links()) > 0


def test_get_specific_profile(cg_client: ContentGridApplicationClient):
    profile = cg_client.get_profile()
    entity_profile = cg_client.get_entity_profile(
        profile.get_entity_links()[0].name
    )
    assert entity_profile.templates != None

    has_failed = False
    try:
        cg_client.get_entity_profile("fadlfjaklsdjfhkladsf")
    except NotFound as e:
        has_failed = True
    assert has_failed
