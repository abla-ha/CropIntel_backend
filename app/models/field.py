from sqlalchemy import Column, Integer, String, Float, Date
from app.core.database import Base


class CropField(Base):
    __tablename__ = 'crop_fields'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)  
    field_name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    area = Column(Float, nullable=False) 
    harvest_date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<CropField(user_id={self.user_id}, field_name='{self.field_name}', location='{self.location}', area={self.area}, harvest_date='{self.harvest_date}')>"
