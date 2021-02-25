from filter_map.utils import inverse_mapping, get_applicable_filters

def test_inverse_mapping():
    _data = {'company': 'Aayulogic Pvt. Ltd', 'project': 'filter map'}

    inversed_data = inverse_mapping(_data)
    assert list(inversed_data.keys()) == list(_data.values()), 'Inversed keys must be equal to actual values'
    assert list(inversed_data.values()) == list(_data.keys()), 'Inversed values must be equal to actual keys'   


def test_get_applicable_filters():
    query_params = {
        'name': 'Aayulogic',
        'project': 'filter map'
    }

    filter_map = {
        'name': 'company.name',
        'project': 'company.project'
    }

    comparision_data = {
        'company.name': 'Aayulogic', 
        'company.project': 'filter map'
    }

    _filter_ready_data = get_applicable_filters(query_params, filter_map)

    assert _filter_ready_data == comparision_data, 'Data returned must be ready to be passed in filter method'
