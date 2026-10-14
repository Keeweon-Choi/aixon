import subprocess, sys
from pathlib import Path

ROOT=Path(__file__).parents[2]
def run(*args): return subprocess.run([sys.executable,*args],cwd=ROOT,text=True,capture_output=True)
def test_content_validator_accepts_site_doc():
    result=run('tools/validate_content.py','--graph','data/seed/seed_graph.yaml')
    assert result.returncode == 0, result.stdout + result.stderr
def test_check_dist_reports_missing_required_files(tmp_path):
    (tmp_path/'index.html').write_text('<html lang="ko"><title>x</title><meta name="description" content="x"><h1>x</h1></html>')
    result=run('tools/check_dist.py',str(tmp_path))
    assert result.returncode == 1
