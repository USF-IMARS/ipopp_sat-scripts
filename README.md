# sat-scripts
port of IMaRS IPOPP stations with human-readable documentation

Files are currently being ported in from each of our IPOPP SPAs following [this guide](https://github.com/USF-IMARS/IPOPP-docs/blob/master/docs/understanding-an-algorithm.md).

Each SPA repo that is being ported should have a git branch called `port`. 
This branch is used to track the status of the port.
Files are deleted from the branch when they are determined to contain no remaining information to port over.
Example: [imars spa port branch](https://github.com/USF-IMARS/imars/tree/port).


## port status 

A rough status of the port is below:

-----------------------------------------------------------

*legend*
* :hourglass: in-progress
* :white_check_mark: done
* :no_entry_sign: fail

------------------------------------------------------------

* :hourglass: [IMaRS SPA](https://github.com/USF-IMARS/imars/tree/port)
    * :hourglass: oc_png
        * :white_check_mark: PngGenerator.py
* :hourglass: [seadas SPA](https://github.com/USF-IMARS/seadas_spa/tree/port)
    * :hourglass: modis_oc
    
