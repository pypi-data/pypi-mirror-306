from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, ValidationError

from red_wine_mm.config.core import config


def validate_inputs(*, input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""

    validated_data = input_data[config.m_config.features].copy()
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleTitanicDataInputs(
            inputs=validated_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return validated_data, errors


class WineDataInputSchema(BaseModel):
    fixed_acidity: Optional[float] = Field(alias="fixed acidity")
    volatile_acidity: Optional[float] = Field(alias="volatile acidity")
    chlorides: Optional[float]
    free_sulfur_dioxide: Optional[float] = Field(alias="free sulfur dioxide")
    total_sulfur_dioxide: Optional[float] = Field(alias="total sulfur dioxide")
    sulphates: Optional[float]
    alcohol: Optional[float]


class MultipleTitanicDataInputs(BaseModel):
    inputs: List[WineDataInputSchema]
