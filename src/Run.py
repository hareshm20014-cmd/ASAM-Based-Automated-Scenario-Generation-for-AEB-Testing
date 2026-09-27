import subprocess #..standard module for running a external exe file from script 
from pathlib import Path

def run_esmini(esmini_exe: str, xosc_path: str) -> None:
    command = [
        esmini_exe,
        "--osc", xosc_path,"--window", "60","60","800","400"] 
    
    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("esmini failed:")
        print(result.stderr)
        raise RuntimeError("esmini run failed")
