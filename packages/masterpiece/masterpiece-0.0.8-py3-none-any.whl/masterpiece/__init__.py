"""
Description
===========

Base classes for MasterPiece - a light-weight and general purpose object-oriented toolkit
for implementing scalable, modular plugin-aware applications.

"""

from .masterpiece import MasterPiece
from .composite import Composite
from .application import Application
from .log import Log
from .plugin import Plugin
from .plugmaster import PlugMaster
from .treevisualizer import TreeVisualizer


__all__ = [
    "MasterPiece",
    "Composite",
    "Application",
    "Log",
    "Plugin",
    "PlugMaster",
    "ArgsMaestro",
    "TreeVisualizer",
]
