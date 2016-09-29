# ERE


This Script generates the *best.xml files, which can be used for evaluating the blief system.

Requirements:

1)After downloading the directories and *.py files you need to
  a)Copy your *.txt files in /input_src directory
  b)Run the Belief tagger on your source /input_src/*.txt files and copy the output data into /input_cb directory.
  c)/input_ere/ directory should contain all the corresponding *.ERE files from the LDC dataset. 

After running the script use the "python main_pipeline_new.py"  which generates the ".best.xml" files in /pred_out directory.





