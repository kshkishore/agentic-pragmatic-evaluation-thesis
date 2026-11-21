#!/bin/bash
cd "$(dirname "$0")"
for ph in j1_text j1_mm gen j1_gen j2 pair; do
  echo "=== PHASE $ph $(date -u +%H:%M:%S)" >> progress.log
  python3 run.py $ph 2>/dev/null | grep -v "^llama_\|^ggml\|^load\|^print_info\|^\s*$" >> run_${ph}.log
  echo "=== DONE $ph $(date -u +%H:%M:%S)" >> progress.log
done
echo ALLDONE >> progress.log
