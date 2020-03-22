import pandas as pd


df = pd.read_csv("./tmp/tmp_all_data.csv").astype({"connection_hrs":float})
df.head()
print (df)


from pivottablejs import pivot_ui
pivot_ui(df,outfile_path='./output/ipivottablejs.html')
HTML('./output/pivottablejs.html')