from pydantic import BaseModel

class ClienteIn(BaseModel):
    name: str | None = None
    email: str | None = None
    phoneNum: str | None = None

    loan_amnt: float
    term : int
    int_rate: float
    installment : float
    subgrade: str
    emp_length : int
    home_ownership : str
    annual_inc: float
    verification_status : str
    purpose: str
    dti: float
    open_acc: int
    pub_rec: int
    revol_bal:float
    revol_util:float
    total_acc:int
    mort_acc:int
    pub_rec_bankruptcies:int