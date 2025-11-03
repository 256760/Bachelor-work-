import configparser

config = configparser.ConfigParser()
config.read("config.ini")

db_user = config["mariadb"]["user"]
db_password = config["mariadb"]["password"]
db_url = config["mariadb"]["url"]

URL_PUBLIC = config["influxdb"]["url_public"]
TOKEN_PUBLIC_READ = config["influxdb"]["token_public_read"]
URL_INTERNAL = config["influxdb"]["url_internal"]
TOKEN_INTERNAL_READ = config["influxdb"]["token_internal_read"]
ORG = config["influxdb"]["org"]

CHMI_METADATA_CONNECTION_STRING = (
    f"mariadb+mariadbconnector://{db_user}:{db_password}@{db_url}/chmi_metadata"
)


CML_METADATA_CONNECTION_STRING = (
    f"mariadb+mariadbconnector://{db_user}:{db_password}@{db_url}/cml_metadata"
)
