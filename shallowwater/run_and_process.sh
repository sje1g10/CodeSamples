# run_and_process.sh
#  Run the shallow water dam break simulation and process the results

echo 'Beginning simulation...'
python run.py
echo 
echo 'Processing results...'
echo
./process_results.sh
