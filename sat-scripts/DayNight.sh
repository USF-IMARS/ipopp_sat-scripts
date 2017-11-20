#/bin/bash
FIL1KM=$1
file_type=`file ${FIL1KM} | grep 'Hierarchical Data Format (version 4) data'`

echo ft: $file_type


if [ -n "$file_type" ]
then
	DAY_FLAG=`${MODIS_DB_HOME}/run/bin3/linux/ncdump_hdf -h ${FIL1KM} | grep "Day"`
else
	DAY_FLAG=`${MODIS_DB_HOME}/run/bin3/linux/h5dump -a /Data_Products/VIIRS-MOD-GEO-TC/VIIRS-MOD-GEO-TC_Gran_0/N_Day_Night_Flag ${FIL1KM} | grep  \"Day\"`
fi

echo df: $DAY_FLAG

if [ -n "$DAY_FLAG" ]
then
   LIGHT="DAY"
else
   LIGHT="NIGHT"
fi

echo "DayNightCheck = $LIGHT" > DayNightCheck.txt
