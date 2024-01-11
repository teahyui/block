import json
import subprocess

def cairo_compile(path):
    "Compile from Cairo source code"
    dirname, filename = path
    completed_process = subprocess.run([
        'cairo-compile', f'{dirname}{filename}.cairo',
        '--cairo_path', 'src',
        '--output', f'tests/integration/cairo_programs_compiled/{filename}.json'])
    assert completed_process.returncode == 0

def cairo_run(program_name):
    "Generate register and memory output from running the program"
    completed_process = subprocess.run([
        'cairo-run',
		'--layout', 'all',
        '--program', f'tests/integration/cairo_programs_compiled/{program_name}.json',
        '--trace_file', f'tests/integration/cairo_programs_trace/{program_name}/trace.bin', 
        '--memory_file', f'tests/integration/cairo_programs_trace/{program_name}/memory.bin'])

def giza_prove(program_name):
    "Generate a proof of the program execution"
    completed_process = subprocess.run([
        'giza', 'prove',
        '--program', f'tests/integration/cairo_programs_compiled/{program_name}.json',
        '--trace', f'tests/integration/cairo_programs_trace/{program_name}/trace.bin',
        '--memory', f'tests/integration/cairo_programs_trace/{program_name}/memory.bin',
        '--output', f'tests/integration/stark_proofs/{program_name}.bin',
        '--fri-folding-factor', '8'
        ])


def setup(path):
    cairo_compile(path)
    cairo_run(path[1])
    giza_prove(path[1])
