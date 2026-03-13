# Calculate number of days since 1850 for ISMIP7 time recording
from datetime import date
import csv
import netCDF4 as nc
import numpy as np

# CSV data header
data = [
    ['year', 'start', 'mid', 'end'],
]

# Define the start date (Jan 1, 1850)
start_date = date(1850, 1, 1)

for yr in range(1850,2301,1):
    
    # get current date
    yrstart = date(yr,1,1)
    yrmid = date(yr,7,1)
    yrend = date(yr+1,1,1)

    # Calculate the difference
    delta_start = yrstart - start_date
    delta_mid = yrmid - start_date
    delta_end = yrend - start_date
    
    # Print bounds
    #print(delta_start.days, delta_end.days)
    #print(delta_start.days, delta_mid.days, delta_end.days)
    #print(delta_mid.days)

    data.append([yr, delta_start.days, delta_mid.days, delta_end.days])


# Write csv
with open('days-since-1850.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write all rows at once
    writer.writerows(data)

    
# Write netcdf for state variable: snapshots at end of the year
file_path = 'days-since-1850_ST.nc'
ds = nc.Dataset(file_path, 'w', format='NETCDF4')
ds.createDimension('time', None)
# Variables
time = ds.createVariable('time', 'int32', ('time'), zlib=True)
year = ds.createVariable('year', 'int32', ('time'), zlib=True)
# Attributes
ds.description = 'Time encoding for ISMIP7 state variables, snapshots at end of year'
time.units = 'days since 1850-01-01 00:00:00'
time.calendar = 'standard'
# assign data
dataout = np.array(data)
time[:] = dataout[1:,2]
year[:] = dataout[1:,0]
# close file
ds.close()


# Write netcdf for fluxes: annual averages assigned to middle of the year, bounds
file_path = 'days-since-1850_FL.nc'
ds = nc.Dataset(file_path, 'w', format='NETCDF4')
ds.createDimension('time', None)
ds.createDimension('two', 2)
# Variables
time = ds.createVariable('time', 'int32', ('time'), zlib=True)
time_bnds = ds.createVariable('time_bnds', 'int32', ('time','two'), zlib=True)
year = ds.createVariable('year', 'int32', ('time'), zlib=True)
# Attributes
ds.description = 'Time encoding for ISMIP7 flux variables, yearly averages registered to middle of the year'
time.units = 'days since 1850-01-01 00:00:00'
time_bnds.units = 'days since 1850-01-01 00:00:00'
time.calendar = 'standard'

# assign data
dataout = np.array(data)
time[:] = dataout[1:,2]
time_bnds[:,:] = dataout[1:,[1,3]]
year[:] = dataout[1:,0]

# close file
ds.close()
