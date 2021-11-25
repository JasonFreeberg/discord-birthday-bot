# Pytest has a hard time finding the utils module when executing the main.main() method, apparently 
# this fixes the import resolution issue: https://stackoverflow.com/a/53248845/10265855
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
