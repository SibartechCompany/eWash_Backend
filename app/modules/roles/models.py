import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Role(Base):
  __tablename__ = "role"

  id_role=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
  name=Column(String, nullable=False)
  description=Column(String, nullable=False)
