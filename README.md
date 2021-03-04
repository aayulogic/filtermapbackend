# FilterMapBackend

![Test Status](https://github.com/aayulogic/filtermapbackend/actions/workflows/tests.yml/badge.svg?branch=master)

## Table Of Content
* [Introduction](#introduction)
* [Installation](#installation)  
* [Usage](#usage)  

## Introduction
FilterBackend which takes mapping of query params to field name.

It takes the query_param to filter map and enables filter option in list view.

## Installation
### Using pip
Currently, drf-filtermapbackend is not released to PYPI. \
So you can only install
it directly from github by running
```shell
pip install https://github.com/aayulogic/filtermapbackend/archive/master.zip
```
### Build using setup.py
1. Clone the repo
```shell
git clone https://github.com/aayulogic/filtermapbackend
cd filtermapbackend
```
2. Install requirements
```shell
pip install -r requirementst.txt
```
3. Install using `setup.py`
```shell
python setup.py install
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
