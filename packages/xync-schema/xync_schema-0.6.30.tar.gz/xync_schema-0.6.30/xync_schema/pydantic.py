from pydantic import BaseModel


class FiatForm(BaseModel):
    cur_id: int
    pm_id: int
    user_id: int
    detail: str
    name: str | None = None
    amount: float
    target: int | None = None
