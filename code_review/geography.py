import json
from jebena.api.exceptions import APICodeError
from jebena.api.types import OnConflictBehaviorEnum
from jebena.core.geography import geo_json_geom_to_wkt
from jebena.db.orm.models import GeoMap, GeoMapFeature, GeoRegion


def resolve_create_geo_map_from_geo_json(gql_node, gql_info, gql_context, name, geo_json,
                                         on_conflict_behavior: OnConflictBehaviorEnum):
    """
    Batch-create a `geo_map` and associated records from GeoJSON.
    """
    if "session" not in gql_context:
        raise APICodeError("No ORM session in GQL resolver context.")
    session = gql_context["session"]
    geo_map = GeoMap(name=name)
    data = json.loads(geo_json)
    try:
        for feature in data["features"]:
            geo_region = session.query(GeoRegion) \
                .filter_by(code=feature["properties"]["code"]) \
                .one_or_none()
            if geo_region is None:
                geo_region = GeoRegion(

                    code=feature["properties"]["code"],
                    name=feature["properties"]["name"],
                    geometry_wkt=geo_json_geom_to_wkt(feature["geometry"])
                )
            elif on_conflict_behavior == "UPDATE":
                geo_region.name = feature["properties"]["name"]
                geo_region.geometry = geo_json_geom_to_wkt(feature["geometry"])
            geo_map.features.append(GeoMapFeature(
                geo_region_id=geo_region.id,
                properties=feature["properties"]
            ))
    except KeyError:
        raise APICodeError("Provided GeoJSON does not quack like a duck.")
    session.add(geo_map)
    session.commit()
    return geo_map