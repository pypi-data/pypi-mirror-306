from openanalytics.checklibs import pkg_install

pkg_install("influxdb-client")

import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from openanalytics.utils import flatten_dict
from openanalytics.connectors.ConnectorInterface import ConnectorInterface
from openanalytics.models import Identify, Log, Page, Token, Track
import logging
from openanalytics.version import APP_NAME


# docker run --name influxdb -p 8086:8086 -v ./data:/var/lib/influxdb2  -v ./config:/etc/influxdb2
# -e INFLUXDB_ADMIN_USER=admin
# -e INFLUXDB_ADMIN_PASSWORD=admin_123456
# -e INFLUXDB_USER=user
# -e INFLUXDB_USER_PASSWORD=admin_123456
# influxdb:latest


class InfluxDBConnector(ConnectorInterface):
    token: str
    org: int
    url: str
    bucket: str
    client: InfluxDBClient = None

    log = logging.getLogger(APP_NAME)

    def __init__(self, token: str, org: int, url: str, bucket: str):
        self.token = token
        self.org = org
        self.url = url
        self.bucket = bucket

    def _connect(self):
        self.client = influxdb_client.InfluxDBClient(
            url=self.url, token=self.token, org=self.org
        )
        self.log.debug("InfluxDB connection opened")

    def _disconnect(self):
        self.client.close()
        self.log.debug("InfluxDB connection closed")

    def _check_and_create_db(self):

        self._connect()
        databases = self.client.get_list_database()
        if self.dbname not in [db["name"] for db in databases]:
            self.client.create_database(self.dbname)

        self._disconnect()

    def _flattern_dict(self, data_dict) -> dict:
        _flat_metadata = flatten_dict(data_dict) if data_dict is not None else {}

        return _flat_metadata

    def _convert_to_data_point(self, data):

        _point = Point(data["type"])
        _point.measurement(data["type"])

        match data["type"]:
            case Identify.SIGNATURE:

                _point.tag("event", data["event"])
                _point.field("userId", data["userId"])

            case Log.SIGNATURE:

                _point.tag("level", data["level"])
                _point.tag("event", data["event"])
                _point.field("summary", data["summary"])

            case Page.SIGNATURE:

                _point.tag("name", data["name"])
                _point.tag("category", data["category"])
                _flat_data = self._flattern_dict(data["properties"])
                if _flat_data is not None or not {}:
                    for key, value in _flat_data.items():
                        _point.field(key, value)

            case Token.SIGNATURE:

                _point.tag("event", data["event"])
                _point.tag("action", data["action"])
                _point.field("count", data["count"])

            case Track.SIGNATURE:

                _point.tag("endpoint", data["endpoint"])
                _point.tag("event", data["event"])
                _flat_data = self._flattern_dict(data["properties"])
                if _flat_data is not None or not {}:
                    for key, value in _flat_data.items():
                        _point.field(key, value)

        _flat_metadata = self._flattern_dict(data["metadata"])
        if _flat_metadata is not None:
            for key, value in _flat_metadata.items():
                _point.field(key, value)

        print(data["timestamp"])
        _point.time(data["timestamp"])
        # _point.time(datetime.now())

        return _point

    def load(self, collection_name, msg) -> any:

        self._connect()
        point = self._convert_to_data_point(msg)
        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        result = write_api.write(bucket=self.bucket, org=self.org, record=point)
        write_api.flush()
        self.log.debug(f"{collection_name} - {msg} record inserted.")
        self._disconnect()

        return result

    def bulk_load(self, collection_name, msg) -> any:

        self._connect()
        points = []
        for record in msg:
            points.append(self._convert_to_data_point(record))

        write_api = self.client.write_api()
        result = write_api.write(bucket=self.bucket, org=self.org, record=points)

        write_api.flush()

        self._disconnect()

        self.log.debug(f"{collection_name} - {len(msg)} records inserted.")

        return result
