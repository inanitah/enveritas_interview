import json
from jebena.api.exceptions import APICodeError
from jebena.api.types import OnConflictBehaviorEnum
from jebena.core.geography import geo_json_geom_to_wkt
from jebena.db.orm.models import GeoMap, GeoMapFeature, GeoRegion


# Mike: It would be beneficial to receive a clear use case and an explanation of what this function aims to achieve.
# Additionally, referencing the associated tests and explaining why this specific implementation was chosen would provide valuable context.

# It seems gql_node and gql_info are not used in this function.
# It would be cleaner to only receive the parameters that are actually needed.
# Using type hints and encapsulating the input data in a request data class can enhance readability and maintainability.
# Example: GeoMapCreationRequest(gql_context, name, geo_json, on_conflict_behavior)
# The name resolve_create_geo_map_from_geo_json could be more descriptive. A suggestion could be create_geo_map_from_geo_json.
# Each function should have a single responsibility. Currently, this function mixes business logic with database integration.
# Also, consider creating unit tests for this code and dividing the implementation between the service layer and repository like this:
# class GeoMapCreator:
# def __init__(self, repository: GeoMapRepository):
#   self.repository = repository
# All database interactions can be managed through the repository, making the code simpler to test without directly patching the database.
# This approach also helps separate the implementation of the service layer and persistence layer.

def resolve_create_geo_map_from_geo_json(gql_node, gql_info, gql_context, name, geo_json,
                                         on_conflict_behavior: OnConflictBehaviorEnum):
    # Mike: Consider adding a more detailed docstring to describe the function's purpose and behavior. For example:
    # This function processes the geo_json input to create a geo_map and its associated features. It validates the input,
    # retrieves existing regions from the database, creates new regions if necessary, and stores the geo_map in the database.
    """
    Batch-create a `geo_map` and associated records from GeoJSON.
    """
    if "session" not in gql_context:
        # Mike: Is APICodeError the best choice here? It might be more appropriate to use a validation exception like ValidateException.
        # This validation could also be handled outside the function to ensure parameters are validated before processing.
        # Example: validate_gql_session(gql_context)
        raise APICodeError("No ORM session in GQL resolver context.")

    session = gql_context["session"]
    geo_map = GeoMap(name=name)

    # Mike: Adding validation for geo_json input can prevent potential issues later on.
    # For example:
    # try:
    #     data = json.loads(geo_json)
    # except JSONDecodeError:
    #     raise ValidateException("Can't decode geo_json, exiting the function")

    data = json.loads(geo_json)
    try:
        # Ensure that the data contains 'features' or handle it accordingly like this: data.get("features", []).

        for feature in data["features"]:
            # Mike: Retrieving all GeoRegions before the loop can reduce database interaction.
            # Here’s an approach:
            # Step 1: Extract all unique codes from the GeoJSON features.
            # codes = {feature["properties"]["code"] for feature in data["features"]}
            #
            # Step 2: Retrieve all GeoRegion records with those codes in a single query.
            # existing_geo_regions = session.query(GeoRegion).filter(GeoRegion.code.in_(codes)).all()
            #
            # Step 3: Create a dictionary of these GeoRegion records for fast lookup.
            # geo_region_dict = {region.code: region for region in existing_geo_regions}
            # Then retrieve the geo_region with:
            # code = feature["properties"]["code"]
            # geo_region = geo_region_dict.get(code)
            # Encapsulating this functionality into a helper function can also improve clarity.
            # geo_region = get_geo_region_from_db(session, on_conflict_behavior)

            geo_region = session.query(GeoRegion) \
                .filter_by(code=feature["properties"]["code"]) \
                .one_or_none()
            # Mike: In both cases inside the if statement, the geo_region is not being saved to the database.
            if geo_region is None:
                # Mike: It’s good practice to validate the feature before processing.
                # Adding a validator for the feature can help manage invalid data more gracefully.
                # For example:
                # try:
                #     validate_feature(feature)
                # except ValidationFeatureException:
                #     logger.warning('The feature is not valid', {'feature': feature})
                #     continue
                # Also, validating the 'geometry' part of the feature is crucial:
                # try:
                #     geo_geometry = geo_json_geom_to_wkt(feature["geometry"])
                # except Exception:
                #     logger.warning('The geometry in the feature is not valid, continuing', {'feature': feature})
                #     continue
                # Committing the creation of the geo_region ensures its ID is available for geo_map creation.
                geo_region = GeoRegion(
                    code=feature["properties"]["code"],
                    name=feature["properties"]["name"],
                    geometry_wkt=geo_json_geom_to_wkt(feature["geometry"])
                )
            # Mike: Consider using the enum value for consistency.
            # elif on_conflict_behavior == OnConflictBehaviorEnum.UPDATE.value

            elif on_conflict_behavior == "UPDATE":
                geo_region.name = feature["properties"]["name"]
                geo_region.geometry_wkt = geo_json_geom_to_wkt(feature["geometry"])

            geo_map.features.append(GeoMapFeature(
                geo_region_id=geo_region.id,
                properties=feature["properties"]
            ))
    except KeyError:
        # Mike: While the message is descriptive, we could consider a more specific exception.
        raise APICodeError("Provided GeoJSON does not contain the expected features.")

    # Mike: Adding a try-except block around the commit operation can help handle potential commit failures gracefully.
    session.add(geo_map)
    session.commit()
    return geo_map
