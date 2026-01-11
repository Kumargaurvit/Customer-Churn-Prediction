from pydantic import BaseModel, Field
from typing import Literal, Annotated

class UserInput(BaseModel):
    CreditScore: Annotated[int, Field(..., description="Credit Score", ge=0, le=900)]
    Geography: Annotated[Literal["France","Spain","Germany"], Field(..., description="Country")]
    Gender: Annotated[Literal["Male","Female"], Field(..., description="Gender")]
    Age: Annotated[int, Field(..., description="Age", ge=0, le=100)]
    Tenure: Annotated[int, Field(..., description="Tenure", ge=0, le=10)]
    Balance: Annotated[float, Field(..., description="Account Balance", ge=0)]
    NumOfProducts: Annotated[int, Field(..., description="Number of Products", ge=0, le=10)]
    HasCrCard: Annotated[int, Field(..., description="Credit Card", ge=0, le=1)]
    IsActiveMember: Annotated[int, Field(..., description="Active Member", ge=0, le=1)]
    EstimatedSalary: Annotated[float, Field(..., description="Estimated Salary", ge=0)]