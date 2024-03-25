from .database import Base
from sqlalchemy import Column, String, DateTime
from utils.utils import time_to_end


class SecretModel(Base):
    __tablename__ = "Secrets"

    secret_key = Column(String, unique=True, nullable=False, primary_key=True)
    secret_data = Column(String, nullable=True)
    elapsed_at = Column(DateTime(timezone=True), nullable=False, default=time_to_end)
