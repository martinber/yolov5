#!/bin/bash
python3 ./create_idl.py ./runs/detect/exp/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/abandonedBox/ ./runs/full_filt_idl/abandonedBox.idl
python3 ./create_idl.py ./runs/detect/exp2/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/backdoor/ ./runs/full_filt_idl/backdoor.idl
python3 ./create_idl.py ./runs/detect/exp3/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/badminton/ ./runs/full_filt_idl/badminton.idl
python3 ./create_idl.py ./runs/detect/exp4/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/busStation/ ./runs/full_filt_idl/busStation.idl
python3 ./create_idl.py ./runs/detect/exp5/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/copyMachine/ ./runs/full_filt_idl/copyMachine.idl
python3 ./create_idl.py ./runs/detect/exp6/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/cubicle/ ./runs/full_filt_idl/cubicle.idl
python3 ./create_idl.py ./runs/detect/exp7/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/fall/ ./runs/full_filt_idl/fall.idl
python3 ./create_idl.py ./runs/detect/exp8/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/office/ ./runs/full_filt_idl/office.idl
python3 ./create_idl.py ./runs/detect/exp9/labels/ ~/extra/async/ipcv/pdbr/labs/2/datasets/overpass/ ./runs/full_filt_idl/overpass.idl
