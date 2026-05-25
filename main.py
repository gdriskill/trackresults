import subprocess
import sys
import os
from track_results.results_parser import ResultsParser

"""Main entry point for track_results."""

def main():
    subprocess.run([sys.executable, "src/track_results/streamlit_app.py"])

if __name__ == "__main__":
    main()