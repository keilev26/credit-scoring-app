import numpy as np
from models.request_models import ClienteIn
from utils.subgrade_mapper import convertir_subgrade_to_num

def preprocesar_cliente(cliente: ClienteIn) -> np.ndarray:
    sub_grade_num = convertir_subgrade_to_num(cliente.subgrade)

    # home_ownership one-hot: OWN, RENT  (OTHER → 0, 0)
    home_ownership_OWN  = 1 if cliente.home_ownership == "OWN"  else 0
    home_ownership_RENT = 1 if cliente.home_ownership == "RENT" else 0

    # purpose one-hot (10 categories; unlisted purpose → all zeros)
    purposes = [
        "credit_card", "debt_consolidation", "home_improvement", "house",
        "major_purchase", "medical", "moving", "other", "small_business", "vacation"
    ]
    purpose_encoded = [1 if cliente.purpose == p else 0 for p in purposes]

    # verification_status one-hot: Source Verified, Verified  (Not Verified → 0, 0)
    vs_source_verified = 1 if cliente.verification_status == "Source Verified" else 0
    vs_verified        = 1 if cliente.verification_status == "Verified"        else 0

    registro = np.array([
        cliente.loan_amnt,
        cliente.total_acc,
        cliente.revol_util,
        cliente.revol_bal,
        cliente.pub_rec,
        cliente.open_acc,
        cliente.dti,
        cliente.mort_acc,
        cliente.pub_rec_bankruptcies,
        cliente.installment,
        cliente.int_rate,
        cliente.annual_inc,
        cliente.emp_length,
        cliente.term,
        sub_grade_num,
        home_ownership_OWN,
        home_ownership_RENT,
        *purpose_encoded,
        vs_source_verified,
        vs_verified,
    ], dtype=float)

    return registro
