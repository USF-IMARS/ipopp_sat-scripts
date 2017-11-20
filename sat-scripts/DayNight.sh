#/bin/bash
#
# writes "DAY" or "NIGHT" to DayNightCheck.txt based on given geo_file.
#
# Parameters:
# ------------------
# geo_file : mxd03 file path like M{Y,O}D03.17234044500.hdf
#    the file we want to check
# Environment Variables:
# MODIS_DB_HOME="/home/ipopp/drl/SPA/seadas7.3/algorithm"
#
# <Ncs_set name="geo_file" value="{drl.{sat}.modis.mxd03}"/>
# <Ncs_set name="data_file" value="{drl.{sat}.modis.mxd021km}"/>
# <Ncs_set name="output_file" value="{imars.{sat}.modis.oc}"/>
#
# Ported from [IMaRS Seadas SPA](https://github.com/USF-IMARS/seadas_spa)
#     * SPA=seadas
#     * station=modis_oc station [cfgfile](https://github.com/USF-IMARS/seadas_spa/blob/port/station/modis_oc/station.cfgfile)
#     * algorithm=DayNight
#         * [generic.xml](https://github.com/USF-IMARS/seadas_spa/blob/port/wrapper/oc/generic.xml)
#         * [installation.xml](https://github.com/USF-IMARS/seadas_spa/blob/port/wrapper/oc/installation.xml)


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
