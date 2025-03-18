import os
import sys
import subprocess
from colorama import Fore, Style, init

# Initialize colorama
init()


def ensure_venv():
    """
    Check if running in a virtual environment, if not, try to activate it.
    """
    # Check if already in a virtual environment
    if sys.prefix == sys.base_prefix:
        # Not in a virtual environment, try to activate it
        script_dir = os.path.dirname(os.path.abspath(__file__))
        venv_dir = os.path.join(os.path.dirname(script_dir), 'venv')

        if os.path.exists(venv_dir):
            print(f"{Fore.YELLOW}Not running in virtual environment. Attempting to activate...{Style.RESET_ALL}")

            # Determine the activate script based on the platform
            if sys.platform == 'win32':
                activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
                if os.name == 'nt':
                    # For PowerShell
                    cmd = f"& '{activate_script}' && python '{__file__}' {' '.join(sys.argv[1:])}"
                    subprocess.run(['powershell', '-Command', cmd], check=True)
                else:
                    # For cmd.exe
                    cmd = f"call {activate_script} && python {__file__} {' '.join(sys.argv[1:])}"
                    subprocess.run(cmd, shell=True, check=True)
            else:
                # For Unix-like systems
                activate_script = os.path.join(venv_dir, 'bin', 'activate')
                cmd = f"source {activate_script} && python {__file__} {' '.join(sys.argv[1:])}"
                subprocess.run(cmd, shell=True, check=True)

            # Exit the original process
            sys.exit(0)
        else:
            print(f"{Fore.YELLOW}Virtual environment not found at {venv_dir}. Continuing without activation.{Style.RESET_ALL}")

# # Example usage
# ensure_venv()
