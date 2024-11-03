import logging

import awkward as ak
import numpy as np

from f9columnar.object_collections import Cut, Variable, Weight
from f9columnar.utils.helpers import load_luminosity, load_periods


class AddIndex(Variable):
    name = "addIndex"

    def __init__(self):
        super().__init__()

    def run(self, arrays):
        array_len = len(arrays[arrays.fields[0]])
        arrays["idx"] = ak.Array(np.arange(0, array_len, 1) * np.ones(array_len, dtype=np.int64))
        return {"arrays": arrays}


class AddYears(Variable):
    name = "addYears"

    def __init__(self):
        """Add years to the arrays based on the run numbers.

        Note
        ----
        171: RunNumber 2017 start, prescale start
        172: prescale end, RunNumber 2017 end
        170: prescale start, prescale end

        """
        super().__init__()
        try:
            self._periods = load_periods()
        except FileNotFoundError:
            logging.warning("Periods file not found. Run numbers will not be available.")
            self._periods = None

    def run(self, arrays):
        if self.is_data:
            run_numbers = arrays["runNumber"]
        else:
            run_numbers = arrays["randomRunNumber"]

        years = np.zeros(len(run_numbers), dtype=np.int32)
        for year, (start, end) in self._periods.items():
            years[ak.where((start <= run_numbers) & (run_numbers <= end))[0]] = year

        arrays["years"] = ak.Array(years)

        return {"arrays": arrays}


class EventObjectNumberCut(Cut):
    name = "eventObjectNumberCut"

    def __init__(self, n_objects, count_branch_name, at_least=False):
        super().__init__()
        self.n_objects = n_objects
        self.count_branch_name = count_branch_name
        self.at_least = at_least

    def run(self, arrays):
        counts = ak.num(arrays[self.count_branch_name])

        if self.at_least:
            mask = counts >= self.n_objects
        else:
            mask = counts == self.n_objects

        arrays = arrays[mask].remove_empty()

        return {"arrays": arrays}


class LumiWeight(Weight):
    name = "lumiWeight"

    def __init__(self):
        super().__init__()
        lumi_dct = load_luminosity()
        lumis, lumis_scale, years = (
            lumi_dct["lumi"].values(),
            lumi_dct["lumi_scale"].values(),
            lumi_dct["lumi"].keys(),
        )

        self.lumi_dct = {}
        for lumi, scale, year in zip(lumis, lumis_scale, years):
            self.lumi_dct[year] = lumi * scale

    def run(self, arrays):
        if self.is_data:
            return {"arrays": arrays}

        run_number = ak.to_numpy(arrays["runNumber"])

        lumis = np.zeros_like(run_number, dtype=np.float32)

        lumis = np.where(run_number == 284500, self.lumi_dct[15] + self.lumi_dct[16], lumis)
        lumis = np.where(run_number == 300000, self.lumi_dct[17], lumis)
        lumis = np.where(run_number == 310000, self.lumi_dct[18], lumis)

        if np.any(lumis == 0.0):
            logging.warning("Some luminosities are zero!")

        arrays["lumi_weight"] = lumis

        return {"arrays": arrays}
