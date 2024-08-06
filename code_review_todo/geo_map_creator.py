import json
import logging
from typing import Dict, Set
from jebena.api.exceptions import APICodeError, ValidationFeatureException, ValidateException
from jebena.api.types import OnConflictBehaviorEnum
from jebena.core.geography import geo_json_geom_to_wkt
from jebena.db.orm.models import GeoMap, GeoMapFeature, GeoRegion

logger = logging.getLogger(__name__)


class GeoMapRepository:
    def get_geo_regions_by_codes(self, codes: Set[str]) -> Dict[str, GeoRegion]:
        # Need to be implemented
        pass

    def add_geo_region(self, geo_region: GeoRegion) -> GeoRegion:
        # Need to be implemented
        pass

    def add_geo_map(self, geo_map: GeoMap) -> None:
        # Need to be implemented
        pass


class GeoMapCreator:
    def __init__(self, repository: GeoMapRepository):
        self.repository = repository

    def validate_geojson(self, geo_json: str) -> dict:
        try:
            data = json.loads(geo_json)
        except json.JSONDecodeError:
            raise ValidateException("Invalid GeoJSON format.")
        if 'features' not in data:
            raise ValidateException("GeoJSON must contain features.")
        return data

    def validate_feature(self, feature: dict) -> None:
        if 'properties' not in feature or 'code' not in feature['properties'] or 'name' not in feature['properties']:
            raise ValidationFeatureException("Invalid feature format.")
        if 'geometry' not in feature:
            raise ValidationFeatureException("Feature must contain geometry.")

    def get_geo_regions(self, codes: Set[str]) -> Dict[str, GeoRegion]:
        return self.repository.get_geo_regions_by_codes(codes)

    def get_geo_region(
            self, feature: dict, geo_region_dict: Dict[str, GeoRegion],
            on_conflict_behavior: OnConflictBehaviorEnum
    ) -> GeoRegion:

        code = feature["properties"]["code"]
        geo_region = geo_region_dict.get(code)

        if geo_region is None:
            try:
                geo_region = GeoRegion(
                    code=code,
                    name=feature["properties"]["name"],
                    geometry_wkt=geo_json_geom_to_wkt(feature["geometry"])
                )
                geo_region = self.repository.add_geo_region(
                    geo_region)  # Ensure the returned geo_region contains the ID
                geo_region_dict[code] = geo_region
            except Exception as e:
                logger.warning('Failed to process geometry in feature', {'feature': feature, 'error': str(e)})
                raise APICodeError("Failed to process GeoRegion geometry.")
        elif on_conflict_behavior == OnConflictBehaviorEnum.UPDATE:
            geo_region.name = feature["properties"]["name"]
            geo_region.geometry_wkt = geo_json_geom_to_wkt(feature["geometry"])

        return geo_region

    def create_geo_map(self, name: str, geo_json: str, on_conflict_behavior: OnConflictBehaviorEnum) -> GeoMap:
        logger.info("Starting the creation of GeoMap")
        data = self.validate_geojson(geo_json)
        geo_map = GeoMap(name=name)

        codes = {feature["properties"]["code"] for feature in data["features"]}
        geo_region_dict = self.get_geo_regions(codes)

        try:
            for feature in data["features"]:
                self.validate_feature(feature)
                geo_region = self.get_geo_region(feature, geo_region_dict, on_conflict_behavior)
                geo_map.features.append(GeoMapFeature(
                    geo_region_id=geo_region.id,
                    properties=feature["properties"]
                ))
        except (KeyError, ValidationFeatureException) as e:
            logger.warning('Invalid feature encountered', {'error': str(e)})
            raise APICodeError(f"Provided GeoJSON does not contain valid feature data: {e}")

        try:
            self.repository.add_geo_map(geo_map)
        except Exception as e:
            logger.error('Failed to commit GeoMap', {'error': str(e)})
            raise APICodeError(f"Failed to create GeoMap: {e}")

        logger.info("Finished the creation of GeoMap")
        return geo_map
