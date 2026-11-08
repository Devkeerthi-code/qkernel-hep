#!/usr/bin/env bash
# Run configs one after another, each logged to results/<name>.log, retrying on crash.
# The runner skips rows already in results/<name>/runs.jsonl, so a retry resumes where it stopped.
#   bash scripts/run_queue.sh configs/main_grid.yaml configs/n_sweep.yaml configs/big_qubits.yaml
cd "$(dirname "$0")/.."
PY=${PY:-.venv/Scripts/python.exe}
[ -x "$PY" ] || PY=.venv/bin/python
MAX_TRIES=${MAX_TRIES:-5}
for cfg in "$@"; do
  name=$(basename "$cfg" .yaml)
  log=results/$name.log
  mkdir -p results
  for try in $(seq 1 "$MAX_TRIES"); do
    echo "=== $(date '+%F %T') start $cfg (attempt $try)" >> "$log"
    if "$PY" -u -m src.run "$cfg" >> "$log" 2>&1; then
      echo "=== $(date '+%F %T') done $cfg" >> "$log"
      break
    fi
    echo "=== $(date '+%F %T') CRASHED $cfg (exit $?), retrying in 60 s" >> "$log"
    [ "$try" = "$MAX_TRIES" ] && { echo "=== giving up on $cfg" >> "$log"; exit 1; }
    sleep 60
  done
done
