import os
import subprocess
import DataRefine

def main():
    # Get the path to app.py inside the scripts directory
    app_path = os.path.join(os.path.dirname(DataRefine.__file__), 'scripts','app_.py')
    # Run the Streamlit app
    subprocess.run(["streamlit", "run", app_path])

if __name__ == "__main__":
    main()