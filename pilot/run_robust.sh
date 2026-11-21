#!/bin/bash
cd "$(dirname "$0")"
echo "=== ROBUST START $(date -u +%H:%M:%S)" >> progress.log
python3 robust.py j1 2>/dev/null | grep -v "^llama_\|^ggml\|^load\|^print_info\|^\s*$" >> run_robust_j1.log
echo "=== DONE robust_j1 $(date -u +%H:%M:%S)" >> progress.log
python3 robust.py j2 2>/dev/null | grep -v "^llama_\|^ggml\|^load\|^print_info\|^\s*$" >> run_robust_j2.log
echo "=== DONE robust_j2 $(date -u +%H:%M:%S)" >> progress.log
echo ROBUSTDONE >> progress.log
