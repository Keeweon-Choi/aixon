#!/usr/bin/env python3
from __future__ import annotations
import re, subprocess, sys
patterns=[r'AKIA[0-9A-Z]{16}',r'gh[pousr]_[A-Za-z0-9]{20,}',r'sk-(?:proj-)?[A-Za-z0-9_-]{20,}',r'Anthropic[a-zA-Z0-9_-]{20,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
files=subprocess.check_output(['git','ls-files'],text=True).splitlines(); hits=[]
for name in files:
 try: text=open(name,encoding='utf8').read()
 except (UnicodeDecodeError,OSError): continue
 for pat in patterns:
  if re.search(pat,text): hits.append(name); break
print('\n'.join(hits) if hits else 'secrets: OK'); raise SystemExit(bool(hits))
