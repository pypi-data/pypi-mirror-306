#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright 2019 Pintaudi Giorgio

# pylint: disable=missing-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-instance-attributes

import json
import sys
from copy import deepcopy
from functools import partial

try:
    # for Python2
    # noinspection PyPep8Naming,PyUnresolvedReferences
    import Tkinter as tkinter
except ImportError:
    # for Python3
    # noinspection PyPep8Naming,PyUnresolvedReferences
    import tkinter
try:
    # for Python2
    # noinspection PyPep8Naming,PyUnresolvedReferences
    import tkMessageBox as messagebox
except ImportError:
    # for Python3
    # noinspection PyPep8Naming,PyUnresolvedReferences,PyCompatibility
    from tkinter import messagebox

if not hasattr(sys, 'argv'):
    sys.argv = ['']


# ------------------------------------


class TopologyDialog(object):

    def __init__(self, parent, topology):
        top = self.top = tkinter.Toplevel(parent)
        top.wm_geometry("1000x150")
        tkinter.Label(top, text="Topology").pack()
        ent_topol = tkinter.Entry(top)
        ent_topol.insert(tkinter.END, topology)
        ent_topol.pack(padx=5, fill='both')
        but = tkinter.Button(top, text="OK", command=self.is_ok)
        but.pack(pady=5)

    def is_ok(self):
        self.top.destroy()


class GenerateTopologyGUI(object):

    def _add_gdcc(self):
        self.gdcc_frames.append(tkinter.Frame(self.root))
        self.gdcc_frames[-1].pack(side=tkinter.LEFT, fill='both')
        if not self.topology:
            max_gdcc = 0
        else:
            max_gdcc = max(key for key in self.topology)
        gdcc = max_gdcc + 1
        self.topology[gdcc] = {}
        self.asu_entries[gdcc] = {}
        self.dif_entries[gdcc] = {}
        # print "Add GDCC %d" %(gdcc)
        tkinter.Label(self.gdcc_frames[-1], text='GDCC %d' % gdcc).pack(fill='both')
        add_new_dif = partial(self._add_dif, gdcc)
        tkinter.Button(self.gdcc_frames[-1], text='<Add DIF>', command=add_new_dif).pack(fill='both')

    # ------------------------------------

    def _add_dif(self, gdcc):
        self.dif_frames.append([])
        self.dif_frames[gdcc - 1].append(tkinter.Frame(self.gdcc_frames[gdcc - 1]))
        self.dif_frames[gdcc - 1][-1].pack(side=tkinter.LEFT, fill='both')
        if not self.topology[gdcc]:
            max_dif = 0
        else:
            max_dif = max(key for key in self.topology[gdcc])
        dif = max_dif + 1
        self.topology[gdcc][dif] = {}
        self.asu_entries[gdcc][dif] = {}
        # print "GDCC %d : add DIF %d" %(gdcc, dif)
        dif_ent = tkinter.Entry(self.dif_frames[gdcc - 1][-1])
        dif_ent.insert(tkinter.END, 'DIF %d ID' % dif)
        tkinter.Label(self.dif_frames[gdcc - 1][-1], text='DIF %d' % dif).pack(fill='both')
        dif_ent.pack(fill='both')
        self.dif_entries[gdcc][dif] = dif_ent
        add_new_asu = partial(self._add_asu, gdcc, dif)
        tkinter.Button(self.dif_frames[gdcc - 1][-1], text='<Add ASU>',
                       command=add_new_asu).pack(fill='both')

    # ------------------------------------

    def _add_asu(self, gdcc, dif):
        ent = tkinter.Entry(self.dif_frames[gdcc - 1][dif - 1])
        ent.pack(fill='both')
        if not self.topology[gdcc][dif]:
            max_asu = 0
        else:
            max_asu = max(key for key in self.topology[gdcc][dif])
        asu = max_asu + 1
        self.topology[gdcc][dif][asu] = 0
        self.asu_entries[gdcc][dif][asu] = ent
        tkinter.Label(self.dif_frames[gdcc - 1][dif - 1], text='ASU %d' % asu).pack(fill='both')
        # print "GDCC %d : DIF %d : add ASU %d" %(gdcc, dif, asu)

    # ------------------------------------

    def _dif_id_is_sane(self):
        if not self.dif_entries:
            messagebox.showwarning("Warning", "DIF ID is empty")
            return False
        for gdcc, dif_entries_map in self.dif_entries.items():
            if not dif_entries_map:
                messagebox.showwarning("Warning", "DIF ID[GDCC %d] is empty" % gdcc)
                return False
            for dif, dif_entry in self.dif_entries[gdcc].items():
                dif_id = dif_entry.get()
                if dif is None or dif_id is None:
                    messagebox.showwarning("Warning", "DIF ID[GDCC %d] is empty" % gdcc)
                    return False
                try:
                    dif_id = int(dif_id)
                except ValueError:
                    messagebox.showwarning("Warning", "DIF ID[GDCC %d][DIF %s] is not an int"
                                           % (gdcc, dif))
                    return False
                self.dif_entries[gdcc][dif] = dif_id
        return True

    # ------------------------------------

    def _replace_dif_id(self):
        for gdcc in self.dif_entries:
            if self.topology[gdcc]:
                self.labeled_topology[gdcc] = {}
            for dif, dif_id in self.dif_entries[gdcc].items():
                if self.topology[gdcc][dif]:
                    self.labeled_topology[gdcc][dif_id] = {}
                    self.labeled_topology[gdcc][dif_id] = deepcopy(self.topology[gdcc][dif])

    # ------------------------------------

    def _topology_is_sane(self):
        if not self.topology:
            messagebox.showwarning("Warning", "topology is empty")
            return False
        for gdcc, dif_map in self.topology.items():
            if not dif_map:
                messagebox.showwarning("Warning", "topology[GDCC %d] is empty" % gdcc)
                return False
            for dif, asu_map in self.topology[gdcc].items():
                if not asu_map:
                    messagebox.showwarning("Warning", "topology[GDCC %d][DIF %d] is empty"
                                           % (gdcc, dif))
                    return False
                for asu, asu_entry in self.asu_entries[gdcc][dif].items():
                    n_channels = asu_entry.get()
                    if not n_channels or n_channels is None:
                        messagebox.showwarning("Warning", "topology[GDCC %d][DIF %d][ASU %d] "
                                                          "is empty" % (gdcc, dif, asu))
                        return False
                    self.topology[gdcc][dif][asu] = int(n_channels)
                    if int(n_channels) <= 0:
                        messagebox.showwarning("Warning", " number of channels "
                                                          "(topology[GDCC %d][DIF %d][ASU %d]) "
                                                          "is less or equal to zero" % (gdcc, dif, asu))
                        return False
        return True

    # ------------------------------------

    def _show_topology(self):
        if self._topology_is_sane():
            if self._dif_id_is_sane():
                self._replace_dif_id()
                self.topology.clear()
                self.topology = self.labeled_topology.copy()
            else:
                return False
            self.topology_json = json.dumps(self.topology)
            dialog = TopologyDialog(self.root, self.topology_json)
            self.show_topology_button["state"] = "disabled"
            self.root.wait_window(dialog.top)
            self.show_topology_button["state"] = "normal"
            self.root.quit()
            return True
        else:
            return False

    # ------------------------------------

    def __init__(self, persistent_mode=None):
        self.gdcc_frames = []
        self.dif_frames = []
        self.topology = {}
        self.labeled_topology = {}
        self.asu_entries = {}
        self.dif_entries = {}
        self.topology_json = None
        self.root = None
        self.show_topology_button = None
        self.persistent_mode = persistent_mode

    # ------------------------------------

    def run(self):
        self.root = tkinter.Tk()
        self.root.title("WAGASCI topology generator")
        self.root.option_add("*Dialog.msg.wrapLength", "10i")

        show_button = self.show_topology_button = tkinter.Button(self.root, text='Print topology string',
                                                                 command=self._show_topology)
        show_button.pack(fill='both')

        add_gdcc_button = tkinter.Button(self.root, text='<Add GDCC>', fg="Blue", command=self._add_gdcc)
        add_gdcc_button.pack(fill='both')

        try:
            self.root.mainloop()
            if self.persistent_mode is None:
                self.root.destroy()
            return_json = self.topology_json
            return return_json
        except AttributeError:
            self.root.destroy()
            return ""


# ------------------------------------

def topology_generator(persistent_mode=None):
    gui = GenerateTopologyGUI(persistent_mode)
    return gui.run()


# ------------------------------------

if __name__ == "__main__":
    topology_generator("persistent_mode")
