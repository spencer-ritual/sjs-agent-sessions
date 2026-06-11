#!/usr/bin/env bash
# Runs every traffic in gold-make-run sequentially against the live local network.
# Records PASS/FAIL per traffic based on exit code + output markers.
set -u
GOLD=/home/ritual/repos/sjs-agent-sessions/gold-make-run
OUTDIR=/tmp/gold-run
SUMMARY="$OUTDIR/summary.txt"
mkdir -p "$OUTDIR"
: > "$SUMMARY"
cd /home/ritual/repos/traffic-gen-internal || exit 1

i=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac
  i=$((i+1))
  # derive a short name from the make target
  name=$(printf '%s' "$line" | sed -E 's/^make (run-[a-z0-9-]+).*/\1/')
  log="$OUTDIR/$(printf '%02d' "$i")_${name}.log"
  echo "=== [$i] START $name :: $line ===" | tee -a "$SUMMARY"
  start=$(date +%s)
  bash -c "$line" >"$log" 2>&1
  rc=$?
  end=$(date +%s)
  dur=$((end-start))
  # success heuristic: exit 0 AND no obvious failure markers
  if [ $rc -eq 0 ] && ! grep -qiE '(traceback|^error|❌|verification failed|timed out|assertion)' "$log"; then
    status="PASS"
  else
    status="FAIL(rc=$rc)"
  fi
  echo "=== [$i] $status $name (${dur}s) -> $log ===" | tee -a "$SUMMARY"
done < "$GOLD"

echo "" | tee -a "$SUMMARY"
echo "########## GOLD RUN COMPLETE ##########" | tee -a "$SUMMARY"
grep -E '^=== \[[0-9]+\] (PASS|FAIL)' "$SUMMARY" | tee -a "$SUMMARY".final
echo "PASS_COUNT=$(grep -cE '\] PASS ' "$SUMMARY")" | tee -a "$SUMMARY"
echo "FAIL_COUNT=$(grep -cE '\] FAIL' "$SUMMARY")" | tee -a "$SUMMARY"
