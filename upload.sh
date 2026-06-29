#!/bin/bash

MAIN_PY="Main.py"
ROBOT_PY="terra_script.py"
RUN_DIR="runs"
OUTFILE="_output.py"

awk '/^from / || /^import /' $MAIN_PY >> $OUTFILE

cat $ROBOT_PY >> $OUTFILE

echo -e "\n\n" >> $OUTFILE
echo "run_data = [" >> $OUTFILE
for f in $(ls $RUN_DIR/*.txt | sort); do
  ESCAPED=$(grep -v '^[[:space:]]*//' "$f" | tr '\n' '#' | sed 's/"/\\\"/g')
  echo "  \"$ESCAPED\"," >> $OUTFILE
done
echo "]" >> $OUTFILE

echo -e "\n\n" >> $OUTFILE
awk '/run_data = \[\]/ {found=1; next} !found {next} {print}' $MAIN_PY >> $OUTFILE

python3.11 -m pybricksdev run ble $OUTFILE

rm $OUTFILE
