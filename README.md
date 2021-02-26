# FilterMapBackend

![Test Status](https://github.com/aayulogic/filtermapbackend/actions/workflows/tests.yml/badge.svg?branch=master)

## Table Of Content
* [Introduction](#introduction)
* [Installation](#installation)  
* [Usage](#usage)  
* [TODOS](#todos)

## Introduction

FilterMapBackend is FilterBackend  like DjangoFilterBackend

## Installation
### Using pip
Currently, drf-filtermapbackend is not released to PYPI. \
So you can only install
it directly from github by running
```shell
pip install git+https://github.com/aayulogic/filtermapbackend@master
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
Example Usage
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

## TODOS
1. Add test cases for FilterMapBackend
2. Update Readme
