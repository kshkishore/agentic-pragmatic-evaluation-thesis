#!/bin/bash
cd "$(dirname "$0")"
echo "=== RESTART $(date -u +%H:%M:%S) (SmolVLM2 template fix)" >> progress.log
for ph in gen j1_gen j2 pair; do
  echo "=== PHASE $ph $(date -u +%H:%M:%S)" >> progress.log
  python3 run.py $ph 2>/dev/null | grep -v "^llama_\|^ggml\|^load\|^print_info\|^\s*$" >> run_${ph}.log
  echo "=== DONE $ph $(date -u +%H:%M:%S)" >> progress.log
  if [ "$ph" = "gen" ]; then python3 metrics.py gen > metrics_gen.log 2>&1; echo "=== DONE metrics_gen $(date -u +%H:%M:%S)" >> progress.log; fi
done
echo ALLDONE >> progress.log
