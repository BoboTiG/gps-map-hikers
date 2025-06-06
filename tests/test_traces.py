from pathlib import Path

import pytest

from host.app import adapt_traces, check_for_sos, get_all_traces

TRACES = Path(__file__).parent / "data"
TRIP_FR = TRACES / "french"
TRIP_NZ = TRACES / "new-zealand"
EXPECTED_TRACES_TRIP_FR = [
    {
        "alt": 70.4,
        "date": "2023-07-18 18:28:17+02:00",
        "lat": 44.770385515876114,
        "lon": 0.7981667295098305,
        "pic": "",
        "ts": 1689697697,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "start",
    },
    {
        "alt": 69.4,
        "date": "2023-07-18 18:29:31+02:00",
        "lat": 44.770343229174614,
        "lon": 0.7979858480393887,
        "pic": "",
        "ts": 1689697771,
        "dist": 15.0,
        "speed": 0.7297297297297298,
        "tdist": 15.0,
        "tdist2": 15.0,
        "type": "step",
    },
    {
        "alt": 95.4,
        "date": "2023-07-18 18:30:34+02:00",
        "lat": 44.77024683728814,
        "lon": 0.7979628816246986,
        "pic": "",
        "ts": 1689697834,
        "dist": 10.0,
        "speed": 0.5714285714285714,
        "tdist": 25.0,
        "tdist2": 25.0,
        "type": "step",
    },
    {
        "alt": 59.4,
        "date": "2023-07-18 18:31:37+02:00",
        "lat": 44.77014499716461,
        "lon": 0.7983508799225092,
        "pic": "",
        "ts": 1689697897,
        "dist": 33.0,
        "speed": 1.885714285714286,
        "tdist": 58.0,
        "tdist2": 58.0,
        "type": "step",
    },
    {
        "alt": 72.4,
        "date": "2023-07-18 18:44:13+02:00",
        "lat": 44.770885412581265,
        "lon": 0.797738078981638,
        "pic": "",
        "ts": 1689698653,
        "dist": 96.0,
        "speed": 0.45714285714285713,
        "tdist": 154.0,
        "tdist2": 154.0,
        "type": "step",
    },
    {
        "alt": 62.4,
        "date": "2023-07-18 18:45:14+02:00",
        "lat": 44.77089459076524,
        "lon": 0.7978495582938194,
        "pic": "",
        "ts": 1689698714,
        "dist": 8.0,
        "speed": 0.4721311475409836,
        "tdist": 162.0,
        "tdist2": 162.0,
        "type": "step",
    },
    {
        "alt": 66.4,
        "date": "2023-07-18 18:49:07+02:00",
        "lat": 44.77090884000063,
        "lon": 0.7979210559278727,
        "pic": "",
        "ts": 1689698947,
        "dist": 6.0,
        "speed": 0.09270386266094421,
        "tdist": 168.0,
        "tdist2": 168.0,
        "type": "sos-past",
    },
    {
        "alt": 55.4,
        "date": "2023-07-18 18:50:21+02:00",
        "lat": 44.77089966181666,
        "lon": 0.7978481333702803,
        "pic": "",
        "ts": 1689699021,
        "dist": 6.0,
        "speed": 0.2918918918918919,
        "tdist": 174.0,
        "tdist2": 174.0,
        "type": "sos-past",
    },
    {
        "alt": 0.0,
        "date": "2023-07-18 18:50:22+02:00",
        "lat": 44.77089966181666,
        "lon": 0.7978481333702803,
        "pic": "",
        "ts": 1689699022,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 174.0,
        "tdist2": 174.0,
        "type": "pause",
    },
    {
        "alt": 69.4,
        "date": "2023-07-18 18:51:29+02:00",
        "lat": 44.77091148030013,
        "lon": 0.7979446928948164,
        "pic": "",
        "ts": 1689699089,
        "dist": 182.0,
        "speed": 9.77910447761194,
        "tdist": 356.0,
        "tdist2": 182.0,
        "type": "step",
    },
    {
        "alt": 76.4,
        "date": "2023-07-18 19:04:09+02:00",
        "lat": 44.77088323328644,
        "lon": 0.7978653162717819,
        "pic": "",
        "ts": 1689699849,
        "dist": 7.0,
        "speed": 0.0331578947368421,
        "tdist": 363.0,
        "tdist2": 189.0,
        "type": "step",
    },
    {
        "alt": 67.4,
        "date": "2023-07-18 19:07:37+02:00",
        "lat": 44.770444189198315,
        "lon": 0.7981211319565773,
        "pic": "",
        "ts": 1689700057,
        "dist": 53.0,
        "speed": 0.9173076923076923,
        "tdist": 416.0,
        "tdist2": 242.0,
        "type": "step",
    },
    {
        "alt": 64.4,
        "date": "2023-07-18 19:08:45+02:00",
        "lat": 44.77048978675157,
        "lon": 0.7980821561068296,
        "pic": "",
        "ts": 1689700125,
        "dist": 6.0,
        "speed": 0.31764705882352945,
        "tdist": 422.0,
        "tdist2": 248.0,
        "type": "step",
    },
    {
        "alt": 75.4,
        "date": "2023-07-18 19:16:57+02:00",
        "lat": 44.770517237484455,
        "lon": 0.7981850858777761,
        "pic": "",
        "ts": 1689700617,
        "dist": 8.0,
        "speed": 0.05853658536585367,
        "tdist": 430.0,
        "tdist2": 256.0,
        "type": "step",
    },
    {
        "alt": 75.4,
        "date": "2023-07-18 19:20:45+02:00",
        "lat": 44.770469879731536,
        "lon": 0.7980780489742756,
        "pic": "",
        "ts": 1689700845,
        "dist": 10.0,
        "speed": 0.15789473684210525,
        "tdist": 440.0,
        "tdist2": 266.0,
        "type": "step",
    },
    {
        "alt": 78.4,
        "date": "2023-07-18 19:22:00+02:00",
        "lat": 44.7704518167302,
        "lon": 0.7981756143271923,
        "pic": "",
        "ts": 1689700920,
        "dist": 8.0,
        "speed": 0.384,
        "tdist": 448.0,
        "tdist2": 274.0,
        "type": "step",
    },
    {
        "alt": 47.4,
        "date": "2023-07-18 19:23:08+02:00",
        "lat": 44.77049733046442,
        "lon": 0.798140661790967,
        "pic": "",
        "ts": 1689700988,
        "dist": 6.0,
        "speed": 0.31764705882352945,
        "tdist": 454.0,
        "tdist2": 280.0,
        "type": "step",
    },
    {
        "alt": 80.4,
        "date": "2023-07-18 19:29:33+02:00",
        "lat": 44.77050290443003,
        "lon": 0.7980679906904697,
        "pic": "",
        "ts": 1689701373,
        "dist": 6.0,
        "speed": 0.05610389610389611,
        "tdist": 460.0,
        "tdist2": 286.0,
        "type": "step",
    },
    {
        "alt": 79.4,
        "date": "2023-07-18 19:32:04+02:00",
        "lat": 44.77041108068079,
        "lon": 0.7980332896113396,
        "pic": "",
        "ts": 1689701524,
        "dist": 10.0,
        "speed": 0.2384105960264901,
        "tdist": 470.0,
        "tdist2": 296.0,
        "type": "step",
    },
    {
        "alt": 79.4,
        "date": "2023-07-18 19:32:05+02:00",
        "lat": 44.77041108068079,
        "lon": 0.7980332896113396,
        "pic": "",
        "ts": 1689701525,
        "dist": 0.0,
        "speed": 0.44,
        "tdist": 470.0,
        "tdist2": 296.0,
        "type": "pause",
    },
    {
        "alt": 68.4,
        "date": "2023-07-18 19:33:25+02:00",
        "lat": 44.770480818115175,
        "lon": 0.798122389242053,
        "pic": "",
        "ts": 1689701605,
        "dist": 307.0,
        "speed": 13.815,
        "tdist": 777.0,
        "tdist2": 307.0,
        "type": "step",
    },
    {
        "alt": 83.4,
        "date": "2023-07-18 19:34:34+02:00",
        "lat": 44.77041476871818,
        "lon": 0.7982177753001451,
        "pic": "",
        "ts": 1689701674,
        "dist": 10.0,
        "speed": 0.5217391304347826,
        "tdist": 787.0,
        "tdist2": 317.0,
        "type": "step",
    },
    {
        "alt": 76.4,
        "date": "2023-07-18 19:35:40+02:00",
        "lat": 44.770513088442385,
        "lon": 0.7981205452233553,
        "pic": "",
        "ts": 1689701740,
        "dist": 14.0,
        "speed": 0.7636363636363637,
        "tdist": 801.0,
        "tdist2": 331.0,
        "type": "step",
    },
    {
        "alt": 70.4,
        "date": "2023-07-18 19:36:52+02:00",
        "lat": 44.770572977140546,
        "lon": 0.798109145835042,
        "pic": "",
        "ts": 1689701812,
        "dist": 6.0,
        "speed": 0.3,
        "tdist": 807.0,
        "tdist2": 337.0,
        "type": "step",
    },
    {
        "alt": 65.4,
        "date": "2023-07-18 19:40:11+02:00",
        "lat": 44.77052520029247,
        "lon": 0.7980506401509047,
        "pic": "",
        "ts": 1689702011,
        "dist": 7.0,
        "speed": 0.12663316582914574,
        "tdist": 814.0,
        "tdist2": 344.0,
        "type": "step",
    },
    {
        "alt": 78.4,
        "date": "2023-07-18 19:41:21+02:00",
        "lat": 44.77044703904539,
        "lon": 0.7980849221348763,
        "pic": "",
        "ts": 1689702081,
        "dist": 10.0,
        "speed": 0.5142857142857142,
        "tdist": 824.0,
        "tdist2": 354.0,
        "type": "step",
    },
    {
        "alt": 78.4,
        "date": "2023-07-18 19:42:30+02:00",
        "lat": 44.7704335860908,
        "lon": 0.7981730159372091,
        "pic": "",
        "ts": 1689702150,
        "dist": 7.0,
        "speed": 0.3652173913043479,
        "tdist": 831.0,
        "tdist2": 361.0,
        "type": "step",
    },
    {
        "alt": 82.4,
        "date": "2023-07-18 19:43:48+02:00",
        "lat": 44.770494061522186,
        "lon": 0.7981248199939728,
        "pic": "",
        "ts": 1689702228,
        "dist": 7.0,
        "speed": 0.3230769230769231,
        "tdist": 838.0,
        "tdist2": 368.0,
        "type": "step",
    },
    {
        "alt": 67.4,
        "date": "2023-07-18 19:49:11+02:00",
        "lat": 44.77056857664138,
        "lon": 0.7980759534984827,
        "pic": "",
        "ts": 1689702551,
        "dist": 10.0,
        "speed": 0.11145510835913312,
        "tdist": 848.0,
        "tdist2": 378.0,
        "type": "step",
    },
    {
        "alt": 75.4,
        "date": "2023-07-18 19:50:16+02:00",
        "lat": 44.77047855500132,
        "lon": 0.7981041166931391,
        "pic": "",
        "ts": 1689702616,
        "dist": 10.0,
        "speed": 0.5538461538461539,
        "tdist": 858.0,
        "tdist2": 388.0,
        "type": "step",
    },
    {
        "alt": 73.4,
        "date": "2023-07-18 19:51:29+02:00",
        "lat": 44.770526960492134,
        "lon": 0.7980821561068296,
        "pic": "",
        "ts": 1689702689,
        "dist": 5.0,
        "speed": 0.2465753424657534,
        "tdist": 863.0,
        "tdist2": 393.0,
        "type": "step",
    },
    {
        "alt": 67.4,
        "date": "2023-07-18 19:56:52+02:00",
        "lat": 44.77047134656459,
        "lon": 0.7978533301502466,
        "pic": "",
        "ts": 1689703012,
        "dist": 20.0,
        "speed": 0.22291021671826625,
        "tdist": 883.0,
        "tdist2": 413.0,
        "type": "step",
    },
    {
        "alt": 64.4,
        "date": "2023-07-18 19:58:08+02:00",
        "lat": 44.77038694079965,
        "lon": 0.7979360595345497,
        "pic": "",
        "ts": 1689703088,
        "dist": 11.0,
        "speed": 0.5210526315789474,
        "tdist": 894.0,
        "tdist2": 424.0,
        "type": "step",
    },
    {
        "alt": 67.4,
        "date": "2023-07-18 20:06:25+02:00",
        "lat": 44.77045009844005,
        "lon": 0.7979208044707775,
        "pic": "",
        "ts": 1689703585,
        "dist": 7.0,
        "speed": 0.05070422535211268,
        "tdist": 901.0,
        "tdist2": 431.0,
        "type": "step",
    },
    {
        "alt": 76.4,
        "date": "2023-07-18 20:19:41+02:00",
        "lat": 44.770413218066096,
        "lon": 0.7980192918330431,
        "pic": "",
        "ts": 1689704381,
        "dist": 9.0,
        "speed": 0.0407035175879397,
        "tdist": 910.0,
        "tdist2": 440.0,
        "type": "step",
    },
    {
        "alt": 78.4,
        "date": "2023-07-18 20:31:24+02:00",
        "lat": 44.77034264244139,
        "lon": 0.7979436870664358,
        "pic": "",
        "ts": 1689705084,
        "dist": 10.0,
        "speed": 0.05120910384068279,
        "tdist": 920.0,
        "tdist2": 450.0,
        "type": "step",
    },
    {
        "alt": 68.4,
        "date": "2023-07-18 20:32:48+02:00",
        "lat": 44.77042298298329,
        "lon": 0.7979252468794584,
        "pic": "",
        "ts": 1689705168,
        "dist": 9.0,
        "speed": 0.3857142857142857,
        "tdist": 929.0,
        "tdist2": 459.0,
        "type": "end",
    },
]
EXPECTED_TRACES_TRIP_NZ = [
    {
        "alt": 89,
        "date": "2016-10-14 14:52:00+13:00",
        "lat": -36.8736861,
        "lon": 174.7583312,
        "pic": "",
        "ts": 1476409920,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "start",
    },
    {
        "alt": 10,
        "date": "2016-10-17 16:54:00+13:00",
        "lat": -36.733125,
        "lon": 174.7534399999999,
        "pic": "",
        "ts": 1476676440,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "pause",
    },
    {
        "alt": 25,
        "date": "2016-10-17 18:42:00+13:00",
        "lat": -36.7193817,
        "lon": 174.7513633,
        "pic": "",
        "ts": 1476682920,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "pause",
    },
    {
        "alt": 10,
        "date": "2016-10-19 11:55:00+13:00",
        "lat": -36.5962336,
        "lon": 174.6987899,
        "pic": "",
        "ts": 1476831300,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "pause",
    },
    {
        "alt": 33,
        "date": "2016-10-20 09:47:00+13:00",
        "lat": -36.4083297,
        "lon": 174.6590697,
        "pic": "",
        "ts": 1476910020,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "pause",
    },
    {
        "alt": 250,
        "date": "2016-10-20 13:22:00+13:00",
        "lat": -36.3087233,
        "lon": 174.6927233,
        "pic": "",
        "ts": 1476922920,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "pause",
    },
    {
        "alt": 432,
        "date": "2016-10-20 15:13:00+13:00",
        "lat": -36.2988817,
        "lon": 174.71439,
        "pic": "",
        "ts": 1476929580,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "pause",
    },
    {
        "alt": 17,
        "date": "2016-10-22 13:18:00+13:00",
        "lat": -36.160268333333335,
        "lon": 174.64769833333332,
        "pic": "",
        "ts": 1477095480,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "pause",
    },
    {
        "alt": 8,
        "date": "2016-10-23 12:32:00+13:00",
        "lat": -36.12640333333333,
        "lon": 174.57502166666666,
        "pic": "",
        "ts": 1477179120,
        "dist": 0.0,
        "speed": 0.0,
        "tdist": 0.0,
        "tdist2": 0.0,
        "type": "end",
    },
]


def test_get_all_traces_no_traces(tmp_path: Path) -> None:
    assert get_all_traces(tmp_path) == []


@pytest.mark.parametrize("trip, count", [(TRIP_FR, 37), (TRIP_NZ, 9)])
def test_get_all_traces(trip: Path, count: int) -> None:
    assert len(get_all_traces(trip)) == count


def test_adapt_traces_no_traces() -> None:
    assert adapt_traces([]) == []


@pytest.mark.parametrize(
    "trip, expected_traces", [(TRIP_FR, EXPECTED_TRACES_TRIP_FR), (TRIP_NZ, EXPECTED_TRACES_TRIP_NZ)]
)
def test_adapt_traces(trip: Path, expected_traces: list[dict]) -> None:
    for trace in adapt_traces(get_all_traces(trip)):
        print(f"{trace},")

    total_distance = 0.0
    for idx, trace in enumerate(adapt_traces(get_all_traces(trip))):
        assert trace == expected_traces[idx]

        # Check the total distance always goes up
        assert trace["tdist"] >= total_distance
        total_distance = trace["tdist"]


@pytest.mark.parametrize(
    "traces, expected",
    [
        (
            [
                {"type": "start"},
            ],
            [
                {"type": "start"},
            ],
        ),
        (
            [
                {"type": "sos"},
            ],
            [
                {"type": "sos"},
            ],
        ),
        (
            [
                {"type": "start"},
                {"type": "sos"},
                {"type": "sos"},
            ],
            [
                {"type": "start"},
                {"type": "sos"},
                {"type": "sos"},
            ],
        ),
        (
            [
                {"type": "start"},
                {"type": "sos"},
                {"type": "sos"},
                {"type": "end"},
            ],
            [
                {"type": "start"},
                {"type": "sos-past"},
                {"type": "sos-past"},
                {"type": "end"},
            ],
        ),
        (
            [
                {"type": "start"},
                {"type": "step"},
                {"type": "sos"},
                {"type": "sos"},
                {"type": "step"},
                {"type": "sos"},
                {"type": "sos"},
            ],
            [
                {"type": "start"},
                {"type": "step"},
                {"type": "sos-past"},
                {"type": "sos-past"},
                {"type": "step"},
                {"type": "sos"},
                {"type": "sos"},
            ],
        ),
        (
            [
                {"type": "start"},
                {"type": "step"},
                {"type": "sos"},
                {"type": "sos"},
                {"type": "step"},
                {"type": "sos"},
                {"type": "sos"},
                {"type": "end"},
            ],
            [
                {"type": "start"},
                {"type": "step"},
                {"type": "sos-past"},
                {"type": "sos-past"},
                {"type": "step"},
                {"type": "sos-past"},
                {"type": "sos-past"},
                {"type": "end"},
            ],
        ),
    ],
)
def test_check_for_sos(traces: list[dict], expected: list[dict]) -> None:
    assert check_for_sos(traces) == expected
