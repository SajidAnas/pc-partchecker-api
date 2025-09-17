from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

class CPU(Base):
    __tablename__ = "cpus"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    socket: Mapped[str] = mapped_column(String(50), nullable=False)
    tdp_w: Mapped[int] = mapped_column(Integer, nullable=False)

class Motherboard(Base):
    __tablename__ = "motherboards"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    socket: Mapped[str] = mapped_column(String(50), nullable=False)
    form_factor: Mapped[str] = mapped_column(String(10), nullable=False)  
    ram_type: Mapped[str] = mapped_column(String(10), nullable=False)     
    ram_max_mts: Mapped[int] = mapped_column(Integer, nullable=False)

class RAMKit(Base):
    __tablename__ = "ram_kits"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    ram_type: Mapped[str] = mapped_column(String(10), nullable=False)
    speed_mts: Mapped[int] = mapped_column(Integer, nullable=False)
    size_gb: Mapped[int] = mapped_column(Integer, nullable=False)
    sticks: Mapped[int] = mapped_column(Integer, nullable=False)

class GPU(Base):
    __tablename__ = "gpus"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    length_mm: Mapped[int] = mapped_column(Integer, nullable=False)
    tdp_w: Mapped[int] = mapped_column(Integer, nullable=False)

class PSU(Base):
    __tablename__ = "psus"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    wattage_w: Mapped[int] = mapped_column(Integer, nullable=False)

class Case(Base):
    __tablename__ = "cases"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    supported_form_factors: Mapped[str] = mapped_column(String(50), nullable=False)  # CSV
    gpu_max_length_mm: Mapped[int] = mapped_column(Integer, nullable=False)

class Build(Base):
    __tablename__ = "builds"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    cpu_id: Mapped[int] = mapped_column(ForeignKey("cpus.id"), nullable=False)
    motherboard_id: Mapped[int] = mapped_column(ForeignKey("motherboards.id"), nullable=False)
    ramkit_id: Mapped[int] = mapped_column(ForeignKey("ram_kits.id"), nullable=False)
    gpu_id: Mapped[int] = mapped_column(ForeignKey("gpus.id"), nullable=False)
    psu_id: Mapped[int] = mapped_column(ForeignKey("psus.id"), nullable=False)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    owner = relationship("User")
    cpu = relationship("CPU")
    motherboard = relationship("Motherboard")
    ramkit = relationship("RAMKit")
    gpu = relationship("GPU")
    psu = relationship("PSU")
    case = relationship("Case")
