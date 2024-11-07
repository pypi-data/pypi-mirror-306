import polars
import polars._typing

from vitalx.aggregation.types import (
    ActivityColumnT,
    BodyColumnT,
    SleepColumnT,
    WorkoutColumnT,
)

DF_GROUP_KEY = "group_key"

SLEEP_DATAFRAME_SCHEMA: dict[SleepColumnT, polars._typing.PolarsDataType] = {
    "session_start": polars.Datetime(time_zone=None, time_unit="ms"),
    "session_end": polars.Datetime(time_zone=None, time_unit="ms"),
    "state": polars.Utf8,
    "duration_second": polars.Int64,
    "stage_asleep_second": polars.Int64,
    "stage_awake_second": polars.Int64,
    "stage_light_second": polars.Int64,
    "stage_rem_second": polars.Int64,
    "stage_deep_second": polars.Int64,
    "stage_unknown_second": polars.Int64,
    "latency_second": polars.Int64,
    "heart_rate_minimum": polars.Int64,
    "heart_rate_mean": polars.Int64,
    "heart_rate_maximum": polars.Int64,
    "heart_rate_dip": polars.Float64,
    "efficiency": polars.Float64,
    "hrv_mean_rmssd": polars.Float64,
    "hrv_mean_sdnn": polars.Float64,
    "skin_temperature_delta": polars.Float64,
    "respiratory_rate": polars.Float64,
    "score": polars.Int64,
    "source_type": polars.Utf8,
    "source_provider": polars.Utf8,
    "source_app_id": polars.Utf8,
}

ACTIVITY_DATAFRAME_SCHEMA: dict[ActivityColumnT, polars._typing.PolarsDataType] = {
    "date": polars.Date(),
    "calories_total": polars.Float64,
    "calories_active": polars.Float64,
    "steps": polars.Int64,
    "distance_meter": polars.Float64,
    "floors_climbed": polars.Int64,
    "duration_active_second": polars.Int64,
    "intensity_sedentary_second": polars.Int64,
    "intensity_low_second": polars.Int64,
    "intensity_medium_second": polars.Int64,
    "intensity_high_second": polars.Int64,
    "heart_rate_mean": polars.Float64,
    "heart_rate_minimum": polars.Float64,
    "heart_rate_maximum": polars.Float64,
    "heart_rate_resting": polars.Float64,
    "source_type": polars.Utf8,
    "source_provider": polars.Utf8,
    "source_app_id": polars.Utf8,
}

WORKOUT_DATAFRAME_SCHEMA: dict[WorkoutColumnT, polars._typing.PolarsDataType] = {
    "session_start": polars.Datetime(time_zone=None, time_unit="ms"),
    "session_end": polars.Datetime(time_zone=None, time_unit="ms"),
    "title": polars.Utf8,
    "sport_id": polars.Int64,
    "sport_name": polars.Utf8,
    "sport_slug": polars.Utf8,
    "duration_active_second": polars.Int64,
    "heart_rate_mean": polars.Int64,
    "heart_rate_minimum": polars.Int64,
    "heart_rate_maximum": polars.Int64,
    "heart_rate_zone_1": polars.Float64,
    "heart_rate_zone_2": polars.Float64,
    "heart_rate_zone_3": polars.Float64,
    "heart_rate_zone_4": polars.Float64,
    "heart_rate_zone_5": polars.Float64,
    "heart_rate_zone_6": polars.Float64,
    "distance_meter": polars.Float64,
    "calories": polars.Float64,
    "elevation_gain_meter": polars.Float64,
    "elevation_maximum_meter": polars.Float64,
    "elevation_minimum_meter": polars.Float64,
    "average_speed": polars.Float64,
    "max_speed": polars.Float64,
    "power_source": polars.Utf8,
    "power_mean": polars.Float64,
    "power_maximum": polars.Float64,
    "power_weighted_mean": polars.Float64,
    "steps": polars.Int64,
    "map": polars.Object,
    "source_type": polars.Utf8,
    "source_provider": polars.Utf8,
    "source_app_id": polars.Utf8,
}


BODY_DATAFRAME_SCHEMA: dict[BodyColumnT, polars._typing.PolarsDataType] = {
    "measured_at": polars.Datetime(time_zone=None, time_unit="ms"),
    "weight_kilogram": polars.Float64,
    "fat_percentage": polars.Float64,
    "source_type": polars.Utf8,
    "source_provider": polars.Utf8,
    "source_app_id": polars.Utf8,
}
