#
# Bulter volmer class
#

import pybamm
from ..base_interface import BaseInterface


class NoReaction(BaseInterface):
    """
    Base submodel for when no reaction occurs

    Parameters
    ----------
    param :
        model parameters
    domain : str
        The domain to implement the model, either: 'Negative' or 'Positive'.
    reaction : str
        The name of the reaction being implemented
    options: dict
        A dictionary of options to be passed to the model.
        See :class:`pybamm.BaseBatteryModel`
    phase : str, optional
        Phase of the particle (default is "primary")

    **Extends:** :class:`pybamm.interface.kinetics.BaseKinetics`
    """

    def __init__(self, param, domain, reaction, options, phase="primary"):
        options = {
            "SEI film resistance": "none",
            "total interfacial current density as a state": "false",
        }
        super().__init__(param, domain, reaction, options, phase)

    def set_phase(self, phase):
        """
        Bypass the phase checks from BaseSubmodel
        """
        options_phase = getattr(self.options, self.domain.lower())["particle phases"]

        if options_phase == "1" and phase == "primary ":
            # Only one phase, no need to distinguish between
            # "primary" and "secondary"
            self.phase_name = ""
        else:
            # add a space so that we can use "" or (e.g.) "primary " interchangeably
            # when naming variables
            self.phase_name = phase + " "

        self.phase = phase

    def get_fundamental_variables(self):
        zero = pybamm.Scalar(0)
        variables = self._get_standard_interfacial_current_variables(zero)
        variables.update(self._get_standard_exchange_current_variables(zero))
        return variables

    def get_coupled_variables(self, variables):
        variables.update(
            self._get_standard_volumetric_current_density_variables(variables)
        )
        return variables

    def _get_dj_dc(self, variables):
        return pybamm.Scalar(0)

    def _get_dj_ddeltaphi(self, variables):
        return pybamm.Scalar(0)

    def _get_j_diffusion_limited_first_order(self, variables):
        return pybamm.Scalar(0)
