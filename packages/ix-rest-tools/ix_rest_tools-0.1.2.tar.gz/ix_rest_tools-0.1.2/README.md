# ix_rest_tools
ix_rest_tools is a Python library for interacting with the iX Web Server API. This library provides methods to fetch and update tags on the iX Web Server.
Installation

Install the package from PyPI:
```
bash

pip install ix_rest_tools
```
Usage

To use the module, start by creating a requests.Session for your HTTP requests. This helps keep the connection alive across multiple requests, reducing overhead.
Import the Library
```
python

from ix_rest_tools import get_tags, get_value, get_values
import requests
```
Initialize a Session

Creating a session helps maintain an active connection to the server:
```
python

session = requests.Session()
```
Set up the Server URL

Define the base URL of your server. Replace your_server_ip_or_domain with the actual IP address or domain:
```
python

url = "your_server_ip_or_domain"
```
1. Fetch All Tags

To retrieve a list of all available tags:
```
python

tags = get_tags(url, session)

if tags:
    print("Tags:", tags)
else:
    print("Failed to retrieve tags.")
```

2. Fetch a Specific Tag Value

To retrieve the value of a specific tag:
```
python

tag_name = "example_tag_name"
value = get_value(url, tag_name, session)

if value:
    print(f"Value of {tag_name}:", value.json())  # or value.text if not JSON
else:
    print(f"Failed to retrieve value for tag {tag_name}.")
```

3. Fetch Multiple Tag Values in Batch

To retrieve multiple tag values in a single request, use get_values. You can specify process_values=True to return a dictionary of tag names and values, or False to return the raw response:
```
python

tags_to_get = ["tag1", "tag2", "tag3"]

# Process the values into a dictionary of tag name-value pairs
values = get_values(url, tags_to_get, session, process_values=True)

if values:
    print("Tag Values:", values)
else:
    print("Failed to retrieve tag values.")
```

Example Script

Here's an example that puts everything together:

```
python

from ix_rest_tools import get_tags, get_value, get_values
import requests

# Set up session and URL
session = requests.Session()
url = "your_server_ip_or_domain"

# Fetch all tags
all_tags = get_tags(url, session)
if all_tags:
    print("All Tags:", all_tags)
else:
    print("Failed to retrieve all tags.")

# Fetch a specific tag value
tag_name = "example_tag"
tag_value = get_value(url, tag_name, session)
if tag_value:
    print(f"Value of {tag_name}:", tag_value.json())
else:
    print(f"Failed to retrieve value for tag {tag_name}.")

# Fetch multiple tag values
tags_to_fetch = ["tag1", "tag2"]
tag_values = get_values(url, tags_to_fetch, session, process_values=True)
if tag_values:
    print("Tag Values:", tag_values)
else:
    print("Failed to retrieve tag values.")

```

Error Handling

Each function returns False if the request fails, allowing you to handle errors gracefully.
License


## Build instructions
Update version number in setup.py

```
python setup.py sdist bdist_wheel
```

```
twine upload dist/*
```

# license
This project is licensed under the MIT License.