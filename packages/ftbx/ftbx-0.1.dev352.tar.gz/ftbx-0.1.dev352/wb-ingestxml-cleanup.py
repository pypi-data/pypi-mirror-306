from src._objects import ObjectType, Objects, SubItems


xmls = Objects(
    object_type=ObjectType.ASSETS,
    sub_items=['parent'],
    filters={"name": "ingest.xml"},
    mode="full"
)
