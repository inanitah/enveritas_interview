class GeoMap(Base):
    __tablename__ = "geo_map"
    id = Column(UUID, primary_key=True, server_default=FetchedValue())
    name = Column(Text, nullable=False)
    features = relationship(lambda: GeoMapFeature, back_populates="geo_map")


class GeoMapFeature(Base):
    __tablename__ = "geo_map_feature"
    id = Column(UUID, primary_key=True, server_default=FetchedValue())
    geo_map_id = Column(UUID, ForeignKey("geo_map.id"), nullable=False)


geo_region_id = Column(UUID, ForeignKey("geo_region.id"), nullable=False)
properties = Column(JSONB, nullable=True)
geo_map = relationship(lambda: GeoMap, back_populates="features")
geo_region = relationship(lambda: GeoRegion)


class GeoRegion(Base):
    __tablename__ = "geo_region"
    id = Column(UUID, primary_key=True, server_default=FetchedValue())
    code = Column(Text, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    geometry_wkt = Column(Text, nullable=False)