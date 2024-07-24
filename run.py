import subprocess

def run_notebook(notebook_path, output_path='/Users/ayannair/Documents/projects/fantanosize/backend/results.json'):
    try:
        subprocess.run([
            'jupyter', 'nbconvert', '--to', 'notebook', '--execute', 
            '--output', output_path, notebook_path
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f'Error running notebook: {str(e)}')
