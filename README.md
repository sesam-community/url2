# URL2
[![Build Status](https://travis-ci.org/sesam-community/url2.svg?branch=master)](https://travis-ci.org/sesam-community/url2)

A new url microservice that for now supports:

    FTP
    [GET] [POST]

##### Example System Config
```
{
  "_id": "url2-xml-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      #FTP [GET xml-to-json][POST json-to-xml]
      "protocol:"ftp",
      "ftp_server": "some.ftp.server",
      "ftp_port": 21,
      "username": "some_username",
      "password": "some_password"
      #Other Systems coming soon
    },
    "image": "sesamcommunity/url2:latest",
    "port": 5000
  }
}
```

##### FTP [GET] pipe config
```
{
  "_id": "some_pipe_id",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "url2-xml-service",
    "url": "/path/to/xml/file.xml?parser=xml&xml_path=some_path&delete_file=false",
    "or": "",
    "url": "/path/to/folder/?parser=xml&xml_path=some_path&delete_file=true"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["add", "_id","path.to.id"],
        ["copy", "*"]
      ]
    }
  }
}
```

##### RETURNED example entity
```
[
    {
        "xml_converted":"to_json",
        "foo": "bar"
    },
    {
        "xml_converted":"to_json",
        "foo": "baz"
    }
]
```

##### FTP [POST] pipe config
```
{
  "_id": "some_pipe_id",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "some_dataset"
  },
  "sink": {
    "type": "json",
    "system": "url2-xml-service",
    "url": "/path/to/xml/file.xml"
  }
}

```
will convert your received json and convert it to xml for example.