from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer,ForeignKey("user_details.user_id", ondelete="CASCADE"),nullable=False)

    token = Column(String, unique=True, nullable=False)

    expires_at = Column(DateTime, nullable=False)

    is_revoked = Column(Boolean, default=False)

    user = relationship("User",back_populates="refresh_tokens")