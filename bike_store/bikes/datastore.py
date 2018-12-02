from django.conf import settings
from google.cloud import datastore


def get_client():
    return datastore.Client(settings.PROJECT_ID)


def from_datastore(entity):
    """Translates Datastore results into the format expected by the
    application.
    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]
    This returns:
        {id: id, prop: val, ...}
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()

    entity['id'] = entity.key.id
    return entity


def list_instances(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='bike', order=[])
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor


def get_instance(id):
    ds = get_client()
    key = ds.key('bike', int(id))
    results = ds.get(key)
    return from_datastore(results)


def create_update_instance(data, id=None):
    ds = get_client()
    if id:
        key = ds.key('bike', int(id))
    else:
        key = ds.key('bike')

    entity = datastore.Entity(
        key=key,
        exclude_from_indexes=('price', ))

    entity.update(data)
    ds.put(entity)
    return from_datastore(entity)


def delete_instance(id):
    ds = get_client()
    key = ds.key('bike', int(id))
    ds.delete(key)
