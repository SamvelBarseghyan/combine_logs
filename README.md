**Warning:**

    Before running script and passing as argument path to directory with log files, check that content of '.log' files are 
    sorted and validated, because of in example files given by interviewer, some files are not sorted and some lines 
    wasn't containt timestamps, but according to the rules of the task they should be sorted and whole lines should contain
    timestamps.

**Description:**
    
For running script use:

    python solution_1 "path_to_dir"
    python solution_2 "path_to_dir"

After running scripts in the current directory script will create files:
    
1. combined_logs.log -> if "solution_1.py" was used
2. combined_logs_file.log -> if "solution_2.py" was used
