# Open-Analytics
## An open-source analytical data capturing pacakge.

Open-Analytics lib enables you to capture and track analyitical data of your application at real-time into your own data-source. You can use your own or open-source tools to visualize the capture data.

## Installation

Install the dependencies and devDependencies and start the server.

```sh
pip install open-analytics
```

## Initalize
```sh
from openanalytics.client import Client
```
```sh
client = Client(connector=connector, sync_mode=False, debug=True)
```

## Connecting to data-source
As of now the open-analytics library provide Connector Plugins for three types of databases.

#### MongoDBConnector
```sh
from openanalytics.connectors.MongoDBConnector import MongoDBConnector
connector = MongoDBConnector(host="mongodb://localhost:27017/", dbname="demobucket")
```

#### InfluxDBConnector
```sh
from openanalytics.connectors.InfluxDBConnector import InfluxDBConnector
connector = InfluxDBConnector(
    token="5wttcrwYX3COT8OQaorbOKUYAmPPNE-7oC_2itF60bBqIfC33L9g4k3APNjcCkCAuBuwWurOVEBo6gNYP0cAuA==",
    org="demoorg",
    url="http://localhost:8086",
    bucket="demobucket",
)
```

#### SQLiteConnector
```sh
from openanalytics.connectors.SQLiteConnector import SQLiteConnector
connector = SQLiteConnector(db="handshake.sqlite3")
```

## Features

### Identify
The Identify method lets you tie a user to their actions and record traits about them. It includes a unique User ID and any optional traits you know about them.
```sh
from openanalytics.models.Identify import Identify
```
```sh
client.idetify(
    Identify(
        userID="UserName / UserEmail", 
        event="Custom Event", 
        metadata={"data": "query data", "location": "query location"},
        timestamp=datetime.now(timezone.utc),
    )
)
```

### Token
Useful in Generative AI token processing. The Token method lets you record token utlization for you events, along with optional extra information about the token processing.
```sh
from openanalytics.models.Token import Token
```
```sh
client.token(
    Token(
        event="LLM Query Event",
        action="Similarity Search",
        count=134,
        metadata={
            "query": "llm prompt",
            "location": {"context": "context of the prompt", "rag": "enabled"},
        },
    )
)
```

### Track
Track lets you record the actions your users perform. Every action triggers what open-analytics calls an “event”, which can also have associated properties.
```sh
from openanalytics.models.Track import Track
```
```sh
client.track(
    Track(
        endpoint="http:localhost:8080/search",
        event="Profile Search",
        properties={"params": "q=username"},
        timestamp=datetime.now(timezone.utc),
    )
)
```

### Page
The Page method lets you record page views on your website, along with optional extra information about the page being viewed.
```sh
from openanalytics.models.Page import Page
```
```sh
client.page(
    Page(
        name="Dashboard", 
        category="AdminGroup", 
        properties={"status": True}
    )
)
```

### Logger
The Log method lets you record log events of your actions, along with optional extra information about the log event.
```sh
from openanalytics.models.Logger import Logger
```
```sh
client.logger(
    Log(
        summary="Log Message",
        level="Debug",
        event="Process Login Function",
        metadata={"user": "username"},
    )
)
```

## License

Apache License v2.0
