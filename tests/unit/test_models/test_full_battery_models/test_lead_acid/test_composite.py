#
# Tests for the lead-acid composite model
#
import pybamm
import unittest


@unittest.skipIf(pybamm.have_scikits_odes(), "scikits.odes not installed")
class TestLeadAcidComposite(unittest.TestCase):
    def test_well_posed(self):
        options = {"thermal": None, "Voltage": "On"}
        model = pybamm.lead_acid.Composite(options)
        model.check_well_posedness()

    def test_well_posed_with_convection(self):
        options = {"thermal": None, "Voltage": "On", "convection": True}
        model = pybamm.lead_acid.Composite(options)
        model.check_well_posedness()


@unittest.skipIf(pybamm.have_scikits_odes(), "scikits.odes not installed")
class TestLeadAcidCompositeSurfaceForm(unittest.TestCase):
    def test_well_posed(self):
        options = {"thermal": None, "Voltage": "On", "capacitance": False}
        model = pybamm.lead_acid.surface_form.Composite(options)
        model.check_well_posedness()

    def test_well_posed_with_capacitance(self):
        options = {"thermal": None, "Voltage": "On", "capacitance": True}
        model = pybamm.lead_acid.surface_form.Composite(options)
        model.check_well_posedness()

    def test_default_solver(self):
        options = {"thermal": None, "Voltage": "On", "capacitance": True}
        model = pybamm.lead_acid.surface_form.Composite(options)
        self.assertIsInstance(model.default_solver, pybamm.ScikitsOdeSolver)
        options = {"thermal": None, "Voltage": "On", "capacitance": False}
        model = pybamm.lead_acid.surface_form.Composite(options)
        self.assertIsInstance(model.default_solver, pybamm.ScikitsDaeSolver)

    def test_well_posed_with_convection(self):
        options = {
            "thermal": None,
            "Voltage": "On",
            "capacitance": False,
            "convection": True,
        }
        model = pybamm.lead_acid.Composite(options)
        model.check_well_posedness()


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()
