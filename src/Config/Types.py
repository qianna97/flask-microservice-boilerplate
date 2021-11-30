import os


SERVICE_NAME = os.environ['SERVICE_NAME']

# App Config
SECRET_KEY 	 = "ae0d1f37049f90405e5533a1b78168d16db1b1e258c8a0bb85fce05ad74c16ca45e93b66f9916a1c1948c6601fd8986398b659f2629a0bc8c6c6ba879cb52c31"

# Database Config
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{dbUserName}:{dbPassword}@{dbHost}/{dbName}".format(
	dbUserName=os.environ['POSTGRES_USER'],
	dbPassword=os.environ['POSTGRES_PASSWORD'],
	dbHost=os.environ['DBHOST'],
	dbName=os.environ['POSTGRES_DB']
)

# redis url
REDIS_BROKER_URL = os.environ['REDIS_BROKER_URL']
REDIS_BROKER_RESULT = os.environ['REDIS_BROKER_RESULT']
REDIS_CACHE_URL = os.environ['REDIS_CACHE_URL']

ENV = os.environ['ENV']