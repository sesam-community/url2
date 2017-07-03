# URL2
[![Build Status](https://travis-ci.org/sesam-community/url2.svg?branch=master)](https://travis-ci.org/sesam-community/url2)

A new url microservice that for now supports:

    FTP,
    SSH
    [GET] [POST]

    JSON Rest
    [GET]
of types:

    XML
    JSON

You can use it to fetch single or multiple files from a path:
It also supports saving files to a specific path.

##### Example System Config
```
{
  "_id": "url2-xml-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "protocol:"*protocol*",
      "hostname": "*hostname*",
      "username": "some_username",
      "password": "some_password"
      #optional
      "ftp_port": 21,
    },
    "image": "sesamcommunity/url2:latest",
    "port": 5000
  }
}
```

The microservice supports ssh protocol and ftp protocol for now.
If ftp is used you need to add ftp_port - it defaults to 21 if not defined.

##### FTP [GET] pipe config
```
{
  "_id": "some_pipe_id",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "url2-xml-service",
    "url": "/path/to/xml/file.xml?xml_path=customerRecords.customerRecord&updated_path=system.customerChangeDateTime&since=2001-12-17T09:30:47%2B02:00&delete_file=false",
    "or": "",
    "url": "/path/to/folder/?type=xml&xml_path=customerRecords.customerRecord&updated_path=system.customerChangeDateTime&since=2001-12-17T09:30:47%2B02:00&delete_file=true"
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
It supports updated path if it exists, if not; remove updated_path and since from url

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
will convert the sent json to xml (for now) and save it to a specific path - this example pipe config saves to  "/path/to/xml/file.xml"

##### Example System Config
```
{
  "_id": "url2-json-service",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "protocol:"json",
      "hostname": "http://se.api.anpdm.com:80/",
      "headers": "{'Accept':'application/json', 'token':'some_token'}",
      "page_number": "1",
      "page_size": "1000"
    },
    "image": "sesamcommunity/url2:latest",
    "port": 5000
  }
}
```

v1/someurl/page_number/page_size

page_number and page_size will be replaced by environment variables at startup.

    arguments needed :
    ?type=json
    &total_pages_path=path.to.totalPages

    optional arguments :
    &updated_path=Updated
    &entities_path=Result.Items
    &since=some_since

##### Returned Example entities
```
[
  {
    "Created": "/Date(1498831049247)/",
    "FolderId": 0,
    "Id": 1996084,
    "Name": "Test Mailinglist",
    "Updated": "/Date(1498831049247)/",
    "_updated": "/Date(1498831049247)/"
  },
  {
    "Created": "/Date(1498831306963)/",
    "FolderId": 0,
    "Id": 1996098,
    "Name": "Test Mailinglist",
    "Updated": "/Date(1498831306963)/",
    "_updated": "/Date(1498831306963)/"
  }
]
```
