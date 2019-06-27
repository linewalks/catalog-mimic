from catalog.cardio.model.base import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from catalog.cardio.model.d_events import DEvents


class CardioEvents(Base):
    __tablename__ = "cardio_events"
    __table_args__ = {"schema": "analysis"}

    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer)
    ts = Column(TIMESTAMP)
    event_id = Column(Integer, ForeignKey(DEvents.event_id))
    event_value = Column(String(100))

    d_events = relationship("DEvents", backref="cardio_events")

    def __init__(self, subject_id, ts, event_id, event_value):
        self.subject_id = subject_id
        self.ts = ts
        self.event_id = event_id
        self.event_value = event_value
