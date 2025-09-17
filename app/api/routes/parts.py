
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.db import models
from app.schemas.pc import (
    CPUCreate, CPURead,
    MotherboardCreate, MotherboardRead,
    RAMKitCreate, RAMKitRead,
    GPUCreate, GPURead,
    PSUCreate, PSURead,
    CaseCreate, CaseRead,
)

router = APIRouter(prefix="/parts", tags=["parts"])


# ----- helpers ---------------------------------------------------------------

def _create(db: Session, model, data: dict):
    obj = model(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def _list(db: Session, model, limit: int, offset: int):
    q = db.query(model)
    items = q.order_by(model.id.desc()).limit(limit).offset(offset).all()
    total = q.count()
    return {"total": total, "items": items}


# ----- CPU -------------------------------------------------------------------

@router.post("/cpus", response_model=CPURead, status_code=201)
def create_cpu(
    p: CPUCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return _create(db, models.CPU, p.model_dump())


@router.get("/cpus", response_model=dict)
def list_cpus(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    res = _list(db, models.CPU, limit, offset)
    # serialize each ORM row through the Read schema to guarantee shape
    res["items"] = [CPURead.model_validate(x) for x in res["items"]]
    return res


# ----- Motherboard -----------------------------------------------------------

@router.post("/motherboards", response_model=MotherboardRead, status_code=201)
def create_motherboard(
    p: MotherboardCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return _create(db, models.Motherboard, p.model_dump())


@router.get("/motherboards", response_model=dict)
def list_motherboards(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    res = _list(db, models.Motherboard, limit, offset)
    res["items"] = [MotherboardRead.model_validate(x) for x in res["items"]]
    return res


# ----- RAMKit ----------------------------------------------------------------

@router.post("/ramkits", response_model=RAMKitRead, status_code=201)
def create_ramkit(
    p: RAMKitCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return _create(db, models.RAMKit, p.model_dump())


@router.get("/ramkits", response_model=dict)
def list_ramkits(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    res = _list(db, models.RAMKit, limit, offset)
    res["items"] = [RAMKitRead.model_validate(x) for x in res["items"]]
    return res


# ----- GPU -------------------------------------------------------------------

@router.post("/gpus", response_model=GPURead, status_code=201)
def create_gpu(
    p: GPUCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return _create(db, models.GPU, p.model_dump())


@router.get("/gpus", response_model=dict)
def list_gpus(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    res = _list(db, models.GPU, limit, offset)
    res["items"] = [GPURead.model_validate(x) for x in res["items"]]
    return res


# ----- PSU -------------------------------------------------------------------

@router.post("/psus", response_model=PSURead, status_code=201)
def create_psu(
    p: PSUCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return _create(db, models.PSU, p.model_dump())


@router.get("/psus", response_model=dict)
def list_psus(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    res = _list(db, models.PSU, limit, offset)
    res["items"] = [PSURead.model_validate(x) for x in res["items"]]
    return res


# ----- Case ------------------------------------------------------------------

@router.post("/cases", response_model=CaseRead, status_code=201)
def create_case(
    p: CaseCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    return _create(db, models.Case, p.model_dump())


@router.get("/cases", response_model=dict)
def list_cases(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    res = _list(db, models.Case, limit, offset)
    res["items"] = [CaseRead.model_validate(x) for x in res["items"]]
    return res
