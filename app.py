from src import app, db
from meinheld import server # mainheld server
from backup import *

if __name__ == '__main__':
    #app.run(debug=True)
    server.listen("0.0.0.0")
    server.run(app)