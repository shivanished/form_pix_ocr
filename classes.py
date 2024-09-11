from pydantic import BaseModel


class CarrierRequest(BaseModel):
    mc_number: str