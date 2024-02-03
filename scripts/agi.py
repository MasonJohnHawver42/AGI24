import csv
import plotly.graph_objects as go
from datetime import datetime, timedelta

DATACSV = "./data/Data.csv"
TOTAL_APPS = 900039258


def main():
    with open(DATACSV) as data:
        reader = csv.reader(data, delimiter=',', quotechar='|')
        
        header_row = next(reader)
        header = { i:name for name, i in enumerate(header_row) }

        app_count_graph(reader, header)


def app_count_graph(reader, header, past=365, res=30):
    date_applied = []
    miss = 0

    i = 0
    for row in reader:
        res = row[header["api_applications_created"]]
        try:
            date_applied.append(int(res))
        except:
            miss += 1
        
        # if i > 100:
        #     break
    
    date_applied = sorted(date_applied)
    print(miss)

    start_unix = date_applied[0]
    start_date = datetime.utcfromtimestamp(start_unix) + timedelta(days=past)

    end_unix = date_applied[-1]
    end_date = datetime.utcfromtimestamp(start_unix)

    print(start_date, end_date)
    print(start_unix, end_unix)

    x = []
    y = []

    curr = start_date

    while curr <= end_date:

        print(curr)

        i = 0
        count = 0

        while i < len(date_applied) and datetime.utcfromtimestamp(date_applied[i]) < curr:
            if datetime.utcfromtimestamp(date_applied[i]) + timedelta(days=past) >= curr:
                count += 1
            i += 1

        x.append(curr)
        y.append(count)

        curr += timedelta(days=res)

    print(x[:10])
    print(y[:10])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Scatter'))
    fig.update_layout(title='Scatter Chart with Dates and Counts', xaxis_title='Date', yaxis_title='Count')

    fig.write_html("app_over_time.html")



main()