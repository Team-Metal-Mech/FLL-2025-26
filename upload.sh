#!/bin/bash

MAIN_PY="main.py"
ROBOT_PY="hemabot.py"
RUN_DIR="runs"
OUTFILE="_output.py"

awk '/^from / || /^import /' $MAIN_PY >> $OUTFILE

cat $ROBOT_PY >> $OUTFILE

echo -e "\n\n" >> $OUTFILE
echo "run_data = [" >> $OUTFILE
for f in $(ls $RUN_DIR/*.txt | sort); do
  ESCAPED=$(tr '\n' '#' < "$f" | sed 's/"/\\\"/g')
  echo "  \"$ESCAPED\"," >> $OUTFILE
done
echo "]" >> $OUTFILE

echo -e "\n\n" >> $OUTFILE
awk '/run_data = \[\]/ {found=1; next} !found {next} {print}' $MAIN_PY >> $OUTFILE

pybricksdev run ble $OUTFILE

rm $OUTFILE
