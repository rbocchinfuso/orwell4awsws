#!/usr/bin/env python
"""orwellpivot.py: Create Pivot of AWS Workspaces Data"""

import pandas as pd
import numpy as np
import os
import glob
import pandas as pd

# owned
__author__ = 'Rich Bocchinfuso'
__copyright__ = 'Copyright 2020, Create Pivot of AWS Workspaces Data'
__credits__ = ['Rich Bocchinfuso']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = 'Rich Bocchinfuso'
__email__ = 'rbocchinfuso@gmail.com'
__status__ = 'Dev'

pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

html_string = '''
<html>
  <head><title>HTML Pandas Dataframe Pivot Report with CSS</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <body>
    {table}
  </body>
</html>.
'''

# set working directory
os.chdir("./output")

# find all csv files in the folder
# use glob pattern matching -> extension = 'csv'
# save result in list -> all_filenames
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# print(all_filenames)

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

# export to csv
combined_csv.to_csv( "../tmp/tmp_all_data.csv", index=False, encoding='utf-8-sig')

df = pd.read_csv("../tmp/tmp_all_data.csv").astype({"connection_hrs":float})
df.head()
print (df)


df["user_state"] = df["user_state"].astype("category")
df["user_state"].cat.set_categories(["ONLINE","OFFLINE"],inplace=True)

# pivot by date, user, user_state
table = pd.pivot_table(df.round(1),index=["log_datestamp","username"],values=["connection_hrs"], columns=["user_state"],aggfunc=[np.sum],fill_value=0)
print (table)

# render dataframe as html
with open('./reports/orwell_pivot_by_date.html', 'w') as f:
    f.write(html_string.format(table=table.to_html(classes='mystyle')))


# pivot by user, date, user_state
table = pd.pivot_table(df.round(1),index=["username","log_datestamp"],values=["connection_hrs"], columns=["user_state"],aggfunc=[np.sum],fill_value=0)
print (table)

# render dataframe as html
with open('./reports/orwell_pivot_by_user.html', 'w') as f:
    f.write(html_string.format(table=table.to_html(classes='mystyle')))


# pivot by user, date, user_state alternate view
table = pd.pivot_table(df.round(1),index=["username","user_state"],values=["connection_hrs"], columns=["log_datestamp"],aggfunc=[np.sum],fill_value=0)
print (table)

# render dataframe as html
with open('./reports/orwell_pivot_by_user_alt.html', 'w') as f:
    f.write(html_string.format(table=table.to_html(classes='mystyle')))


# pivot by user, date, user_state, hour
table = pd.pivot_table(df.round(1),index=["username","log_datestamp",'user_state'],values=["connection_hrs"], columns=["log_timestamp"],aggfunc=[np.sum],fill_value=0)
print (table)

# render dataframe as html
with open('./reports/orwell_pivot_by_hour.html', 'w') as f:
    f.write(html_string.format(table=table.to_html(classes='mystyle')))

