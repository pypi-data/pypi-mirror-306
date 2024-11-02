"""Test the TadoZone object."""

import os
import json
from unittest.mock import patch

from PyTado.http import Http
from PyTado.interface import Tado


def _mock_tado_climate_zone_from_fixture(filename):
    obj = Http
    with patch.object(obj, "_Http__login"), patch(
            "PyTado.interface.Tado.get_me"
    ), patch(
        "PyTado.interface.Tado.get_state",
        return_value=json.loads(load_fixture(filename)),
    ):
        tado = Tado("my@username.com", "mypassword")
        return tado.get_zone_state(1)


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path) as fptr:
        return fptr.read()


def test_ac_issue_32294_heat_mode():
    """Test smart ac cool mode."""
    ac_issue_32294_heat_mode = _mock_tado_climate_zone_from_fixture(
        "ac_issue_32294.heat_mode.json"
    )
    assert ac_issue_32294_heat_mode.preparation is False
    assert ac_issue_32294_heat_mode.open_window is False
    assert ac_issue_32294_heat_mode.open_window_attr == {}
    assert ac_issue_32294_heat_mode.current_temp == 21.82
    assert ac_issue_32294_heat_mode.current_temp_timestamp == "2020-02-29T22:51:05.016Z"
    assert ac_issue_32294_heat_mode.connection is None
    assert ac_issue_32294_heat_mode.tado_mode == "HOME"
    assert ac_issue_32294_heat_mode.overlay_active is False
    assert ac_issue_32294_heat_mode.overlay_termination_type is None
    assert ac_issue_32294_heat_mode.current_humidity == 40.4
    assert (
            ac_issue_32294_heat_mode.current_humidity_timestamp
            == "2020-02-29T22:51:05.016Z"
    )
    assert ac_issue_32294_heat_mode.ac_power_timestamp == "2020-02-29T22:50:34.850Z"
    assert ac_issue_32294_heat_mode.heating_power_timestamp is None
    assert ac_issue_32294_heat_mode.ac_power == "ON"
    assert ac_issue_32294_heat_mode.heating_power is None
    assert ac_issue_32294_heat_mode.heating_power_percentage is None
    assert ac_issue_32294_heat_mode.is_away is False
    assert ac_issue_32294_heat_mode.power == "ON"
    assert ac_issue_32294_heat_mode.current_hvac_action == "HEATING"
    assert ac_issue_32294_heat_mode.current_fan_speed == "AUTO"
    assert ac_issue_32294_heat_mode.link == "ONLINE"
    assert ac_issue_32294_heat_mode.current_hvac_mode == "SMART_SCHEDULE"
    assert ac_issue_32294_heat_mode.target_temp == 25.0
    assert ac_issue_32294_heat_mode.available is True
    assert ac_issue_32294_heat_mode.precision == 0.1
    assert ac_issue_32294_heat_mode.current_swing_mode == "OFF"


def test_smartac3_smart_mode():
    """Test smart ac smart mode."""
    smartac3_smart_mode = _mock_tado_climate_zone_from_fixture(
        "smartac3.smart_mode.json"
    )
    assert smartac3_smart_mode.preparation is False
    assert smartac3_smart_mode.open_window is False
    assert smartac3_smart_mode.open_window_attr == {}
    assert smartac3_smart_mode.current_temp == 24.43
    assert smartac3_smart_mode.current_temp_timestamp == "2020-03-05T03:50:24.769Z"
    assert smartac3_smart_mode.connection is None
    assert smartac3_smart_mode.tado_mode == "HOME"
    assert smartac3_smart_mode.overlay_active is False
    assert smartac3_smart_mode.overlay_termination_type is None
    assert smartac3_smart_mode.current_humidity == 60.0
    assert smartac3_smart_mode.current_humidity_timestamp == "2020-03-05T03:50:24.769Z"
    assert smartac3_smart_mode.ac_power_timestamp == "2020-03-05T03:52:22.253Z"
    assert smartac3_smart_mode.heating_power_timestamp is None
    assert smartac3_smart_mode.ac_power == "OFF"
    assert smartac3_smart_mode.heating_power is None
    assert smartac3_smart_mode.heating_power_percentage is None
    assert smartac3_smart_mode.is_away is False
    assert smartac3_smart_mode.power == "ON"
    assert smartac3_smart_mode.current_hvac_action == "IDLE"
    assert smartac3_smart_mode.current_fan_speed == "MIDDLE"
    assert smartac3_smart_mode.link == "ONLINE"
    assert smartac3_smart_mode.current_hvac_mode == "SMART_SCHEDULE"
    assert smartac3_smart_mode.target_temp == 20.0
    assert smartac3_smart_mode.available is True
    assert smartac3_smart_mode.precision == 0.1
    assert smartac3_smart_mode.current_swing_mode == "OFF"


def test_smartac3_cool_mode():
    """Test smart ac cool mode."""
    smartac3_cool_mode = _mock_tado_climate_zone_from_fixture("smartac3.cool_mode.json")
    assert smartac3_cool_mode.preparation is False
    assert smartac3_cool_mode.open_window is False
    assert smartac3_cool_mode.open_window_attr == {}
    assert smartac3_cool_mode.current_temp == 24.76
    assert smartac3_cool_mode.current_temp_timestamp == "2020-03-05T03:57:38.850Z"
    assert smartac3_cool_mode.connection is None
    assert smartac3_cool_mode.tado_mode == "HOME"
    assert smartac3_cool_mode.overlay_active is True
    assert smartac3_cool_mode.overlay_termination_type == "TADO_MODE"
    assert smartac3_cool_mode.current_humidity == 60.9
    assert smartac3_cool_mode.current_humidity_timestamp == "2020-03-05T03:57:38.850Z"
    assert smartac3_cool_mode.ac_power_timestamp == "2020-03-05T04:01:07.162Z"
    assert smartac3_cool_mode.heating_power_timestamp is None
    assert smartac3_cool_mode.ac_power == "ON"
    assert smartac3_cool_mode.heating_power is None
    assert smartac3_cool_mode.heating_power_percentage is None
    assert smartac3_cool_mode.is_away is False
    assert smartac3_cool_mode.power == "ON"
    assert smartac3_cool_mode.current_hvac_action == "COOLING"
    assert smartac3_cool_mode.current_fan_speed == "AUTO"
    assert smartac3_cool_mode.link == "ONLINE"
    assert smartac3_cool_mode.current_hvac_mode == "COOL"
    assert smartac3_cool_mode.target_temp == 17.78
    assert smartac3_cool_mode.available is True
    assert smartac3_cool_mode.precision == 0.1
    assert smartac3_cool_mode.current_swing_mode == "OFF"


def test_smartac3_auto_mode():
    """Test smart ac cool mode."""
    smartac3_auto_mode = _mock_tado_climate_zone_from_fixture("smartac3.auto_mode.json")
    assert smartac3_auto_mode.preparation is False
    assert smartac3_auto_mode.open_window is False
    assert smartac3_auto_mode.open_window_attr == {}
    assert smartac3_auto_mode.current_temp == 24.8
    assert smartac3_auto_mode.current_temp_timestamp == "2020-03-05T03:55:38.160Z"
    assert smartac3_auto_mode.connection is None
    assert smartac3_auto_mode.tado_mode == "HOME"
    assert smartac3_auto_mode.overlay_active is True
    assert smartac3_auto_mode.overlay_termination_type == "TADO_MODE"
    assert smartac3_auto_mode.current_humidity == 62.5
    assert smartac3_auto_mode.current_humidity_timestamp == "2020-03-05T03:55:38.160Z"
    assert smartac3_auto_mode.ac_power_timestamp == "2020-03-05T03:56:38.627Z"
    assert smartac3_auto_mode.heating_power_timestamp is None
    assert smartac3_auto_mode.ac_power == "ON"
    assert smartac3_auto_mode.heating_power is None
    assert smartac3_auto_mode.heating_power_percentage is None
    assert smartac3_auto_mode.is_away is False
    assert smartac3_auto_mode.power == "ON"
    assert smartac3_auto_mode.current_hvac_action == "COOLING"
    assert smartac3_auto_mode.current_fan_speed == "AUTO"
    assert smartac3_auto_mode.link == "ONLINE"
    assert smartac3_auto_mode.current_hvac_mode == "AUTO"
    assert smartac3_auto_mode.target_temp is None
    assert smartac3_auto_mode.available is True
    assert smartac3_auto_mode.precision == 0.1
    assert smartac3_auto_mode.current_swing_mode == "OFF"


def test_smartac3_dry_mode():
    """Test smart ac cool mode."""
    smartac3_dry_mode = _mock_tado_climate_zone_from_fixture("smartac3.dry_mode.json")
    assert smartac3_dry_mode.preparation is False
    assert smartac3_dry_mode.open_window is False
    assert smartac3_dry_mode.open_window_attr == {}
    assert smartac3_dry_mode.current_temp == 25.01
    assert smartac3_dry_mode.current_temp_timestamp == "2020-03-05T04:02:07.396Z"
    assert smartac3_dry_mode.connection is None
    assert smartac3_dry_mode.tado_mode == "HOME"
    assert smartac3_dry_mode.overlay_active is True
    assert smartac3_dry_mode.overlay_termination_type == "TADO_MODE"
    assert smartac3_dry_mode.current_humidity == 62.0
    assert smartac3_dry_mode.current_humidity_timestamp == "2020-03-05T04:02:07.396Z"
    assert smartac3_dry_mode.ac_power_timestamp == "2020-03-05T04:02:40.867Z"
    assert smartac3_dry_mode.heating_power_timestamp is None
    assert smartac3_dry_mode.ac_power == "ON"
    assert smartac3_dry_mode.heating_power is None
    assert smartac3_dry_mode.heating_power_percentage is None
    assert smartac3_dry_mode.is_away is False
    assert smartac3_dry_mode.power == "ON"
    assert smartac3_dry_mode.current_hvac_action == "DRYING"
    assert smartac3_dry_mode.current_fan_speed == "AUTO"
    assert smartac3_dry_mode.link == "ONLINE"
    assert smartac3_dry_mode.current_hvac_mode == "DRY"
    assert smartac3_dry_mode.target_temp is None
    assert smartac3_dry_mode.available is True
    assert smartac3_dry_mode.precision == 0.1
    assert smartac3_dry_mode.current_swing_mode == "OFF"


def test_smartac3_fan_mode():
    """Test smart ac cool mode."""
    smartac3_fan_mode = _mock_tado_climate_zone_from_fixture("smartac3.fan_mode.json")
    assert smartac3_fan_mode.preparation is False
    assert smartac3_fan_mode.open_window is False
    assert smartac3_fan_mode.open_window_attr == {}
    assert smartac3_fan_mode.current_temp == 25.01
    assert smartac3_fan_mode.current_temp_timestamp == "2020-03-05T04:02:07.396Z"
    assert smartac3_fan_mode.connection is None
    assert smartac3_fan_mode.tado_mode == "HOME"
    assert smartac3_fan_mode.overlay_active is True
    assert smartac3_fan_mode.overlay_termination_type == "TADO_MODE"
    assert smartac3_fan_mode.current_humidity == 62.0
    assert smartac3_fan_mode.current_humidity_timestamp == "2020-03-05T04:02:07.396Z"
    assert smartac3_fan_mode.ac_power_timestamp == "2020-03-05T04:03:44.328Z"
    assert smartac3_fan_mode.heating_power_timestamp is None
    assert smartac3_fan_mode.ac_power == "ON"
    assert smartac3_fan_mode.heating_power is None
    assert smartac3_fan_mode.heating_power_percentage is None
    assert smartac3_fan_mode.is_away is False
    assert smartac3_fan_mode.power == "ON"
    assert smartac3_fan_mode.current_hvac_action == "FAN"
    assert smartac3_fan_mode.current_fan_speed == "AUTO"
    assert smartac3_fan_mode.link == "ONLINE"
    assert smartac3_fan_mode.current_hvac_mode == "FAN"
    assert smartac3_fan_mode.target_temp is None
    assert smartac3_fan_mode.available is True
    assert smartac3_fan_mode.precision == 0.1
    assert smartac3_fan_mode.current_swing_mode == "OFF"


def test_smartac3_heat_mode():
    """Test smart ac heat mode."""
    smartac3_heat_mode = _mock_tado_climate_zone_from_fixture("smartac3.heat_mode.json")
    assert smartac3_heat_mode.preparation is False
    assert smartac3_heat_mode.open_window is False
    assert smartac3_heat_mode.open_window_attr == {}
    assert smartac3_heat_mode.current_temp == 24.76
    assert smartac3_heat_mode.current_temp_timestamp == "2020-03-05T03:57:38.850Z"
    assert smartac3_heat_mode.connection is None
    assert smartac3_heat_mode.tado_mode == "HOME"
    assert smartac3_heat_mode.overlay_active is True
    assert smartac3_heat_mode.overlay_termination_type == "TADO_MODE"
    assert smartac3_heat_mode.current_humidity == 60.9
    assert smartac3_heat_mode.current_humidity_timestamp == "2020-03-05T03:57:38.850Z"
    assert smartac3_heat_mode.ac_power_timestamp == "2020-03-05T03:59:36.390Z"
    assert smartac3_heat_mode.heating_power_timestamp is None
    assert smartac3_heat_mode.ac_power == "ON"
    assert smartac3_heat_mode.heating_power is None
    assert smartac3_heat_mode.heating_power_percentage is None
    assert smartac3_heat_mode.is_away is False
    assert smartac3_heat_mode.power == "ON"
    assert smartac3_heat_mode.current_hvac_action == "HEATING"
    assert smartac3_heat_mode.current_fan_speed == "AUTO"
    assert smartac3_heat_mode.link == "ONLINE"
    assert smartac3_heat_mode.current_hvac_mode == "HEAT"
    assert smartac3_heat_mode.target_temp == 16.11
    assert smartac3_heat_mode.available is True
    assert smartac3_heat_mode.precision == 0.1
    assert smartac3_heat_mode.current_swing_mode == "OFF"


def test_smartac3_with_swing():
    """Test smart with swing mode."""
    smartac3_with_swing = _mock_tado_climate_zone_from_fixture(
        "smartac3.with_swing.json"
    )
    assert smartac3_with_swing.preparation is False
    assert smartac3_with_swing.open_window is False
    assert smartac3_with_swing.open_window_attr == {}
    assert smartac3_with_swing.current_temp == 20.88
    assert smartac3_with_swing.current_temp_timestamp == "2020-03-28T02:09:27.830Z"
    assert smartac3_with_swing.connection is None
    assert smartac3_with_swing.tado_mode == "HOME"
    assert smartac3_with_swing.overlay_active is False
    assert smartac3_with_swing.overlay_termination_type is None
    assert smartac3_with_swing.current_humidity == 42.3
    assert smartac3_with_swing.current_humidity_timestamp == "2020-03-28T02:09:27.830Z"
    assert smartac3_with_swing.ac_power_timestamp == "2020-03-27T23:02:22.260Z"
    assert smartac3_with_swing.heating_power_timestamp is None
    assert smartac3_with_swing.ac_power == "ON"
    assert smartac3_with_swing.heating_power is None
    assert smartac3_with_swing.heating_power_percentage is None
    assert smartac3_with_swing.is_away is False
    assert smartac3_with_swing.power == "ON"
    assert smartac3_with_swing.current_hvac_action == "HEATING"
    assert smartac3_with_swing.current_fan_speed == "AUTO"
    assert smartac3_with_swing.link == "ONLINE"
    assert smartac3_with_swing.current_hvac_mode == "SMART_SCHEDULE"
    assert smartac3_with_swing.target_temp == 20.0
    assert smartac3_with_swing.available is True
    assert smartac3_with_swing.precision == 0.1
    assert smartac3_with_swing.current_swing_mode == "ON"


def test_smartac3_hvac_off():
    """Test smart ac cool mode."""
    smartac3_hvac_off = _mock_tado_climate_zone_from_fixture("smartac3.hvac_off.json")
    assert smartac3_hvac_off.preparation is False
    assert smartac3_hvac_off.open_window is False
    assert smartac3_hvac_off.open_window_attr == {}
    assert smartac3_hvac_off.current_temp == 21.44
    assert smartac3_hvac_off.current_temp_timestamp == "2020-03-05T01:21:44.089Z"
    assert smartac3_hvac_off.connection is None
    assert smartac3_hvac_off.tado_mode == "AWAY"
    assert smartac3_hvac_off.overlay_active is True
    assert smartac3_hvac_off.overlay_termination_type == "MANUAL"
    assert smartac3_hvac_off.current_humidity == 48.2
    assert smartac3_hvac_off.current_humidity_timestamp == "2020-03-05T01:21:44.089Z"
    assert smartac3_hvac_off.ac_power_timestamp == "2020-02-29T05:34:10.318Z"
    assert smartac3_hvac_off.heating_power_timestamp is None
    assert smartac3_hvac_off.ac_power == "OFF"
    assert smartac3_hvac_off.heating_power is None
    assert smartac3_hvac_off.heating_power_percentage is None
    assert smartac3_hvac_off.is_away is True
    assert smartac3_hvac_off.power == "OFF"
    assert smartac3_hvac_off.current_hvac_action == "OFF"
    assert smartac3_hvac_off.current_fan_speed == "OFF"
    assert smartac3_hvac_off.link == "ONLINE"
    assert smartac3_hvac_off.current_hvac_mode == "OFF"
    assert smartac3_hvac_off.target_temp is None
    assert smartac3_hvac_off.available is True
    assert smartac3_hvac_off.precision == 0.1
    assert smartac3_hvac_off.current_swing_mode == "OFF"


def test_smartac3_manual_off():
    """Test smart ac cool mode."""
    smartac3_manual_off = _mock_tado_climate_zone_from_fixture(
        "smartac3.manual_off.json"
    )
    assert smartac3_manual_off.preparation is False
    assert smartac3_manual_off.open_window is False
    assert smartac3_manual_off.open_window_attr == {}
    assert smartac3_manual_off.current_temp == 25.01
    assert smartac3_manual_off.current_temp_timestamp == "2020-03-05T04:02:07.396Z"
    assert smartac3_manual_off.connection is None
    assert smartac3_manual_off.tado_mode == "HOME"
    assert smartac3_manual_off.overlay_active is True
    assert smartac3_manual_off.overlay_termination_type == "MANUAL"
    assert smartac3_manual_off.current_humidity == 62.0
    assert smartac3_manual_off.current_humidity_timestamp == "2020-03-05T04:02:07.396Z"
    assert smartac3_manual_off.ac_power_timestamp == "2020-03-05T04:05:08.804Z"
    assert smartac3_manual_off.heating_power_timestamp is None
    assert smartac3_manual_off.ac_power == "OFF"
    assert smartac3_manual_off.heating_power is None
    assert smartac3_manual_off.heating_power_percentage is None
    assert smartac3_manual_off.is_away is False
    assert smartac3_manual_off.power == "OFF"
    assert smartac3_manual_off.current_hvac_action == "OFF"
    assert smartac3_manual_off.current_fan_speed == "OFF"
    assert smartac3_manual_off.link == "ONLINE"
    assert smartac3_manual_off.current_hvac_mode == "OFF"
    assert smartac3_manual_off.target_temp is None
    assert smartac3_manual_off.available is True
    assert smartac3_manual_off.precision == 0.1
    assert smartac3_manual_off.current_swing_mode == "OFF"


def test_smartac3_offline():
    """Test smart ac cool mode."""
    smartac3_offline = _mock_tado_climate_zone_from_fixture("smartac3.offline.json")
    assert smartac3_offline.preparation is False
    assert smartac3_offline.open_window is False
    assert smartac3_offline.open_window_attr == {}
    assert smartac3_offline.current_temp == 25.05
    assert smartac3_offline.current_temp_timestamp == "2020-03-03T21:23:57.846Z"
    assert smartac3_offline.connection is None
    assert smartac3_offline.tado_mode == "HOME"
    assert smartac3_offline.overlay_active is True
    assert smartac3_offline.overlay_termination_type == "TADO_MODE"
    assert smartac3_offline.current_humidity == 61.6
    assert smartac3_offline.current_humidity_timestamp == "2020-03-03T21:23:57.846Z"
    assert smartac3_offline.ac_power_timestamp == "2020-02-29T18:42:26.683Z"
    assert smartac3_offline.heating_power_timestamp is None
    assert smartac3_offline.ac_power == "OFF"
    assert smartac3_offline.heating_power is None
    assert smartac3_offline.heating_power_percentage is None
    assert smartac3_offline.is_away is False
    assert smartac3_offline.power == "ON"
    assert smartac3_offline.current_hvac_action == "IDLE"
    assert smartac3_offline.current_fan_speed == "AUTO"
    assert smartac3_offline.link == "OFFLINE"
    assert smartac3_offline.current_hvac_mode == "COOL"
    assert smartac3_offline.target_temp == 17.78
    assert smartac3_offline.available is False
    assert smartac3_offline.precision == 0.1
    assert smartac3_offline.current_swing_mode == "OFF"


def test_hvac_action_heat():
    """Test smart ac cool mode."""
    hvac_action_heat = _mock_tado_climate_zone_from_fixture("hvac_action_heat.json")
    assert hvac_action_heat.preparation is False
    assert hvac_action_heat.open_window is False
    assert hvac_action_heat.open_window_attr == {}
    assert hvac_action_heat.current_temp == 21.4
    assert hvac_action_heat.current_temp_timestamp == "2020-03-06T18:06:09.546Z"
    assert hvac_action_heat.connection is None
    assert hvac_action_heat.tado_mode == "HOME"
    assert hvac_action_heat.overlay_active is True
    assert hvac_action_heat.overlay_termination_type == "TADO_MODE"
    assert hvac_action_heat.current_humidity == 50.4
    assert hvac_action_heat.current_humidity_timestamp == "2020-03-06T18:06:09.546Z"
    assert hvac_action_heat.ac_power_timestamp == "2020-03-06T17:38:30.302Z"
    assert hvac_action_heat.heating_power_timestamp is None
    assert hvac_action_heat.ac_power == "OFF"
    assert hvac_action_heat.heating_power is None
    assert hvac_action_heat.heating_power_percentage is None
    assert hvac_action_heat.is_away is False
    assert hvac_action_heat.power == "ON"
    assert hvac_action_heat.current_hvac_action == "IDLE"
    assert hvac_action_heat.current_fan_speed == "AUTO"
    assert hvac_action_heat.link == "ONLINE"
    assert hvac_action_heat.current_hvac_mode == "HEAT"
    assert hvac_action_heat.target_temp == 16.11
    assert hvac_action_heat.available is True
    assert hvac_action_heat.precision == 0.1
    assert hvac_action_heat.current_swing_mode == "OFF"


def test_smartac3_turning_off():
    """Test smart ac cool mode."""
    smartac3_turning_off = _mock_tado_climate_zone_from_fixture(
        "smartac3.turning_off.json"
    )
    assert smartac3_turning_off.preparation is False
    assert smartac3_turning_off.open_window is False
    assert smartac3_turning_off.open_window_attr == {}
    assert smartac3_turning_off.current_temp == 21.4
    assert smartac3_turning_off.current_temp_timestamp == "2020-03-06T19:06:13.185Z"
    assert smartac3_turning_off.connection is None
    assert smartac3_turning_off.tado_mode == "HOME"
    assert smartac3_turning_off.overlay_active is True
    assert smartac3_turning_off.overlay_termination_type == "MANUAL"
    assert smartac3_turning_off.current_humidity == 49.2
    assert smartac3_turning_off.current_humidity_timestamp == "2020-03-06T19:06:13.185Z"
    assert smartac3_turning_off.ac_power_timestamp == "2020-03-06T19:05:21.835Z"
    assert smartac3_turning_off.heating_power_timestamp is None
    assert smartac3_turning_off.ac_power == "ON"
    assert smartac3_turning_off.heating_power is None
    assert smartac3_turning_off.heating_power_percentage is None
    assert smartac3_turning_off.is_away is False
    assert smartac3_turning_off.power == "OFF"
    assert smartac3_turning_off.current_hvac_action == "OFF"
    assert smartac3_turning_off.current_fan_speed == "OFF"
    assert smartac3_turning_off.link == "ONLINE"
    assert smartac3_turning_off.current_hvac_mode == "OFF"
    assert smartac3_turning_off.target_temp is None
    assert smartac3_turning_off.available is True
    assert smartac3_turning_off.precision == 0.1
    assert smartac3_turning_off.current_swing_mode == "OFF"


def test_tadov2_heating_auto_mode():
    """Test tadov2 heating auto mode."""
    mode = _mock_tado_climate_zone_from_fixture("tadov2.heating.auto_mode.json")
    assert mode.preparation is False
    assert mode.open_window is False
    assert mode.open_window_attr == {}
    assert mode.current_temp == 20.65
    assert mode.current_temp_timestamp == "2020-03-10T07:44:11.947Z"
    assert mode.connection is None
    assert mode.tado_mode == "HOME"
    assert mode.overlay_active is False
    assert mode.overlay_termination_type is None
    assert mode.current_humidity == 45.20
    assert mode.current_humidity_timestamp == "2020-03-10T07:44:11.947Z"
    assert mode.ac_power_timestamp is None
    assert mode.heating_power_timestamp == "2020-03-10T07:47:45.978Z"
    assert mode.ac_power is None
    assert mode.heating_power is None
    assert mode.heating_power_percentage == 0.0
    assert mode.is_away is False
    assert mode.power == "ON"
    assert mode.current_hvac_action == "IDLE"
    assert mode.current_fan_speed is None
    assert mode.link == "ONLINE"
    assert mode.current_hvac_mode == "SMART_SCHEDULE"
    assert mode.target_temp == 20.0
    assert mode.available is True
    assert mode.precision == 0.1
    assert mode.current_swing_mode == "OFF"


def test_tadov2_heating_manual_mode():
    """Test tadov2 heating manual mode."""
    mode = _mock_tado_climate_zone_from_fixture("tadov2.heating.manual_mode.json")
    assert mode.preparation is False
    assert mode.open_window is False
    assert mode.open_window_attr == {}
    assert mode.current_temp == 20.65
    assert mode.current_temp_timestamp == "2020-03-10T07:44:11.947Z"
    assert mode.connection is None
    assert mode.tado_mode == "HOME"
    assert mode.overlay_active is True
    assert mode.overlay_termination_type == "MANUAL"
    assert mode.current_humidity == 45.2
    assert mode.current_humidity_timestamp == "2020-03-10T07:44:11.947Z"
    assert mode.ac_power_timestamp is None
    assert mode.heating_power_timestamp == "2020-03-10T07:47:45.978Z"
    assert mode.ac_power is None
    assert mode.heating_power is None
    assert mode.heating_power_percentage == 0.0
    assert mode.is_away is False
    assert mode.power == "ON"
    assert mode.current_hvac_action == "IDLE"
    assert mode.current_fan_speed is None
    assert mode.link == "ONLINE"
    assert mode.current_hvac_mode == "HEAT"
    assert mode.target_temp == 20.5
    assert mode.available is True
    assert mode.precision == 0.1
    assert mode.current_swing_mode == "OFF"


def test_tadov2_heating_off_mode():
    """Test tadov2 heating off mode."""
    mode = _mock_tado_climate_zone_from_fixture("tadov2.heating.off_mode.json")
    assert mode.preparation is False
    assert mode.open_window is False
    assert mode.open_window_attr == {}
    assert mode.current_temp == 20.65
    assert mode.current_temp_timestamp == "2020-03-10T07:44:11.947Z"
    assert mode.connection is None
    assert mode.tado_mode == "HOME"
    assert mode.overlay_active is True
    assert mode.overlay_termination_type == "MANUAL"
    assert mode.current_humidity == 45.2
    assert mode.current_humidity_timestamp == "2020-03-10T07:44:11.947Z"
    assert mode.ac_power_timestamp is None
    assert mode.heating_power_timestamp == "2020-03-10T07:47:45.978Z"
    assert mode.ac_power is None
    assert mode.heating_power is None
    assert mode.heating_power_percentage == 0.0
    assert mode.is_away is False
    assert mode.power == "OFF"
    assert mode.current_hvac_action == "OFF"
    assert mode.current_fan_speed is None
    assert mode.link == "ONLINE"
    assert mode.current_hvac_mode == "OFF"
    assert mode.target_temp is None
    assert mode.available is True
    assert mode.precision == 0.1
    assert mode.current_swing_mode == "OFF"


def test_tadov2_water_heater_auto_mode():
    """Test tadov2 water heater auto mode."""
    mode = _mock_tado_climate_zone_from_fixture("tadov2.water_heater.auto_mode.json")
    assert mode.preparation is False
    assert mode.open_window is False
    assert mode.open_window_attr == {}
    assert mode.current_temp is None
    assert mode.current_temp_timestamp is None
    assert mode.connection is None
    assert mode.tado_mode == "HOME"
    assert mode.overlay_active is False
    assert mode.overlay_termination_type is None
    assert mode.current_humidity is None
    assert mode.current_humidity_timestamp is None
    assert mode.ac_power_timestamp is None
    assert mode.heating_power_timestamp is None
    assert mode.ac_power is None
    assert mode.heating_power is None
    assert mode.heating_power_percentage is None
    assert mode.is_away is False
    assert mode.power == "ON"
    assert mode.current_hvac_action == "IDLE"
    assert mode.current_fan_speed is None
    assert mode.link == "ONLINE"
    assert mode.current_hvac_mode == "SMART_SCHEDULE"
    assert mode.target_temp == 65.00
    assert mode.available is True
    assert mode.precision == 0.1
    assert mode.current_swing_mode == "OFF"


def test_tadov2_water_heater_manual_mode():
    """Test tadov2 water heater manual mode."""
    mode = _mock_tado_climate_zone_from_fixture("tadov2.water_heater.manual_mode.json")
    assert mode.preparation is False
    assert mode.open_window is False
    assert mode.open_window_attr == {}
    assert mode.current_temp is None
    assert mode.current_temp_timestamp is None
    assert mode.connection is None
    assert mode.tado_mode == "HOME"
    assert mode.overlay_active is True
    assert mode.overlay_termination_type == "MANUAL"
    assert mode.current_humidity is None
    assert mode.current_humidity_timestamp is None
    assert mode.ac_power_timestamp is None
    assert mode.heating_power_timestamp is None
    assert mode.ac_power is None
    assert mode.heating_power is None
    assert mode.heating_power_percentage is None
    assert mode.is_away is False
    assert mode.power == "ON"
    assert mode.current_hvac_action == "IDLE"
    assert mode.current_fan_speed is None
    assert mode.link == "ONLINE"
    assert mode.current_hvac_mode == "HEATING"
    assert mode.target_temp == 55.00
    assert mode.available is True
    assert mode.precision == 0.1
    assert mode.current_swing_mode == "OFF"


def test_tadov2_water_heater_off_mode():
    """Test tadov2 water heater off mode."""
    mode = _mock_tado_climate_zone_from_fixture("tadov2.water_heater.off_mode.json")
    assert mode.preparation is False
    assert mode.open_window is False
    assert mode.open_window_attr == {}
    assert mode.current_temp is None
    assert mode.current_temp_timestamp is None
    assert mode.connection is None
    assert mode.tado_mode == "HOME"
    assert mode.overlay_active is True
    assert mode.overlay_termination_type == "MANUAL"
    assert mode.current_humidity is None
    assert mode.current_humidity_timestamp is None
    assert mode.ac_power_timestamp is None
    assert mode.heating_power_timestamp is None
    assert mode.ac_power is None
    assert mode.heating_power is None
    assert mode.heating_power_percentage is None
    assert mode.is_away is False
    assert mode.power == "OFF"
    assert mode.current_hvac_action == "OFF"
    assert mode.current_fan_speed is None
    assert mode.link == "ONLINE"
    assert mode.current_hvac_mode == "OFF"
    assert mode.target_temp is None
    assert mode.available is True
    assert mode.precision == 0.1
    assert mode.current_swing_mode == "OFF"
