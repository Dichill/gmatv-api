@echo off
echo [Debug-Info] Cleaning Files...
cd data/json
echo [Debug-Busy] Going into Directory...
DEL *json
echo [Debug-Info] Deleting every *.json files.
echo [Debug-Finished] Cleaning Complete, executing python file.
cd ../../
python test.py