"""Capture Allure overview/suites over HTTP (file:// SPA routes break)."""

from pathlib import Path
import runpy

# Delegate to the maintained recapture helper.
runpy.run_path(str(Path(__file__).resolve().parent / "recapture_kt08_allure.py"), run_name="__main__")
