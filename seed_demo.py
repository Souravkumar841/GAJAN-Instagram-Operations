"""Idempotently add fictional demonstration records to ops.db."""
import os
from pathlib import Path
os.environ.setdefault('OPS_DB',str(Path(__file__).resolve().parent/'ops.db'))
from app import core
core.init()
for brand,owner,handle,status in [('DEMO_FASHION','Aisha','demo_fashion','configured'),('DEMO_CAFE','Rahul','demo_cafe','waiting_human'),('DEMO_TRAVEL','Priya','demo_travel','planned')]:
 a=core.register(brand,owner,handle)
 core.update(a['id'],status=status)
 core.task(a['id'],'review_profile',owner,2)
 core.task(a['id'],'confirm_2fa',owner,3)
print('Sample database ready:',os.environ['OPS_DB'])
