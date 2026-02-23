#!/bin/bash
# Ralph Loop: Iterative Report Quality Test
# Generates comprehensive public report and saves for evaluation

CSV_FILE="custom_export_2026-02-01_2026-02-15.csv"
API_URL="http://localhost:8000/api/generate"
OUTPUT_DIR="ralph-loop-results"
ITERATION=${1:-1}

mkdir -p "$OUTPUT_DIR"

OUTFILE="$OUTPUT_DIR/iteration-${ITERATION}.md"
LOGFILE="$OUTPUT_DIR/iteration-${ITERATION}.log"

echo "[Ralph Loop] Iteration $ITERATION - $(date)" | tee "$LOGFILE"
echo "[Ralph Loop] Generating comprehensive public report..." | tee -a "$LOGFILE"

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -F "file=@${CSV_FILE}" \
  -F "report_type=public" \
  -F "report_format=comprehensive" \
  -F "use_ai=true" \
  -F "model=gpt-5.2-pro" \
  -F "report_grouping=repository" \
  -F "repo_limit=0" \
  -F "include_individuals=true" \
  "$API_URL")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

echo "[Ralph Loop] HTTP Status: $HTTP_CODE" | tee -a "$LOGFILE"

if [ "$HTTP_CODE" = "200" ]; then
  # Extract markdown from JSON response
  echo "$BODY" | python3 -c "
import json, sys
data = json.load(sys.stdin)
report = data.get('report', data.get('markdown', ''))
print(report)
" > "$OUTFILE" 2>/dev/null

  if [ -s "$OUTFILE" ]; then
    LINES=$(wc -l < "$OUTFILE")
    CHARS=$(wc -c < "$OUTFILE")
    echo "[Ralph Loop] ✅ Report saved: $OUTFILE ($LINES lines, $CHARS bytes)" | tee -a "$LOGFILE"
  else
    echo "$BODY" > "$OUTFILE"
    echo "[Ralph Loop] ⚠️ Raw response saved (couldn't parse JSON)" | tee -a "$LOGFILE"
  fi
else
  echo "$BODY" > "$LOGFILE.error"
  echo "[Ralph Loop] ❌ Failed with HTTP $HTTP_CODE" | tee -a "$LOGFILE"
fi
