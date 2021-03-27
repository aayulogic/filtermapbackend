from collections import OrderedDict
from typing import Union, Type, Tuple, List, ValuesView

from django.db.models import QuerySet
from django.forms.utils import pretty_name
from django.template import loader
from django_filters import utils as dj_filters_utils
from django_filters.rest_framework import FilterSet
from rest_framework.filters import BaseFilterBackend
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView

from .utils import inverse_mapping, get_applicable_filters


class FilterMapFilterSet(FilterSet):
    """
    FilterSet used in FilterMapBackend

    Nothing much here, just uses get_applicable_filters filter queryset
    instead of default one
    """

    class Meta:
        fil_map = {}

    def filter_queryset(self, queryset: QuerySet) -> QuerySet:
        """
        Override filter queryset to use our own get_applicable_filters
        """
        cleaned_data = self.form.cleaned_data
        return queryset.filter(
            **get_applicable_filters(cleaned_data, self.Meta.fil_map)
        )


class FilterMapBackend(BaseFilterBackend):
    """
    Filter map backend

    Filter Map
    ----------

    Provide filter map in view

    .. code-block:: python

        filter_map = {'name' : 'filter_expression', ...}
        OR
        define get_filter_map

    Raise Exception
    ---------------

    Raise exception when validation of query_params fails
    default is True

    .. code-block:: python

        raise_filter_exception=True
        or
        define get_raise_filter_exception

    """
    template = 'filter_map/form.html'

    def get_raise_exception(self, view: GenericAPIView) -> bool:
        """Should return True/False, decides to raise ValidationError when bad data are sent to filter"""
        if hasattr(view, "get_raise_filter_exception"):
            return view.get_raise_filter_exception()
        return getattr(view, "raise_filter_exception", True)

    def get_filterset(self, request: Request, queryset: QuerySet, view: GenericAPIView) -> Union[FilterSet, None]:
        """
        Returns filterset instance
        """
        filterset_class = self.get_filterset_class(view, self.get_filter_map(view))
        if filterset_class is None:
            return None
        kwargs = self.get_filterset_kwargs(request, queryset)
        return filterset_class(**kwargs)

    @staticmethod
    def get_filterset_kwargs(request: Request, queryset: QuerySet) -> dict:
        """
        Returns kwargs for instantiating filterset
        """
        return {
            'data': request.query_params,
            'queryset': queryset,
            'request': request,
        }

    def filter_queryset(self, request: Request, queryset: QuerySet, view: GenericAPIView) -> QuerySet:
        """
        Return a filtered queryset
        """
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset

        if not filterset.is_valid() and self.get_raise_exception(view):
            raise dj_filters_utils.translate_validation(filterset.errors)
        return filterset.qs

    @staticmethod
    def get_filter_map(view: GenericAPIView) -> Union[dict, None]:
        """Get filter map from view instance"""
        filter_map_func = getattr(view, 'get_filter_map', None)
        filter_map_var = getattr(view, 'filter_map', None)

        if not (filter_map_func or filter_map_var):
            return None

        if filter_map_func:
            return filter_map_func()

        if filter_map_var:
            return filter_map_var

    def to_html(self, request: Request, queryset: QuerySet, view: GenericAPIView) -> str:
        """Render filter map to html form fields"""
        filter_map = self.get_filter_map(view)
        if filter_map:
            template = loader.get_template(self.template)
            return template.render({
                'filter': self.get_filterset_class(view, filter_map)(**self.get_filterset_kwargs(
                    request, queryset))
            })
        else:
            return ''

    @staticmethod
    def get_filterset_class(view: GenericAPIView, filter_map: dict) -> Type[FilterMapFilterSet]:
        """
        build own filterset class for the filter
        """
        model_class = view.get_queryset().model
        filter_map = filter_map or dict()

        # plain filter map, no tuples
        plain_filter_map = {key: "__".join(val) if isinstance(val, tuple) else val for key, val in
                            filter_map.items()}

        class Filterset(FilterMapFilterSet):
            class Meta:
                model = model_class
                # clean filed map for proper fields with expressions
                fields = FilterMapBackend.clean_field_names(
                    filter_map.values())
                fil_map = plain_filter_map

            def get_form_class(self):
                val_to_name = inverse_mapping(plain_filter_map)
                fields = OrderedDict()

                for name, filter_ in self.filters.items():
                    f = filter_.field

                    # set label for field using filter_map
                    # eg. if map is {"name": "profile__name"} then set label to "Name", by default it is "Profile Name"
                    f.label = pretty_name(val_to_name[name])

                    fields.update({val_to_name[name]: f})

                return type(str('%sForm' % self.__class__.__name__),
                            (self._meta.form,), fields)

        return Filterset

    @staticmethod
    def clean_field_names(field_names: Union[ValuesView, list]) -> dict:
        """Clean field names from query string to (field_name, expression) form"""
        real_fields = set()
        map_ = dict()
        filters = dict()
        for field_name in field_names:
            real_name, op = FilterMapBackend.clean_field_name(field_name)
            map_.update({field_name: op})
            real_fields.add(real_name)

        for real_name in real_fields:
            ops = set()
            for field_name, op in map_.items():
                if real_name in field_name:
                    ops.update(op)

            filters.update({real_name: ops})
        return filters

    @staticmethod
    def clean_field_name(field_name: Union[str, tuple]) -> Tuple[str, List[str]]:
        """
        Clean field name: Convert field expression to ("field_name", ["operation"])
        """
        if isinstance(field_name, tuple):
            return field_name[0], [field_name[1]]

        # just these for now, add more when needed
        ops = ["date__gte", "date__lte", "gte", "lte", "gt", "lt"]
        for op in ops:
            if f"__{op}" in field_name:
                return field_name.replace(f"__{op}", ""), [op]
        return field_name, ['exact']
