from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, Date

# We need to inherit Base in order to register models with SQLAlchemy
Base = declarative_base()


class Asteroid(Base):
    __tablename__ = 'asteroids'
    id = Column(Integer, primary_key=True)
    neo_reference_id = Column(Integer)
    name = Column(String)
    absolute_magnitude_h = Column(Float)
    estimated_diameter_min_meters = Column(Float)
    estimated_diameter_max_meters = Column(Float)
    is_potentially_hazardous_asteroid = Column(Boolean)
    close_approach_date = Column(Date)
    relative_velocity_kmph = Column(Float)
    miss_distance_km = Column(Float)
    load_date = Column(Date)

    def __repr__(self):
        return "<Asteroid(" \
               "id = {}" \
               ", neo_reference_id = {}" \
               ", name = '{}'" \
               ", absolute_magnitude_h = {}" \
               ", estimated_diameter_min_meters = {}" \
               ", estimated_diameter_max_meters = {}" \
               ", is_potentially_hazardous_asteroid = {}" \
               ", close_approach_date = {}" \
               ", relative_velocity_kmph = {}" \
               ", miss_distance_km = {}" \
               ", load_date = {}" \
               ")>".format(self.id, self.neo_reference_id, self.name, self.absolute_magnitude_h
                           , self.estimated_diameter_min_meters, self.estimated_diameter_max_meters
                           , self.is_potentially_hazardous_asteroid, self.close_approach_date
                           , self.relative_velocity_kmph, self.miss_distance_km, self.load_date)

