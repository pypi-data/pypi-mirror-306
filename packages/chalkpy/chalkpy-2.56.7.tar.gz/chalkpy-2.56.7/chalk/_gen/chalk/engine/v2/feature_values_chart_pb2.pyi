from chalk._gen.chalk.chart.v1 import densetimeserieschart_pb2 as _densetimeserieschart_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureValueBaseWindowFunction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_UNSPECIFIED: _ClassVar[FeatureValueBaseWindowFunction]
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_UNIQUE_VALUES: _ClassVar[FeatureValueBaseWindowFunction]
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_TOTAL_OBSERVATIONS: _ClassVar[FeatureValueBaseWindowFunction]
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_NULL_PERCENTAGE: _ClassVar[FeatureValueBaseWindowFunction]
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_MAX_VALUE: _ClassVar[FeatureValueBaseWindowFunction]
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_MIN_VALUE: _ClassVar[FeatureValueBaseWindowFunction]
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_AVERAGE: _ClassVar[FeatureValueBaseWindowFunction]
    FEATURE_VALUE_BASE_WINDOW_FUNCTION_UNIQUE_PKEYS: _ClassVar[FeatureValueBaseWindowFunction]

FEATURE_VALUE_BASE_WINDOW_FUNCTION_UNSPECIFIED: FeatureValueBaseWindowFunction
FEATURE_VALUE_BASE_WINDOW_FUNCTION_UNIQUE_VALUES: FeatureValueBaseWindowFunction
FEATURE_VALUE_BASE_WINDOW_FUNCTION_TOTAL_OBSERVATIONS: FeatureValueBaseWindowFunction
FEATURE_VALUE_BASE_WINDOW_FUNCTION_NULL_PERCENTAGE: FeatureValueBaseWindowFunction
FEATURE_VALUE_BASE_WINDOW_FUNCTION_MAX_VALUE: FeatureValueBaseWindowFunction
FEATURE_VALUE_BASE_WINDOW_FUNCTION_MIN_VALUE: FeatureValueBaseWindowFunction
FEATURE_VALUE_BASE_WINDOW_FUNCTION_AVERAGE: FeatureValueBaseWindowFunction
FEATURE_VALUE_BASE_WINDOW_FUNCTION_UNIQUE_PKEYS: FeatureValueBaseWindowFunction

class FeatureValuePercentileWindowFunction(_message.Message):
    __slots__ = ("percentile",)
    PERCENTILE_FIELD_NUMBER: _ClassVar[int]
    percentile: float
    def __init__(self, percentile: _Optional[float] = ...) -> None: ...

class FeatureValueSeries(_message.Message):
    __slots__ = ("feature_fqn", "series_title", "base_window_function", "percentile_window_function")
    FEATURE_FQN_FIELD_NUMBER: _ClassVar[int]
    SERIES_TITLE_FIELD_NUMBER: _ClassVar[int]
    BASE_WINDOW_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    PERCENTILE_WINDOW_FUNCTION_FIELD_NUMBER: _ClassVar[int]
    feature_fqn: str
    series_title: str
    base_window_function: FeatureValueBaseWindowFunction
    percentile_window_function: FeatureValuePercentileWindowFunction
    def __init__(
        self,
        feature_fqn: _Optional[str] = ...,
        series_title: _Optional[str] = ...,
        base_window_function: _Optional[_Union[FeatureValueBaseWindowFunction, str]] = ...,
        percentile_window_function: _Optional[_Union[FeatureValuePercentileWindowFunction, _Mapping]] = ...,
    ) -> None: ...

class GetFeatureValuesTimeSeriesChartRequest(_message.Message):
    __slots__ = ("title", "series", "window_period", "start_timestamp_inclusive", "end_timestamp_exclusive")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SERIES_FIELD_NUMBER: _ClassVar[int]
    WINDOW_PERIOD_FIELD_NUMBER: _ClassVar[int]
    START_TIMESTAMP_INCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    END_TIMESTAMP_EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    title: str
    series: _containers.RepeatedCompositeFieldContainer[FeatureValueSeries]
    window_period: _duration_pb2.Duration
    start_timestamp_inclusive: _timestamp_pb2.Timestamp
    end_timestamp_exclusive: _timestamp_pb2.Timestamp
    def __init__(
        self,
        title: _Optional[str] = ...,
        series: _Optional[_Iterable[_Union[FeatureValueSeries, _Mapping]]] = ...,
        window_period: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...,
        start_timestamp_inclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        end_timestamp_exclusive: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class GetFeatureValuesTimeSeriesChartResponse(_message.Message):
    __slots__ = ("chart",)
    CHART_FIELD_NUMBER: _ClassVar[int]
    chart: _densetimeserieschart_pb2.DenseTimeSeriesChart
    def __init__(
        self, chart: _Optional[_Union[_densetimeserieschart_pb2.DenseTimeSeriesChart, _Mapping]] = ...
    ) -> None: ...
