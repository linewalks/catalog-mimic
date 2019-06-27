from catalog.cardio.model.base import Base
from sqlalchemy import Column, String, Integer


class DEvents(Base):
    __tablename__ = "d_events"
    __table_args__ = {"schema": "analysis"}

    event_id = Column(Integer, primary_key=True)
    category = Column(String(100))
    event_code = Column(String(100))
    event_name = Column(String(500))
    event_unit = Column(String(100))
    standard_code = Column(String(100))

    def __init__(self, event_id, category, event_code, event_name, event_unit, standard_code):
        self.event_id = event_id
        self.category = category
        self.event_code = event_code
        self.event_name = event_name
        self.event_unit = event_unit
        self.standard_code = standard_code
