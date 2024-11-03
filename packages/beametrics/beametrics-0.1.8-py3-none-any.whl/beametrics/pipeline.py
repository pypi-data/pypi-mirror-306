import apache_beam as beam
from apache_beam.transforms.window import FixedWindows, TimestampedValue, IntervalWindow
from typing import Dict, Any, List
from beametrics.filter import FilterCondition, MessageFilter
from beametrics.metrics import MetricType, MetricDefinition
from beametrics.metrics_exporter import (
    GoogleCloudMetricsConfig,
    GoogleCloudMetricsExporter,
)
from apache_beam.transforms.core import WindowIntoFn
from apache_beam.coders.coders import GlobalWindowCoder


class DynamicWindowIntoFn(FixedWindows):
    def __init__(self, window_size):
        super().__init__(window_size)


def parse_json(message: bytes) -> Dict[str, Any]:
    """Parse JSON message from PubSub"""
    import json

    return json.loads(message.decode("utf-8"))


class DecodeAndParse(beam.DoFn):
    """Decode and parse PubSub message"""

    def process(self, element):
        return [parse_json(element)]


class ExportMetricsToCloudMonitoring(beam.DoFn):
    """Export metrics to Cloud Monitoring"""

    def __init__(self, metrics_config: GoogleCloudMetricsConfig):
        self.metrics_config = metrics_config
        self.exporter = None

    def setup(self):
        self.exporter = GoogleCloudMetricsExporter(self.metrics_config)

    def process(self, count):
        self.exporter.export(float(count))
        yield count


class ExtractField(beam.DoFn):
    """Extract field value from message for aggregation"""

    def __init__(self, field: str):
        self.field = field

    def process(self, element):
        value = element.get(self.field)
        if value is not None and isinstance(value, (int, float)):
            yield float(value)


class PubsubToCloudMonitoringPipeline(beam.PTransform):
    """Transform PubSub messages to Cloud Monitoring metrics"""

    def __init__(
        self,
        filter_conditions: List[FilterCondition],
        metrics_config: GoogleCloudMetricsConfig,
        metric_definition: MetricDefinition,
        window_size: beam.options.value_provider.ValueProvider,
    ):
        """Initialize the pipeline transform

        Args:
            filter_conditions: List of conditions for filtering messages
            metrics_config: Configuration for metrics export
            metric_definition: Definition of the metric to generate
            window_size: Size of the fixed window in seconds (minimum 60)

        Raises:
            ValueError: If window_size is less than 60 seconds
        """

        super().__init__()
        self.filter = MessageFilter(filter_conditions)
        self.metrics_config = metrics_config
        self.metric_definition = metric_definition
        self.window_size = window_size

    def _get_window_transform(self):
        """Get the window transform with configured size"""
        return beam.WindowInto(DynamicWindowIntoFn(self.window_size))

    def _get_combiner(self):
        """Get appropriate combiner based on metric type"""
        metric_type = self.metric_definition.type

        class DeferredMetricCombiner(beam.CombineFn):
            def __init__(self, metric_type):
                self.metric_type = metric_type

            def create_accumulator(self):
                return 0

            def add_input(self, accumulator, input):
                if isinstance(input, dict):
                    return accumulator + 1
                return accumulator + input

            def merge_accumulators(self, accumulators):
                return sum(accumulators)

            def extract_output(self, accumulator):
                if isinstance(
                    self.metric_type, beam.options.value_provider.ValueProvider
                ):
                    type_str = self.metric_type.get().upper()
                else:
                    type_str = self.metric_type.value.upper()

                return (
                    accumulator
                    if type_str == "COUNT"
                    else accumulator / len(accumulators)
                )

        return DeferredMetricCombiner(metric_type)

    def expand(self, pcoll):
        filtered = (
            pcoll
            # | "Window" >> self._get_window_transform()
            | "DecodeAndParse" >> beam.ParDo(DecodeAndParse())
            | "FilterMessages" >> beam.Filter(self.filter.matches)
        )

        class MetricTypeRouter(beam.DoFn):
            def __init__(self, metric_type, field):
                self.metric_type = metric_type
                self.field = field

            def process(self, element):
                if isinstance(
                    self.metric_type, beam.options.value_provider.ValueProvider
                ):
                    is_count = self.metric_type.get().upper() == "COUNT"
                else:
                    is_count = self.metric_type == MetricType.COUNT

                if is_count:
                    yield element
                else:
                    yield float(element.get(self.field, 0))

        values = filtered | "RouteByMetricType" >> beam.ParDo(
            MetricTypeRouter(self.metric_definition.type, self.metric_definition.field)
        )

        return (
            values
            | "Window" >> beam.WindowInto(FixedWindows(60))
            | "AggregateMetrics"
            >> beam.CombineGlobally(self._get_combiner()).without_defaults()
            | "ExportMetrics"
            >> beam.ParDo(ExportMetricsToCloudMonitoring(self.metrics_config))
        )
