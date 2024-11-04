#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio


import wagascianpy.program.program
import wagascianpy.program.program_builder
import wagascianpy.utils.environment


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self):
        self._builder = None

    @property
    def builder(self):
        # type: (...) -> wagascianpy.program.program_builder.ProgramBuilder
        return self._builder

    @builder.setter
    def builder(self, builder):
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled product.
        """
        self._builder = builder

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build_decoder(self, overwrite_flag=False, compatibility_mode=False):
        self.builder.enforce_dependencies()
        self.builder.add_decoder(overwrite_flag=overwrite_flag, compatibility_mode=compatibility_mode)

    def build_make_hist(self, overwrite):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_make_hist(overwrite=overwrite)

    def build_bcid_distribution(self, chip_by_chip, overwrite):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_bcid_distribution(chip_by_chip=chip_by_chip, overwrite=overwrite)

    def build_adc_distribution(self, chip_by_chip, overwrite):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_bcid_distribution(chip_by_chip=chip_by_chip, overwrite=overwrite)

    def build_tdc_calibration(self):
        self.builder.do_not_enforce_dependencies()
        self.builder.tdc_calibration()

    def build_spill_number_fixer(self):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_spill_number_fixer(enable_graphics=False)

    def build_apply_detector_flags(self, wagasci_database_location):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_apply_detector_flags(wagasci_database=wagasci_database_location)

    def build_sanity_check(self, wagasci_database_location):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_sanity_check(wagasci_database=wagasci_database_location)

    def build_beam_summary_data(self,
                                bsd_database_location,
                                bsd_repository_location,
                                download_bsd_database_location="/tmp/bsd/bsddb.db",
                                download_bsd_repository_location="/tmp/bsd",
                                t2krun=10):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_beam_summary_data(bsd_database_location=bsd_database_location,
                                           bsd_repository_location=bsd_repository_location,
                                           download_bsd_database_location=download_bsd_database_location,
                                           download_bsd_repository_location=download_bsd_repository_location,
                                           t2krun=t2krun,
                                           recursive=True)

    def build_temperature(self, sqlite_database):
        self.builder.do_not_enforce_dependencies()
        self.builder.add_temperature(sqlite_database=sqlite_database)

    def build_adc_calibration(self, history_location=None):
        self.builder.do_not_enforce_dependencies()
        if not history_location:
            try:
                env = wagascianpy.utils.environment.WagasciEnvironment()
                history_location = env["WAGASCI_PEUDIR"]
            except KeyError as error:
                raise KeyError("Could not find WAGASCI history directory : {}".format(str(error)))
        self.builder.multiple_runs_analyzer_save_location = history_location
        self.builder.add_adc_calibration()

    def build_all(self,
                  wagasci_database_location,
                  bsd_database_location,
                  bsd_repository_location,
                  history_location,
                  sqlite_database,
                  download_bsd_database_location="/tmp/bsd/bsddb.db",
                  download_bsd_repository_location="/tmp/bsd",
                  t2krun=10,
                  overwrite_flag=False,
                  compatibility_mode=False
                  ):
        self.build_decoder(overwrite_flag=overwrite_flag, compatibility_mode=compatibility_mode)
        self.build_tdc_calibration()
        self.build_spill_number_fixer()
        self.build_beam_summary_data(bsd_database_location=bsd_database_location,
                                     bsd_repository_location=bsd_repository_location,
                                     download_bsd_database_location=download_bsd_database_location,
                                     download_bsd_repository_location=download_bsd_repository_location,
                                     t2krun=t2krun)
        self.build_temperature(sqlite_database=sqlite_database)
        self.build_adc_calibration(history_location=history_location)
        self.build_apply_detector_flags(wagasci_database_location=wagasci_database_location)
        self.build_sanity_check(wagasci_database_location=wagasci_database_location)
        self.builder.enforce_dependencies()
