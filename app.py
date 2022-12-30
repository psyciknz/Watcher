from flask import Flask, request,  render_template
import os
import influxdb
from influxdb import InfluxDBClient
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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

@app.route("/watch")
def influx_watch():
    host=os.getenv('INFLUX_HOST')
    port=os.getenv('INFLUX_PORT')
    username=os.getenv('INFLUX_USER')
    password=os.getenv('INFLUX_PWD')
    database=os.getenv('INFLUX_DB')

    cli = InfluxDBClient(host=host,port=port,username=username,
                password=password,database=database)

    result = cli.query("select time,title,tmdb_id, url,poster_html from watch where time > now() - 30d and type = 'movie'")
    return render_template("movies.html", movies=result)
#def influx_watch():
    

    

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("APP_SERVER_PORT")))
