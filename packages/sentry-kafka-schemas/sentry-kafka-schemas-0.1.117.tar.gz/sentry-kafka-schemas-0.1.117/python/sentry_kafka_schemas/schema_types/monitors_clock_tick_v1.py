from typing import Union, Literal, TypedDict, Required


class ClockTick(TypedDict, total=False):
    """
    clock_tick.

    A message indicating that the ingest-monitor consumer has processed check-ins past the specified minute-bound timestamp.
    """

    ts: Required[Union[int, float]]
    """
    The timestamp the clock ticked at.

    Required property
    """

    volume_anomaly_result: "_ClockTickVolumeAnomalyResult"
    """ The result of the volume anomaly detection for the minute that has been ticked past. """



_ClockTickVolumeAnomalyResult = Union[Literal['normal'], Literal['abnormal']]
""" The result of the volume anomaly detection for the minute that has been ticked past. """
_CLOCKTICKVOLUMEANOMALYRESULT_NORMAL: Literal['normal'] = "normal"
"""The values for the 'The result of the volume anomaly detection for the minute that has been ticked past' enum"""
_CLOCKTICKVOLUMEANOMALYRESULT_ABNORMAL: Literal['abnormal'] = "abnormal"
"""The values for the 'The result of the volume anomaly detection for the minute that has been ticked past' enum"""

