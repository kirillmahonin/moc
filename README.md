MOC generation tool (Python 3 script)
===

This tool recursively searches for .h files, that contain Q_OBJECT macroses. If the files were found they will be modified. #include with a MOC file will be added at the end of the file or after //MOC string
