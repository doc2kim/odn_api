from django_filters import Filter
from django_filters.widgets import SuffixedMultiWidget
from django.forms import MultiValueField, FloatField, NumberInput, DateInput, TimeInput, CharField


class CustomLocationWidget(SuffixedMultiWidget):
    suffixes = ['lat', 'lon']

    def __init__(self, attrs=None):
        widgets = [
            NumberInput(attrs={'step': '0.0001', 'placeholder': '위도'}),
            NumberInput(attrs={'step': '0.0001', 'placeholder': '경도'}),
        ]
        super().__init__(widgets, attrs)


class CustomLocationField(MultiValueField):
    widget = CustomLocationWidget

    def __init__(self, fields=None, *args, **kwargs):
        if fields is None:
            fields = (
                FloatField(),
                FloatField()
            )
            super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return list(data_list)
        return [None, None]


class CustomLocationFilter(Filter):
    field_class = CustomLocationField


class CustomDateTimeWidget(SuffixedMultiWidget):
    suffixes = ['date_start', 'date_stop', 'time_start', 'time_stop']

    def __init__(self, attrs=None):
        widgets = [
            DateInput(attrs={'placeholder': '날짜 시작'}),
            DateInput(attrs={'placeholder': '날짜 종료'}),
            TimeInput(attrs={'placeholder': '시간 시작'}),
            TimeInput(attrs={'placeholder': '시간 종료'}),
        ]
        super().__init__(widgets, attrs)


class CustomDateTimeField(MultiValueField):
    widget = CustomDateTimeWidget

    def __init__(self, fields=None, *args, **kwargs):
        if fields is None:
            fields = (
                CharField(),
                CharField(),
                CharField(),
                CharField()
            )
            super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return list(data_list)
        return [None, None, None, None]


class CustomDateTimeFilter(Filter):
    field_class = CustomDateTimeField
