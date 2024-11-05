"""OpenDAP Catalog Data classes."""

from __future__ import annotations

from typing import Optional, Dict, Any

# from typing import Tuple

import numpy as np
from pydantic import BaseModel
from pydantic import validator, root_validator


class CatClimRItem(BaseModel):
    """Mike Johnson's CatClimRItem class.

    Source data from which this is derived comes from:
        'https://github.com/mikejohnson51/climateR-catalogs/releases/download/June-2024/catalog.parquet'
    """

    id: Optional[str] = None
    asset: Optional[str] = None
    URL: str
    varname: str
    long_name: Optional[str] = None  # type: ignore
    variable: Optional[str] = None
    description: Optional[str] = None
    units: Optional[str] = None
    model: Optional[str] = None
    ensemble: Optional[str] = None
    scenario: Optional[str] = None
    T_name: Optional[str] = None
    duration: Optional[str] = None
    interval: Optional[str] = None
    nT: Optional[int] = 0  # noqa
    X_name: str  # noqa
    Y_name: str  # noqa
    X1: Optional[float] = None
    Xn: Optional[float] = None
    Y1: Optional[float] = None
    Yn: Optional[float] = None
    resX: float  # noqa
    resY: float  # noqa
    ncols: Optional[int] = None
    nrows: Optional[int] = None
    proj: Optional[str] = None
    toptobottom: str
    tiled: Optional[str] = None
    crs: Optional[str] = None

    @root_validator(pre=False)
    @classmethod
    def set_default_long_name(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Sets long_name to asset value if long_name is None or empty."""
        if not values.get("long_name"):
            values["long_name"] = values.get("description", "None")
        return values

    @validator("crs", pre=True, always=True)
    @classmethod
    def _default_crs(cls, val: str, values: str) -> str:
        """Sets to a default CRS if none is provided."""
        if val is None or not val:
            if "proj" in values:
                return values["proj"]
            if "proj" not in values:
                return "EPSG:4326"
        else:
            return val

    @validator("proj", pre=True, always=True)
    @classmethod
    def _default_proj(cls, val: str, values: str) -> str:
        """Sets to a default PROJ if none is provided."""
        if val is None or not val:
            if "crs" in values:
                return values["crs"]
            if "crs" not in values:
                return "EPSG:4326"
        else:
            return val

    @validator("nT", pre=True, always=False)
    @classmethod
    def set_nt(cls, v: int) -> int:  # noqa:
        """Convert to int."""
        return 0 if np.isnan(v) else v

    @validator("toptobottom", always=False)
    @classmethod
    def _toptobottom_as_bool(cls, val: str) -> bool:
        """Convert to python boolean type."""
        return val.upper() == "TRUE"  # type: ignore

    @validator("tiled", always=False)
    @classmethod
    def _tiled(cls, val: str) -> str:
        """Must be one of just a few options.  Returns NA if left blank."""
        if val.upper() not in ["", "NA", "T", "XY"]:
            raise ValueError("tiled must be one of ['', 'NA', 'T', 'XY']")
        if val == "":
            return "NA"
        return val.upper()

    class Config:
        """interior class to direct pydantic's behavior."""

        anystr_strip_whitespace = True
        allow_mutations = False
