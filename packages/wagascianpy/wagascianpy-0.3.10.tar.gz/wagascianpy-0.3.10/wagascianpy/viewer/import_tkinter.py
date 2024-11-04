#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

def import_tkinter():
    try:
        # for Python2
        # noinspection PyPep8Naming
        import Tkinter as tkinter
        print("Found Python2 Tkinter module")
    except ImportError:
        # for Python3
        try:
            import tkinter
            print("Found Python3 tkinter module")
        except ImportError:
            print("[ERROR] tkinter could not be found!")
            tkinter = None
    return tkinter


def import_filedialog():
    try:
        # for Python2
        # noinspection PyPep8Naming,PyUnresolvedReferences
        import tkFileDialog as filedialog
        print("Found Python2 tkFileDialog module")
    except ImportError:
        # for Python3
        try:
            # noinspection PyPep8Naming,PyUnresolvedReferences,PyCompatibility
            from tkinter import filedialog
            print("Found Python3 filedialog module")
        except ImportError:
            print("[ERROR] filedialog could not be found!")
            filedialog = None
    return filedialog


def import_messagebox():
    try:
        # for Python2
        # noinspection PyPep8Naming,PyUnresolvedReferences
        import tkMessageBox as messagebox
        print("Found Python2 tkMessageBox module")
    except ImportError:
        # for Python3
        try:
            # noinspection PyPep8Naming,PyUnresolvedReferences,PyCompatibility
            from tkinter import messagebox
            print("Found Python3 messagebox module")
        except ImportError:
            print("[ERROR] messagebox could not be found!")
            messagebox = None
    return messagebox


def import_pygubu():
    try:
        import pygubu
        print("Found Python pygubu module")
    except ImportError:
        print("[ERROR] pygubu could not be found!")
        pygubu = None
    return pygubu
