from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.db import models
from app.schemas.pc import BuildCreate, BuildRead, BuildValidation, RuleResult

router = APIRouter(prefix="/builds", tags=["builds"])

@router.post("/", response_model=BuildRead, status_code=201)
def create_build(p: BuildCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    refs = {
        "cpu": db.get(models.CPU, p.cpu_id),
        "motherboard": db.get(models.Motherboard, p.motherboard_id),
        "ramkit": db.get(models.RAMKit, p.ramkit_id),
        "gpu": db.get(models.GPU, p.gpu_id),
        "psu": db.get(models.PSU, p.psu_id),
        "case": db.get(models.Case, p.case_id),
    }
    if any(v is None for v in refs.values()):
        raise HTTPException(status_code=400, detail="One or more part IDs not found")
    build = models.Build(owner_id=user.id, **p.dict())
    db.add(build); db.commit(); db.refresh(build)
    return build

@router.get("/", response_model=dict)
def list_builds(db: Session = Depends(get_db), user: models.User = Depends(get_current_user),
                limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
    q = db.query(models.Build).filter(models.Build.owner_id == user.id)
    items = q.order_by(models.Build.created_at.desc()).limit(limit).offset(offset).all()
    return {"total": q.count(), "items": [BuildRead.model_validate(x) for x in items]}

@router.get("/{build_id}/validate", response_model=BuildValidation)
def validate_build(build_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    b = db.query(models.Build).filter(models.Build.id == build_id, models.Build.owner_id == user.id).first()
    if not b: raise HTTPException(status_code=404, detail="Build not found")
    cpu, mb, ram, gpu, psu, case = b.cpu, b.motherboard, b.ramkit, b.gpu, b.psu, b.case

    rules = []
    rules.append(RuleResult(rule="cpu_socket", ok=(cpu.socket == mb.socket), message=f"{cpu.socket} vs {mb.socket}"))
    supported = set(x.strip() for x in case.supported_form_factors.split(","))
    rules.append(RuleResult(rule="form_factor", ok=(mb.form_factor in supported), message=f"{mb.form_factor} in {supported}"))
    rules.append(RuleResult(rule="ram_type", ok=(ram.ram_type == mb.ram_type), message=f"{ram.ram_type} vs {mb.ram_type}"))
    rules.append(RuleResult(rule="ram_speed", ok=(ram.speed_mts <= mb.ram_max_mts), message=f"{ram.speed_mts} <= {mb.ram_max_mts}"))
    rules.append(RuleResult(rule="gpu_length", ok=(gpu.length_mm <= case.gpu_max_length_mm), message=f"{gpu.length_mm} <= {case.gpu_max_length_mm}"))

    total_power = cpu.tdp_w + gpu.tdp_w + 100
    ok_power = psu.wattage_w >= total_power
    rules.append(RuleResult(rule="psu_wattage", ok=ok_power, message=f"{psu.wattage_w} >= {total_power} (cpu+gpu+100)"))

    return BuildValidation(passed=all(r.ok for r in rules),
                           rules=rules,
                           summary={"total_power": total_power, "psu_wattage": psu.wattage_w, "headroom_w": psu.wattage_w - total_power})
