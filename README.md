# FilterMapBackend

![Test Status](https://github.com/aayulogic/filtermapbackend/actions/workflows/tests.yml/badge.svg?branch=master)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPI version](https://badge.fury.io/py/drf-filtermapbackend.svg)](https://badge.fury.io/py/drf-filtermapbackend)

## Table Of Content
* [Introduction](#introduction)
* [Installation](#installation)  
* [Usage](#usage)  

## Introduction
FilterBackend which takes mapping of query params to field name.

It takes the query_param to filter map and enables filter option in list view.

## Installation
Install `drf-filtermapbackend` using
```shell
pip install drf-filtermapbackend
```
Then include `filter_map` in your installed apps
```python
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'filter_map',
    ...
]
```

## Usage
You can use FilterMapBackend by adding it to your filter backends and setting filter_map attribute.
For example
```python
from rest_framework.viewsets import ModelViewSet
from filter_map.backends import FilterMapBackend

class ProfileViewSet(ModelViewSet):
    """
    Consider Profile Model has user FK,
    """
    queryset = ...
    serializer_class = ...
    filter_backends = (FilterMapBackend,)
    filter_map = {
        # plain map
        'first_name': 'user__first_name',
        
        # used with lte operator
        'joined_before': 'date_joined__date__lte',
        
        # also supports separate field name and operator 
        'last_name': ('user__last_name', 'iexact'),
    }
    
```

You can also define `get_filter_map` method to return the filter map.
This will allow you to change filter_map in runtime. Here's an example

```python
from rest_framework.viewsets import ModelViewSet
from filter_map.backends import FilterMapBackend

class ProfileViewSet(ModelViewSet):
    """
    Consider Profile Model has user FK,
    """
    queryset = ...
    serializer_class = ...
    filter_backends = (FilterMapBackend,)
    
    def get_filter_map(self):
        # Disable joined_before filter for non staff users
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return {
                'first_name': 'user__first_name',
                'joined_before': 'date_joined__date__lte',
                'last_name': ('user__last_name', 'iexact'),
            }
        else:
            return {
                'first_name': 'user__first_name',
                'last_name': ('user__last_name', 'iexact'),
            }
            
```
