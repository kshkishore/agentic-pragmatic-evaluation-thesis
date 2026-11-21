#!/bin/bash
# Runs after the robustness experiment: Experiment 7 (CO-STAR generation brief), Experiment 8 (extension set), determinism check.
cd "$(dirname "$0")"
F='^llama_\|^ggml\|^load\|^print_info\|^\s*$\|^clip_\|^mtmd\|^init_\|^alloc\|^warmup\|^main:'
while ! grep -q ROBUSTDONE progress.log; do sleep 20; done
echo "=== CHAIN2 START $(date -u +%H:%M:%S)" >> progress.log
python3 exp7.py gen 2>/dev/null | grep -v "$F" >> run_exp7_gen.log;  echo "=== DONE exp7_gen $(date -u +%H:%M:%S)" >> progress.log
python3 exp7.py j1  2>/dev/null | grep -v "$F" >> run_exp7_j1.log;   echo "=== DONE exp7_j1 $(date -u +%H:%M:%S)" >> progress.log
python3 ext_run.py j1 2>/dev/null | grep -v "$F" >> run_ext_j1.log;  echo "=== DONE ext_j1 $(date -u +%H:%M:%S)" >> progress.log
python3 exp7.py j2  2>/dev/null | grep -v "$F" >> run_exp7_j2.log;   echo "=== DONE exp7_j2 $(date -u +%H:%M:%S)" >> progress.log
python3 ext_run.py j2 2>/dev/null | grep -v "$F" >> run_ext_j2.log;  echo "=== DONE ext_j2 $(date -u +%H:%M:%S)" >> progress.log
python3 ext_run.py rerun 2>/dev/null | grep -v "$F" >> run_rerun.log; echo "=== DONE rerun $(date -u +%H:%M:%S)" >> progress.log
echo CHAIN2DONE >> progress.log
