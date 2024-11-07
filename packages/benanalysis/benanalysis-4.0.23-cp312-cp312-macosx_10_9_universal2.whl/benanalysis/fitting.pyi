from __future__ import annotations
import benanalysis._benpy_core
__all__ = ['FitWavelengthParams', 'FitWavelengthParamsFree', 'fit_wavelength']
class FitWavelengthParams:
    """
    
    Holds parameters for the wavelength fitting function.
    
    :ivar d: Grating line distance (m).
    :vartype d: float
    :ivar omega_t: Angular frequency of the turret.
    :vartype omega_t: float
    :ivar omega_m: Angular frequency of the motor.
    :vartype omega_m: float
    :ivar cos_K: Cosine of the displacement angle.
    :vartype cos_K: float
    :ivar theta_z: Zero order angle.
    :vartype theta_z: float
    :ivar alpha: Alpha fit factor.
    :vartype alpha: float
    :ivar a: Turret error amplitude.
    :vartype a: float
    :ivar phi: Turret error phase.
    :vartype phi: float
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def a(self) -> float:
        """
        Turret error amplitude
        """
    @a.setter
    def a(self, arg0: float) -> None:
        ...
    @property
    def alpha(self) -> float:
        """
        Alpha fit factor
        """
    @alpha.setter
    def alpha(self, arg0: float) -> None:
        ...
    @property
    def cos_K(self) -> float:
        """
        Cosine of the displacement angle
        """
    @cos_K.setter
    def cos_K(self, arg0: float) -> None:
        ...
    @property
    def d(self) -> float:
        """
        Grating line distance
        """
    @d.setter
    def d(self, arg0: float) -> None:
        ...
    @property
    def omega_m(self) -> float:
        """
        Angular frequency of the motor
        """
    @omega_m.setter
    def omega_m(self, arg0: float) -> None:
        ...
    @property
    def omega_t(self) -> float:
        """
        Angular frequency of the turret
        """
    @omega_t.setter
    def omega_t(self, arg0: float) -> None:
        ...
    @property
    def phi(self) -> float:
        """
        Turret error phase
        """
    @phi.setter
    def phi(self, arg0: float) -> None:
        ...
    @property
    def theta_z(self) -> float:
        """
        Zero order angle
        """
    @theta_z.setter
    def theta_z(self, arg0: float) -> None:
        ...
class FitWavelengthParamsFree:
    """
    
    Flags indicating which parameters are available for fitting.
    
    :ivar d: Whether grating line distance is free to be fitted.
    :vartype d: bool
    :ivar omega_t: Whether angular frequency of the turret is free.
    :vartype omega_t: bool
    :ivar omega_m: Whether angular frequency of the motor is free.
    :vartype omega_m: bool
    :ivar cos_K: Whether cosine of the displacement angle is free.
    :vartype cos_K: bool
    :ivar theta_z: Whether zero order angle is free.
    :vartype theta_z: bool
    :ivar alpha: Whether alpha fit factor is free.
    :vartype alpha: bool
    :ivar a: Whether turret error amplitude is free.
    :vartype a: bool
    :ivar phi: Whether turret error phase is free.
    :vartype phi: bool
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def a(self) -> bool:
        """
        Whether turret error amplitude is free
        """
    @a.setter
    def a(self, arg0: bool) -> None:
        ...
    @property
    def alpha(self) -> bool:
        """
        Whether alpha fit factor is free
        """
    @alpha.setter
    def alpha(self, arg0: bool) -> None:
        ...
    @property
    def cos_K(self) -> bool:
        """
        Whether cosine of the displacement angle is free
        """
    @cos_K.setter
    def cos_K(self, arg0: bool) -> None:
        ...
    @property
    def d(self) -> bool:
        """
        Whether grating line distance is free to be fitted
        """
    @d.setter
    def d(self, arg0: bool) -> None:
        ...
    @property
    def omega_m(self) -> bool:
        """
        Whether angular frequency of the motor is free
        """
    @omega_m.setter
    def omega_m(self, arg0: bool) -> None:
        ...
    @property
    def omega_t(self) -> bool:
        """
        Whether angular frequency of the turret is free
        """
    @omega_t.setter
    def omega_t(self, arg0: bool) -> None:
        ...
    @property
    def phi(self) -> bool:
        """
        Whether turret error phase is free
        """
    @phi.setter
    def phi(self, arg0: bool) -> None:
        ...
    @property
    def theta_z(self) -> bool:
        """
        Whether zero order angle is free
        """
    @theta_z.setter
    def theta_z(self, arg0: bool) -> None:
        ...
def fit_wavelength(data: benanalysis._benpy_core.Scan, params: FitWavelengthParams, free: FitWavelengthParamsFree) -> bool:
    """
    Fits the grating equation to micro-step/wavelength data.
    
    :param data: The data used for the fit, mapping micro-step to wavelength.
    :type data: benanalysis.Scan
    :param params: Initial parameters for the fit. These values are adjusted during the fitting process.
    :type params: FitWavelengthParams
    :param free: Flags indicating which parameters are available for fitting.
    :type free: FitWavelengthParamsFree
    :return: ``True`` if the fitting is successful, ``False`` otherwise.
    :rtype: bool
    """
