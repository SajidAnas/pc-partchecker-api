from pydantic import BaseModel, Field

class CPUCreate(BaseModel):
    name: str; socket: str
    tdp_w: int = Field(ge=1)
class CPURead(CPUCreate):
    id: int
    class Config: from_attributes = True

class MotherboardCreate(BaseModel):
    name: str; socket: str; form_factor: str; ram_type: str; ram_max_mts: int
class MotherboardRead(MotherboardCreate):
    id: int
    class Config: from_attributes = True

class RAMKitCreate(BaseModel):
    name: str; ram_type: str; speed_mts: int; size_gb: int; sticks: int
class RAMKitRead(RAMKitCreate):
    id: int
    class Config: from_attributes = True

class GPUCreate(BaseModel):
    name: str; length_mm: int; tdp_w: int
class GPURead(GPUCreate):
    id: int
    class Config: from_attributes = True

class PSUCreate(BaseModel):
    name: str; wattage_w: int
class PSURead(PSUCreate):
    id: int
    class Config: from_attributes = True

class CaseCreate(BaseModel):
    name: str; supported_form_factors: str; gpu_max_length_mm: int
class CaseRead(CaseCreate):
    id: int
    class Config: from_attributes = True

class BuildCreate(BaseModel):
    cpu_id: int; motherboard_id: int; ramkit_id: int; gpu_id: int; psu_id: int; case_id: int
class BuildRead(BuildCreate):
    id: int
    class Config: from_attributes = True

class RuleResult(BaseModel):
    rule: str; ok: bool; message: str
class BuildValidation(BaseModel):
    passed: bool; rules: list[RuleResult]; summary: dict
