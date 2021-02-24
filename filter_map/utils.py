
import datetime
import pytz

def inverse_mapping(mapping):
    """
    Inverse key -> value to value -> key
    # NOTE: make sure values are unique
    """
    return mapping.__class__(map(reversed, mapping.items()))


def get_applicable_filters(qp, filter_map):
    """
    get applicable filters from filter map,

    :param qp: query params
    :type qp: dict
    :param filter_map: filter map
    :type filter_map: dict
    :return: dictionary ready to be passed in filter method
    """
    query_params = {k: v for k, v in qp.items()}
    start = query_params.pop('start_date', '')
    end = query_params.pop('end_date', '')

    approved = query_params.pop('approved', ' ')
    if approved and approved in ['true', 'True', '1']:
        query_params.update({
            'approved': True
        })
    elif approved and approved in ['false', 'False', '0']:
        query_params.update({
            'approved': False
        })

    if start:
        if isinstance(start, datetime.date):
            query_params.update({
                'start_date': start
            })
        else:
            try:
                start_date = datetime.datetime.strptime(
                    start, '%Y-%m-%d'
                ).replace(tzinfo=pytz.utc)
                query_params.update({
                    'start_date': start_date
                })
            except ValueError:
                pass

    if end:
        if isinstance(end, datetime.date):
            query_params.update({
                'end_date': end
            })
        else:
            try:
                end_date = datetime.datetime.strptime(
                    end, '%Y-%m-%d'
                ).replace(tzinfo=pytz.utc)
                query_params.update({
                    'end_date': end_date
                })
            except ValueError:
                pass
    return {
        filter_map.get(k): v for k, v in query_params.items() if
        k in filter_map.keys() and v is not None and v != ''
    }
