from contentgrid_application_client import ContentGridApplicationClient, EntityCollection, EntityObject
from fixtures import cg_client

def test_get_collection(cg_client: ContentGridApplicationClient):
    profile = cg_client.get_profile()
    entity_name = profile.get_entity_links()[0].name
    collection_response = cg_client.get_entity_collection(entity_name)

    assert type(collection_response) == EntityCollection
    assert collection_response.page_info != None
    assert collection_response.page_info.total_elements >= 0
    assert collection_response.embedded != None
    assert collection_response.links != None


def test_get_entity(cg_client: ContentGridApplicationClient):
    collection_response = cg_client.get_entity_collection(plural_entity_name="skills")

    if collection_response.page_info.total_elements > 0:
        for hal_object in collection_response.get_entities():
            assert type(hal_object) == EntityObject
            assert hal_object.id != None

        example_entity_link = collection_response.get_entities()[0].get_self_link()
        entity_object = cg_client.get_entity_instance(entity_link=example_entity_link)

        assert type(entity_object) == EntityObject
        assert entity_object.id != None
        assert len(entity_object.metadata.keys()) > 0

    if collection_response.page_info.total_pages > 0:
        collection_response.first()
        collection_response.next()
        collection_response.prev()
        collection_response.last()
        assert type(collection_response) == EntityCollection