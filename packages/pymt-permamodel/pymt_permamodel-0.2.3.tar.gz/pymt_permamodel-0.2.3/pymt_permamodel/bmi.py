from __future__ import absolute_import

import pathlib
import sys

from permamodel.components.bmi_frost_number import BmiFrostnumberMethod as FrostNumber
from permamodel.components.bmi_Ku import BmiKuModel as KuEnhanced
from permamodel.components.bmi_Ku_component import BmiKuMethod as Ku

if sys.version_info >= (3, 12):  # pragma: no cover (PY12+)
    import importlib.resources as importlib_resources
else:  # pragma: no cover (<PY312)
    import importlib_resources

FrostNumber.__name__ = "FrostNumber"
FrostNumber.METADATA = pathlib.Path(
    importlib_resources.files(__name__) / "data" / FrostNumber.__name__
)

Ku.__name__ = "Ku"
Ku.METADATA = pathlib.Path(importlib_resources.files(__name__) / "data" / Ku.__name__)

KuEnhanced.__name__ = "KuEnhanced"
KuEnhanced.METADATA = pathlib.Path(
    importlib_resources.files(__name__) / "data" / KuEnhanced.__name__
)

__all__ = [
    "FrostNumber",
    "Ku",
    "KuEnhanced",
]
