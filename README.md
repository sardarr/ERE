# ERE


Requirements:

1)Clone all the directories and the "main_pipeline_tmp.py"

2)Run the Belief tagger on your txt files and copy the input data and CB tagger output in /input_txt and /belief_output directories. 
/ldc_ere contains the corresponding ERE files from the LDC data, which are used in creating the final ".best.xml" files.

Run the code from the root :

python main_pipeline_tmp.py

/Root
.
├── belief_output

│   └── 0a421343005f3241376fa01e1cb3c6fb.cmp.txt.xml "output from the belief tagger" 
 
├── input_txt

│   └── 0a421343005f3241376fa01e1cb3c6fb.cmp.txt "input txt files"

├── ldc_ere

│   └── 0a421343005f3241376fa01e1cb3c6fb.rich_ere.xml "ere file from the LDC data set"

├── main_pipeline_tmp.py	"python main_pipeline_tmp.py"

└── output

    └── 0a421343005f3241376fa01e1cb3c6fb.best.xml	"output .best.xml"
	