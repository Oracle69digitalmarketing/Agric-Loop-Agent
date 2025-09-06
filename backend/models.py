from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class FarmerInput(Base):
    __tablename__ = "farmer_inputs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    farmer_id = Column(String(255), index=True, nullable=False)

    # Use server_default for database-generated timestamps
    timestamp = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    input_type = Column(String(50), nullable=False)
    text_content = Column(Text, nullable=True)
    media_url = Column(String(2048), nullable=True)
    caption = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)

    def __repr__(self):
        return f"<FarmerInput(id={self.id}, farmer_id='{self.farmer_id}', type='{self.input_type}')>"
