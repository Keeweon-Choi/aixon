#!/usr/bin/env python3
"""Run the public verification targets and leave auditable per-step logs."""
from __future__ import annotations
import datetime as dt, json, subprocess, time
from pathlib import Path
steps=['lint','typecheck','test','validate','build','check-dist','e2e','secrets']
root=Path('artifacts/verification/runs')/dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ'); root.mkdir(parents=True,exist_ok=True)
out=[]
for step in steps:
 start=time.monotonic(); run=subprocess.run(['make',step],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 log=root/f'{step}.log'; log.write_text(run.stdout,encoding='utf8')
 out.append({'step':step,'command':f'make {step}','exit_code':run.returncode,'duration_seconds':round(time.monotonic()-start,3),'log_file':str(log)})
 if run.returncode: break
(root/'summary.json').write_text(json.dumps(out,indent=2),encoding='utf8')
raise SystemExit(0 if len(out)==len(steps) and not out[-1]['exit_code'] else 1)
