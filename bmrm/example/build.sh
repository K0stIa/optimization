rm elps.h
rm elps_api.h
python setup.py build_ext --inplace
rm -r build
rm elps.cpp