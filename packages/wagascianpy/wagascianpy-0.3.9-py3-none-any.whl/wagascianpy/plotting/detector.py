#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio

"""

This module is used by the data harvesters to handle the decoded data TTrees for each DIF. Basically it just
opens a TTree and enables some of its TBranches. Optionally it can store a list of events for later retrieval.
It is not really meant to read the TTree itself, just open it and do some collateral checks.

The classes are organized in a tree-like structure where basically a "Detectors" object is just a list of "Detector"
objects, which in turn are a list of "Dif" objects. The detectors and DIFs are iterable like standard Python lists,
even if strictly speaking they are not subclasses of 'list'.

"""

from collections import namedtuple
from typing import Optional, List

try:
    import ROOT

    ROOT.PyConfig.IgnoreCommandLineOptions = True
except ImportError:
    ROOT = None

from wagascianpy.plotting.topology import Topology, DetectorType, DifIndex, DetectorIndex, snakecase

WallmrdDifList = namedtuple('WallmrdDifList', ['top', 'bottom'])
WagasciDifList = namedtuple('WagasciDifList', ['top', 'side'])


class Dif(object):
    """
    Class representing a signle DIF. It contains the following info about a DIF:
      - DIF ID (a unique integer for each DIF)
      - A boolean flag if the DIF is enabled or disabled
      - A main TTree associated to the DIF (usually the raw data tree)
      - A list of TTrees that are friends with the main TTree
      - A list of spills (can be any Python list)
    """

    def __init__(self, name, dif_id, enabled):
        # type: (str, int, bool) -> None
        """
        :param name: name of the DIF
        :param dif_id: unique ID of the DIF
        :param enabled: true if the DIF is to be enabled
        """
        self.name = name
        self._dif_id = dif_id
        self._enabled = enabled
        self._tree_name = None
        self._chain = None
        self._friends = {}
        self._spills = None

    @property
    def dif_id(self):
        """
        :return: integer ID of the DIF
        """
        return self._dif_id

    def is_enabled(self):
        """
        :return: true if DIF is enabled
        """
        return self._enabled

    def enable(self):
        """
        Enable the DIF
        """
        self._enabled = True

    def disable(self):
        """
        Disable the DIF
        """
        self._enabled = False

    def add_tree(self, root_file, tree_name, tree_friends=None):
        # type: (str, str, Optional[List[str]]) -> None
        """
        Get the TTree handle from the ROOT file together with all its friends if any
        :param root_file: ROOT file where the TTree is stored
        :param tree_name: TTree name
        :param tree_friends: Names of the friend TTrees
        :return: nothing
        """
        if self._tree_name is None:
            self._tree_name = tree_name
        if tree_name != self._tree_name:
            raise ValueError("TTree name must be consistent among all ROOT files")
        if self._chain is None:
            self._chain = ROOT.TChain(tree_name)
        print("Tree {} found in {}".format(tree_name, root_file))
        self._chain.Add(root_file)
        if tree_friends:
            tfile = ROOT.TFile(root_file, "READ")
            for friend in tree_friends:
                if tfile.GetListOfKeys().Contains(friend):
                    print("Tree friend {} found in {}".format(friend, root_file))
                    if friend not in self._friends:
                        self._friends[friend] = ROOT.TChain(friend)
                        self._chain.AddFriend(self._friends[friend])
                    self._friends[friend].Add(root_file)
                else:
                    print("Tree friend {} not found in {}".format(friend, root_file))
            tfile.Close()

    def set_active_branches(self, active_branches):
        # type: (List[str]) -> None
        """
        Set which branches of the main TTree are active
        :param active_branches: names of the active branches
        :return: None
        """
        assert self._chain is not None, "Add a tree before accessing it"
        self._chain.SetBranchStatus("*", 0)
        for variable in active_branches:
            # if not any((branch.GetName() == variable for branch in self._chain.GetListOfBranches())):
            #     raise StopIteration("Branch {} not found in tree {}".format(variable, self._chain.GetName()))
            self._chain.SetBranchStatus(variable, 1)

    def get_tree(self):
        # type: (...) -> ROOT.TChain
        """
        :return: main TTree
        """
        assert self._chain is not None, "Add a tree before accessing it"
        return self._chain

    def get_friend(self, name):
        # type: (str) -> ROOT.TChain
        """
        :param name: name of friend TTree
        :return: a TTree whose friend with the main TTree
        """
        return self._friends[name]

    def has_friend(self, name):
        # type: (str) -> bool
        """
        :param name: name of friend TTree
        :return: true if the main TTree has a friend
        """
        return name in self._friends

    def set_spills(self, spills):
        # type: (List[sp.WagasciBsdSpill]) -> None
        """
        Store a list of spills
        :param spills: list of spills (but can be any list of objects)
        """
        assert isinstance(spills, list), "The spill list must be a list"
        self._spills = spills

    def get_spills(self):
        # type: (...) -> List[sp.WagasciBsdSpill]
        """
        :return: list of spills (but can be any list of objects)
        """
        assert self._spills is not None, "Please set the spill list before accessing it"
        return self._spills

    def has_spills(self):
        # type: (...) -> bool
        """
        :return: true if a non empty list of spills has been set
        """
        return bool(self._spills)

    def has_tree(self):
        # type: (...) -> bool
        """
        :return: true if the main TTree has been set
        """
        if self._chain is None:
            return False
        else:
            return True


class Detector(object):
    """
    Class representing a detector. It is useful to keep track of which detector is active and which not.
    If contains the following info:
      - Name of the detector
      - boolean Flag if the detector is enabled or not
      - List of Dif objects corresponding to the DIFs that make up the detector
    """

    def __init__(self, name, difs, enabled=True):
        # type: (str, Union[WallmrdDifList,WagasciDifList], bool) -> None
        """
        :param name: name of the detector
        :param difs: list of Dif objects
        :param enabled: true if the detector is to be enabled
        """
        self.name = name
        self._enabled = enabled
        if isinstance(difs, WallmrdDifList):
            self.detector_type = DetectorType.Wallmrd
            self.top = difs.top
            self.bottom = difs.bottom
            self.num_difs = 2
        elif isinstance(difs, WagasciDifList):
            self.detector_type = DetectorType.Wagasci
            self.top = difs.top
            self.side = difs.side
            self.num_difs = 2
        else:
            raise NotImplementedError("DIF list type {} not recognized".format(type(difs).__name__))

    def is_enabled(self):
        # type: (...) -> bool
        """
        :return: true if all Difs in the detector are enabled and have a TTree and spill list loaded, false otherwise
        """
        if not self._enabled:
            return False
        else:
            for dif in self:
                if not dif.has_tree() or not dif.has_spills():
                    return False
        return True

    def get_snake_case_name(self):
        """
        :return: name of the detector in snake case
        """
        return self.name.lower().replace(' ', '_')

    def __iter__(self):
        """ Returns the DifsIterator object """
        return DifsIterator(self)


class Detectors(object):
    """
    List of Detector objects representing all the detectors in the WAGASCI experiment.
    This class can be iterated by DIF or by detector. When iterated by DIF, the loop is over Dif objects,
    when iterated by detector, the loop is over the Detector objects.
    """

    def __init__(self, enabled_detectors=None):
        # type: (Optional[Topology]) -> None
        """
        :param enabled_detectors: which detectors are enabled and which are not
        """
        self._enabled_detectors = Topology(iterate_by_dif=True)
        if enabled_detectors is not None:
            self._enabled_detectors.import_topology(enabled_detectors)

        self.wallmrd_north = Detector(
            name=DetectorIndex.get_name(DetectorIndex.WallMrdNorth),
            difs=WallmrdDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WallmrdNorthTop),
                                    enabled=self._enabled_detectors.wallmrd_north_top.is_enabled()),
                                Dif(name="bottom",
                                    dif_id=int(DifIndex.WallmrdNorthBottom),
                                    enabled=self._enabled_detectors.wallmrd_north_bottom.is_enabled())),
            enabled=(self._enabled_detectors.wallmrd_north_top.is_enabled() or
                     self._enabled_detectors.wallmrd_north_bottom.is_enabled()))
        self.wallmrd_south = Detector(
            name=DetectorIndex.get_name(DetectorIndex.WallMrdSouth),
            difs=WallmrdDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WallmrdSouthTop),
                                    enabled=self._enabled_detectors.wallmrd_south_top.is_enabled()),
                                Dif(name="bottom",
                                    dif_id=int(DifIndex.WallmrdSouthBottom),
                                    enabled=self._enabled_detectors.wallmrd_south_bottom.is_enabled())),
            enabled=(self._enabled_detectors.wallmrd_south_top.is_enabled() or
                     self._enabled_detectors.wallmrd_south_bottom.is_enabled()))
        self.wagasci_upstream = Detector(
            name=DetectorIndex.get_name(DetectorIndex.WagasciUpstream),
            difs=WagasciDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WagasciUpstreamTop),
                                    enabled=self._enabled_detectors.wagasci_upstream_top.is_enabled()),
                                Dif(name="side",
                                    dif_id=int(DifIndex.WagasciUpstreamSide),
                                    enabled=self._enabled_detectors.wagasci_upstream_side.is_enabled())),
            enabled=(self._enabled_detectors.wagasci_upstream_top.is_enabled() or
                     self._enabled_detectors.wagasci_upstream_side.is_enabled()))
        self.wagasci_downstream = Detector(
            name=DetectorIndex.get_name(DetectorIndex.WagasciDownstream),
            difs=WagasciDifList(Dif(name="top",
                                    dif_id=int(DifIndex.WagasciDownstreamTop),
                                    enabled=self._enabled_detectors.wagasci_downstream_top.is_enabled()),
                                Dif(name="side",
                                    dif_id=int(DifIndex.WagasciDownstreamSide),
                                    enabled=self._enabled_detectors.wagasci_downstream_side.is_enabled())),
            enabled=(self._enabled_detectors.wagasci_downstream_top.is_enabled() or
                     self._enabled_detectors.wagasci_downstream_side.is_enabled()))

    def __iter__(self):
        """ Returns the DetectorsIterator object """
        return DetectorsIterator(self)

    def get_dif(self, dif):
        # type: (Union[int, str]) -> Dif
        """
        :param dif: name or ID of the DIF
        :return: Dif object
        """
        dif_name = DifIndex.get_name_snakecase(dif) if isinstance(dif, int) else snakecase(dif)
        dif_id = DifIndex.get_index(dif) if isinstance(dif, str) else dif
        detector = next((detector for detector in self if snakecase(detector.name) in dif_name))
        return next(dif for dif in detector if dif.dif_id == dif_id)

    def get_detector(self, detector_id):
        # type: (Union[int, str]) -> Detector
        """
        :param detector_id: name or ID of the DETECTOR
        :return: Detector object whose ID is detector_id
        """
        if isinstance(detector_id, int):
            return getattr(self, DetectorIndex.get_name_snakecase(detector_id))
        else:
            return getattr(self, snakecase(detector_id))

    def has_dif(self, dif_id):
        # type: (...) -> bool
        """
        :param dif_id: unique DIF ID
        :return: true if the DIF is enabled and its TTree is loaded
        """
        try:
            dif = self.get_dif(dif_id)
        except (ValueError, AttributeError):
            return False
        else:
            return dif.is_enabled() and dif.has_tree()

    def disable_all_difs(self):
        # type: (...) -> None
        """
        Disable all DIFs
        """
        for detector in self:
            for dif in detector:
                dif.disable()

    def enable_dif(self, dif_id):
        # type: (int) -> None
        """
        :param dif_id: unique DIF ID
        :return: disable DIF whose ID is dif_id
        """
        dif_id = int(dif_id)
        self.get_dif(dif_id).enable()

    def activate_branches(self, active_branches_names):
        # type: (List[str]) -> None
        for detector in self:
            for dif in detector:
                if dif.has_tree():
                    dif.set_active_branches(active_branches=active_branches_names)
                else:
                    dif.disable()


class DifsIterator(object):
    """
    Itarate over all Dif objects
    """

    def __init__(self, detector):
        # Difs object reference
        self._detector = detector
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        """ Returns the next value from difs object's lists """
        result = None
        if self._detector.detector_type == DetectorType.Wallmrd:
            if self._index < 2:
                if self._index == 0:
                    result = self._detector.top
                elif self._index == 1:
                    result = self._detector.bottom
                self._index += 1
                return result
        elif self._detector.detector_type == DetectorType.Wagasci:
            if self._index < 2:
                if self._index == 0:
                    result = self._detector.top
                elif self._index == 1:
                    result = self._detector.side
                self._index += 1
                return result
        else:
            raise NotImplementedError("Detector type {} not recognized".format(self._detector.detector_type))
        # End of Iteration
        raise StopIteration

    def next(self):
        return self.__next__()


class DetectorsIterator(object):
    """
    Iterate overall Detector objects
    """

    def __init__(self, detectors):
        # Detectors object reference
        self._detectors = detectors
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        """ Returns the next value from detectors object's lists """
        result = None
        if self._index < len(DetectorIndex):
            if self._index == DetectorIndex.WallMrdNorth:
                result = self._detectors.wallmrd_north
            elif self._index == DetectorIndex.WallMrdSouth:
                result = self._detectors.wallmrd_south
            elif self._index == DetectorIndex.WagasciUpstream:
                result = self._detectors.wagasci_upstream
            elif self._index == DetectorIndex.WagasciDownstream:
                result = self._detectors.wagasci_downstream
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration

    def next(self):
        return self.__next__()
