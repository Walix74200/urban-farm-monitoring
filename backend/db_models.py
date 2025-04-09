from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, DateTime, Text, TIMESTAMP, ForeignKey, BigInteger, Boolean, String
from sqlalchemy.sql import func

Base = declarative_base()

class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(BigInteger, primary_key=True)
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"))
    version = Column(Text)
    last_seen = Column(TIMESTAMP(timezone=True), server_default=func.now())

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(BigInteger, ForeignKey("sensors.id", ondelete="CASCADE"))
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"))
    cycle_id = Column(Integer)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float)
    humidity = Column(Float)
    raw_data = Column(Text)
    analyzed = Column(Boolean, default=False)
    version = Column(String)  # ✅ Ajout de version ici

class Anomaly(Base):
    __tablename__ = "anomalies"
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(BigInteger, ForeignKey("sensors.id", ondelete="CASCADE"))
    plant_id = Column(Integer, ForeignKey("plants.id", ondelete="CASCADE"))
    cycle_id = Column(Integer)
    timestamp = Column(DateTime, nullable=False)
    type = Column(Text, nullable=False)
    details = Column(Text)
    severity = Column(Text)
