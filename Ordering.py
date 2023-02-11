import data_clean as dc
import aggregations as agg

testingFile = dc.open_file(r""".\data\Fall 2019 Event Info (Data Project).xlsx""")

sheets = dc.data_clean(testingFile, 2, 5, 10, 13)

testingSheet = sheets[('(12.11.19) Study pectacular', 'a')]

top_majors = agg.getCount(testingSheet, "Major")
top_year = agg.getCount(testingSheet, "Classification")
