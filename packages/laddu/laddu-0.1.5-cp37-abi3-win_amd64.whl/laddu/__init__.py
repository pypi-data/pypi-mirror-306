from abc import ABCMeta, abstractmethod

from laddu.amplitudes import Manager, constant, parameter
from laddu.amplitudes.breit_wigner import BreitWigner
from laddu.amplitudes.common import ComplexScalar, PolarComplexScalar, Scalar
from laddu.amplitudes.ylm import Ylm
from laddu.amplitudes.zlm import Zlm
from laddu.convert import convert_from_amptools
from laddu.data import BinnedDataset, Dataset, open
from laddu.likelihoods import NLL, LikelihoodManager, Status
from laddu.utils.variables import Angles, CosTheta, Mass, Phi, PolAngle, Polarization, PolMagnitude
from laddu.utils.vectors import Vector3, Vector4

from . import amplitudes, convert, data, likelihoods, utils
from .laddu import version

__version__ = version()


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def callback(self, step: int, status: Status) -> tuple[Status, bool]:
        pass


__all__ = [
    "__version__",
    "convert",
    "convert_from_amptools",
    "Dataset",
    "open",
    "BinnedDataset",
    "utils",
    "data",
    "amplitudes",
    "likelihoods",
    "Vector3",
    "Vector4",
    "CosTheta",
    "Phi",
    "Angles",
    "PolMagnitude",
    "PolAngle",
    "Polarization",
    "Mass",
    "Manager",
    "LikelihoodManager",
    "NLL",
    "Status",
    "Observer",
    "parameter",
    "constant",
    "Scalar",
    "ComplexScalar",
    "PolarComplexScalar",
    "Ylm",
    "Zlm",
    "BreitWigner",
]
