"""
AP2 Repository Monitoring Agent

A Python package for monitoring GitHub repositories and generating 
enhanced JSON reports with intelligent analysis and DWS IQ suitability assessment.
"""

from .monitor import AP2Monitor, RepositoryData

__version__ = "1.0.0"
__author__ = "AP2 Team"
__email__ = "ap2@example.com"

__all__ = ["AP2Monitor", "RepositoryData"]