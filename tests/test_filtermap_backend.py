from unittest import TestCase
from unittest.mock import patch

from django import forms
from django.http import HttpRequest
from rest_framework.request import Request

from filter_map.backends import FilterMapBackend, FilterMapFilterSet
from tests.utils import GENDER_CHOICES, ProfileQuerySet, ViewClass


class FilterMapBackendTestCase(TestCase):

    def test_clean_field_name(self):
        cases = [
            # input, expected_output

            # field name only
            ("field_name", ("field_name", ['exact'])),

            # field_name__exp
            ("field_name__date__gte", ("field_name", ['date__gte'])),
            ("field_name__date__lte", ("field_name", ['date__lte'])),
            ("field_name__gte", ("field_name", ["gte"])),
            ("field_name__lte", ("field_name", ["lte"])),
            ("field_name__gt", ("field_name", ["gt"])),
            ("field_name__lt", ("field_name", ["lt"])),
            ("field_name__isnull", ("field_name", ["isnull"])),

            # tuple
            (("field_name", "exp"), ("field_name", ["exp"]))

        ]

        for input_value, expected_output in cases:
            output = FilterMapBackend.clean_field_name(input_value)
            self.assertEqual(output, expected_output)

    def test_clean_field_names(self):
        input_values = [
            "field_name0",
            "field_name1__date__gte",
            "field_name2__lte",
            ("field_name3", "iexact"),
            "field_name4__isnull"
        ]
        expected_output = {
            "field_name0": {"exact"},
            "field_name1": {"date__gte"},
            "field_name2": {"lte"},
            "field_name3": {"iexact"},
            "field_name4": {"isnull"},
        }
        output = FilterMapBackend.clean_field_names(input_values)
        self.assertEqual(output, expected_output)

    def test_get_filterset_class(self):
        view = ViewClass()
        filter_map = {
            "first_name": "user__first_name",
            "gender": "gender"
        }
        filterset_class = FilterMapBackend.get_filterset_class(view, filter_map)
        self.assertEqual(filterset_class.Meta.fil_map, filter_map)

        # test field and label
        form_class = filterset_class().get_form_class()
        self.assertTrue(
            isinstance(form_class.declared_fields['first_name'], forms.CharField)
        )
        self.assertTrue(
            isinstance(form_class.declared_fields['gender'], forms.ChoiceField)
        )
        self.assertEqual(list(form_class.declared_fields['gender'].choices), [('', '---------')] + GENDER_CHOICES)

    def test_get_raise_exception(self):
        view = ViewClass()
        view.raise_filter_exception = True

        self.assertTrue(FilterMapBackend().get_raise_exception(view))

        view.raise_filter_exception = False
        self.assertFalse(FilterMapBackend().get_raise_exception(view))

        view.get_raise_filter_exception = lambda *a: True
        self.assertTrue(FilterMapBackend().get_raise_exception(view))

        view.get_raise_filter_exception = lambda *a: False
        self.assertFalse(FilterMapBackend().get_raise_exception(view))

    def test_get_filter_map(self):
        view = ViewClass()

        # should be None first
        self.assertIsNone(FilterMapBackend.get_filter_map(view))

        fil_map_1 = {'a': 'b'}
        view.filter_map = fil_map_1
        self.assertEqual(FilterMapBackend.get_filter_map(view), fil_map_1)

        fil_map_2 = {'c': 'd'}
        view.get_filter_map = lambda *a: fil_map_2
        self.assertEqual(FilterMapBackend.get_filter_map(view), fil_map_2)

    def test_get_filterset_kwargs(self):
        http_request = HttpRequest()
        http_request.GET.update({'foo': 'bar'})
        request = Request(http_request)

        output = FilterMapBackend.get_filterset_kwargs(request, ['1', '2'])
        expected_output = {
            'data': {'foo': ['bar']},
            'queryset': ['1', '2'],
            'request': request
        }
        self.assertEqual(output, expected_output, output)

    def test_get_filterset(self):
        fil_map = {'foo': 'bar'}
        request = Request(HttpRequest())
        queryset = ProfileQuerySet()
        view = ViewClass()
        filterset_kwargs = {
            'data': {},
            'queryset': queryset,
            'request': request
        }

        with patch(
            'filter_map.backends.FilterMapBackend.get_filterset_class',
            return_value=FilterMapFilterSet
        ) as get_filterset_class, patch(
            'filter_map.backends.FilterMapBackend.get_filter_map',
            return_value=fil_map
        ) as get_filter_map, patch(
            'filter_map.backends.FilterMapBackend.get_filterset_kwargs',
            return_value=filterset_kwargs
        ) as get_filterset_kwargs:
            filterset = FilterMapBackend().get_filterset(request, queryset, view)
            self.assertTrue(isinstance(filterset, FilterMapFilterSet))

            self.assertEqual(get_filter_map.call_count, 1)
            self.assertEqual(get_filter_map.call_args.args, (view,))

            self.assertEqual(get_filterset_class.call_count, 1)
            self.assertEqual(get_filterset_class.call_args.args, (view, fil_map))

            self.assertEqual(get_filterset_kwargs.call_count, 1)
            self.assertEqual(get_filterset_kwargs.call_args.args, (request, queryset))

    def test_filter_queryset(self):
        request = Request(HttpRequest())
        queryset = ProfileQuerySet([1, 2, 3])
        new_queryset = ProfileQuerySet([1, 2])

        view = ViewClass()

        with patch(
                'filter_map.backends.FilterMapFilterSet.filter_queryset',
                return_value=new_queryset
        ) as filter_queryset:
            qs = FilterMapBackend().filter_queryset(request, queryset, view)
            self.assertEqual(qs, new_queryset)

            self.assertEqual(filter_queryset.call_count, 1)
            self.assertEqual(filter_queryset.call_args.args, (queryset,))
