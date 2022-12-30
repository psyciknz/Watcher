from flask import Flask, request,  render_template
import os
import influxdb
from influxdb import InfluxDBClient
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def hello_world():
    port =os.getenv('APP_SERVER_PORT')
    return f'<p><a href="tv">TV</a></p> \
        <a href="movies">Movies</a>'


@app.route("/influx")
def influx_health():
    host=os.getenv('INFLUX_HOST')
    port=os.getenv('INFLUX_PORT')
    username=os.getenv('INFLUX_USER')
    password=os.getenv('INFLUX_PWD')
    database=os.getenv('INFLUX_DB')

    cli = InfluxDBClient(host=host,port=port,username=username,
                password=password,database=database)

    def check_db_status():
        # if the db is not found, then try to create it
        try:
            dblist = cli.get_list_database()
            db_found = False
            for db in dblist:
                if db['name'] == database:
                    db_found = True
            if not(db_found):
                print('Database <%s> not found, trying to create it', database)
                cli.create_database(database)
            return True
        except Exception as e:
            print('Error querying open-nti database: %s', e)
            return False 

    status = check_db_status()

    return "<p>MongoDB health check: {}</p>".format(status)
#def influx_health():

@app.route("/movies")
def influx_watch_movies():
    host=os.getenv('INFLUX_HOST')
    port=os.getenv('INFLUX_PORT')
    username=os.getenv('INFLUX_USER')
    password=os.getenv('INFLUX_PWD')
    database=os.getenv('INFLUX_DB')

    cli = InfluxDBClient(host=host,port=port,username=username,
                password=password,database=database)

    tabledata = cli.query("select time,title,tmdb_id, url,poster_html from watch \
        where time > now() - 30d and type = 'movie' \
            order by time desc")
    data_points = []
    for measurement, tags in tabledata.keys():
        for p in tabledata.get_points(measurement=measurement, tags=tags):
            data_points.append(p)

    #records = tabledata.get_points('watch')
    #movies=list(records)
    #for record in movies:
    #    print(record[0])
    #records = result.items()[0]
    return render_template("movies_bootstrap.html",title="Movies", measurement="watch",
        columns=["time","title","tmdb_id","url","poster_html"],
        points=data_points)
#def influx_watch():

@app.route("/tv")
def influx_watch_tv():
    host=os.getenv('INFLUX_HOST')
    port=os.getenv('INFLUX_PORT')
    username=os.getenv('INFLUX_USER')
    password=os.getenv('INFLUX_PWD')
    database=os.getenv('INFLUX_DB')

    cli = InfluxDBClient(host=host,port=port,username=username,
                password=password,database=database)

    tabledata = cli.query("select time,/show/,season, episode,title,episode_url,url \
            from watch where time > now() - 30d and type = 'episode' \
                order by time desc")
    data_points = []
    for measurement, tags in tabledata.keys():
        for p in tabledata.get_points(measurement=measurement, tags=tags):
            data_points.append(p)

    #records = tabledata.get_points('watch')
    #movies=list(records)
    #for record in movies:
    #    print(record[0])
    #records = result.items()[0]
    return render_template("tv_bootstrap.html",title="TV", measurement="watch",
        columns=["time","show","season","episode","title","episode_url","url"],
        points=data_points)
#def influx_watch():
    

    

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("APP_SERVER_PORT")))
