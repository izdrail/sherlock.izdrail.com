from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PocModel(Base):
    __tablename__ = "pocs"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    html_url = Column(String, nullable=True)
    description = Column(String, nullable=True)
    stargazers_count = Column(Integer, nullable=True)
    nvd_description = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    pushed_at = Column(DateTime, nullable=True)
