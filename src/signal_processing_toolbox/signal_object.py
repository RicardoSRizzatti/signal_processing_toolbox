# %%
"""
Signal object
"""
from typing import Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
import numpy as np

class Signal(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    data_signal: np.ndarray
    sampling_rate: int = Field(..., ge=1)
    physical_unit: str
    physical_name: str
    name: str
    samples: Optional[int] = 0
    duration: Optional[float] = 0
    sample_period: Optional[float] = 0
    freq_max: Optional[float] = 0
    freq_resolution: Optional[float] = 0
    
    @field_validator('data_signal')
    def dimension_data_signal_validation(cls,v):
        if v.ndim != 1:
            raise ValueError('This data have to be a 1D array.')
        else:
            return v
        
    def model_post_init(self, __context: Any) -> None:
        self.samples = self.data_signal.shape[0]
        self.duration= self.samples/self.sampling_rate
        self.sample_period= 1/self.sampling_rate
        self.freq_max= self.sampling_rate/2
        self.freq_resolution= 1/self.duration
        return super().model_post_init(__context)
