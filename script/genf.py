# genf.py

# Demo:
# python genf.py SLOPES='[3,4,5,6,7,8,9]'

# This script should generate a CSV file full of feature data
# from GSPC prices from Yahoo.

# SLOPES should specify moving-avg durations, in days, which I compute slopes from.
# I should have at least two SLOPE values and they should be between 2 and 32.

# If you have questions, e-me: bikle101@gmail.com

import numpy  as np
import pandas as pd
import pdb

# I should check cmd line arg
import sys
if (len(sys.argv) != 2):
  print('You typed something wrong:')
  print('Demo:')
  print("python genf.py SLOPES='[3,4,5,6,7,8,9]'")
  sys.exit()
arg1_l = sys.argv[1].split('=')
if (arg1_l[0] != 'SLOPES'):
  print('Problem:')
  print('I cannot determine SLOPES from your command line.')
  print('Demo:')
  print("python genf.py SLOPES='[3,4,5,6,7,8,9]'")
  sys.exit()

# I should get integers from arg1_l:
slopes_s = arg1_l[1]
slopes_a = []
for slope_s in slopes_s.split(','):
    slope_i = int(slope_s.replace('[','').replace(']',''))
    slopes_a.append(slope_i)

gspc_df = pd.read_csv('../public/csv/gspc2.csv')

# I should compute pctlead:
gspc_df['pctlead'] = (100.0 * (gspc_df.cp.shift(-1) - gspc_df.cp) / gspc_df.cp).fillna(0)

# I should compute mvgavg-slope for each slope_i

# ref:
# http://www.ml4.us/cclasses/class03pd41
# http://pandas.pydata.org/pandas-docs/stable/computation.html#rolling-windows
# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.rolling.html#pandas.DataFrame.rolling

for slope_i in slopes_a:
  rollx          = gspc_df.rolling(window=slope_i)
  col_s          = 'slope'+str(slope_i)
  slope_sr       = 100.0 * (rollx.mean().cp - rollx.mean().cp.shift(1))/rollx.mean().cp
  gspc_df[col_s] = slope_sr

# I should generate Date features:
dt_sr = pd.to_datetime(gspc_df.cdate)
dow_l = [float(dt.strftime('%w' ))/100.0 for dt in dt_sr]
moy_l = [float(dt.strftime('%-m'))/100.0 for dt in dt_sr]
dom_l = [float(dt.strftime('%-d'))/100.0 for dt in dt_sr]
wom_l = [round(dom/5)/10.0               for dom in dom_l]
gspc_df['dow'] = dow_l
gspc_df['moy'] = moy_l
# FAIL: gspc_df['wom'] = wom_l

# I should write to CSV file to be used later:
gspc_df.to_csv('../public/csv/feat.csv', float_format='%4.4f', index=False)
'bye'

