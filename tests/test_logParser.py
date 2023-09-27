import Owls.parser.LogFile as lfp
import pathlib
import pytest

final_timestep_str = """
PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484754, Final residual = 4.87714e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234891, Final residual = 2.9262e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230027, Final residual = 2.57245e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0628781, Final residual = 0.00590879, No Iterations 9
time step continuity errors : sum local = 1.37969e-06, global = 9.72129e-19, cumulative = 1.25296e-16
nonePCG:  Solving for p, Initial residual = 0.0060665, Final residual = 7.59284e-07, No Iterations 149
time step continuity errors : sum local = 1.77299e-10, global = 1.04468e-18, cumulative = 1.26341e-16
ExecutionTime = 1.05 s  ClockTime = 2 s"""


def test_logParser_raises_if_not_exist():
    fn = "does_not_exist"
    with pytest.raises(FileNotFoundError):
        logFile = lfp.LogFile(fn)


def test_logHeaderParser():
    fn = "tests/log"
    logFile = lfp.LogFile(fn)

    assert pathlib.Path(fn).exists()
    assert logFile.header.Build == "51ed7a6034-20230103"
    assert logFile.header.Arch == "LSB;label=32;scalar=64"
    assert logFile.header.Exec == "pimpleFoam"
    assert logFile.header.Host == "MacBook-Pro-8.local"
    assert logFile.header.PID == 71972
    assert logFile.header.IO == "uncollated"
    assert logFile.header.Case == "/Users/go/Downloads/periodicPlaneChannel100"
    assert logFile.header.nProcs == 4


def test_logFooter():
    fn = "tests/log"
    logFile = lfp.LogFile(fn)

    assert pathlib.Path(fn).exists()
    assert logFile.footer.completed == True


def test_latestTime():
    fn = "tests/log"
    logFile = lfp.LogFile(fn)

    assert pathlib.Path(fn).exists()
    assert logFile.latestTime.time == 20.0
    assert logFile.latestTime.continuity_errors != {}
    assert (
        logFile.latestTime.continuity_errors["timeStepContErrors_cumulative"]
        == "1.25296e-16"
    )


def test_ExecutionTime():
    fn = "tests/log"
    logFile = lfp.LogFile(fn)

    assert pathlib.Path(fn).exists()
    assert logFile.latestTime.execution_time != {}
    assert logFile.latestTime.execution_time["ExecutionTime"] == 1.05
    assert logFile.latestTime.execution_time["ClockTime"] == 2.0


def test_footerParser():
    fn = "tests/log"
    logFile = lfp.LogFile(fn)
    assert "End" in logFile.footer.content
    assert "Finalising parallel run" in logFile.footer.content


def test_footerParser():
    fn = "tests/log"
    logFile = lfp.LogFile(fn)
    assert "End" in logFile.footer.content
    assert "Finalising parallel run" in logFile.footer.content


def test_timeStepParser():
    fn = "tests/log"
    logFile = lfp.LogFile(fn)
    timesteps = {time: cnt for time, cnt in logFile._LogFile__time_steps()}
    assert len(timesteps) == 100

    assert timesteps[20] == [e + "\n" for e in final_timestep_str.split("\n")]

    logFile = lfp.LogFile(fn)
    timesteps = {time: cnt for time, cnt in logFile._LogFile__time_steps(frequency=5)}
    assert len(timesteps) == 20


def test_applyTransportEqnLineParser():
    fn = "tests/log"
    line = (
        "smoothSolver:  Solving for Ux, Initial residual = 0.00484754, Final residual ="
        " 4.87714e-07, No Iterations 2"
    )
    logFile = lfp.LogFile(fn)

    parseResults = lfp.apply_line_parser_(line, lfp.transportEqn("Ux"))
    assert parseResults["Ux_solverName"] == "smoothSolver"
    assert parseResults["Ux_InitialResidual"] == "0.00484754"
    assert parseResults["Ux_FinalResidual"] == "4.87714e-07"
    assert parseResults["Ux_NoIterations"] == "2"
    assert parseResults["Ux_count"] == 1


def test_applyCustomLineParser():
    fn = "tests/log"

    line = "[OGL LOG][Proc: 0]Ux_local_cols: call_init: 0.029 [ms]"
    logFile = lfp.LogFile(fn)

    matcher = lfp.customMatcher(
        "Ux_local_cols",
        (
            r"\[OGL LOG\]\[Proc: 0\]Ux_local_cols: call_init:"
            r" (?P<Ux_local_cols>[0-9.]*) \[ms\]"
        ),
    )

    parseResults = lfp.apply_line_parser_(line, matcher)
    assert parseResults != {}
    assert parseResults["Ux_local_cols"] == "0.029"


def test_CourantNumberParser():
    fn = "tests/log"

    line ="Courant Number mean: 4.8777e-04 max: 0.852134"
    logFile = lfp.LogFile(fn)

    matcher = lfp.CourantNumber()

    parseResults = lfp.apply_line_parser_(line, matcher)
    assert parseResults != {}
    assert parseResults["CourantNumber_mean"] == "4.8777e-04"
    assert parseResults["CourantNumber_max"] == "0.852134"


def test_parseInnerLoops():
    matcher = [
        lfp.transportEqn("Ux"),
    ]

    splitter = lfp.PimpleMatcher()

    lines = """
PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484754, Final residual = 4.87714e-07, No Iterations 2
PIMPLE: iteration 2
smoothSolver:  Solving for Ux, Initial residual = 0.00584754, Final residual = 5.87714e-07, No Iterations 2
    """.split(
        "\n"
    )
    fn = "tests/log"
    logFile = lfp.LogFile(fn)
    parseResults = [
        d for d in logFile._LogFile__parse_inner_loops(lines, matcher, splitter, {})
    ]
    assert parseResults == [
        {
            "PIMPLEIteration": "1",
            "PIMPLE_count": 1,
            "Ux_FinalResidual": "4.87714e-07",
            "Ux_InitialResidual": "0.00484754",
            "Ux_NoIterations": "2",
            "Ux_solverName": "smoothSolver",
            "Ux_count": 1,
        },
        {
            "PIMPLEIteration": "2",
            "PIMPLE_count": 2,
            "Ux_FinalResidual": "5.87714e-07",
            "Ux_InitialResidual": "0.00584754",
            "Ux_NoIterations": "2",
            "Ux_solverName": "smoothSolver",
            "Ux_count": 1,
        },
    ]


def test_parseInnerLoops_innerCount():
    lines = """
PIMPLE: iteration 1
nonePCG:  Solving for p, Initial residual = 0.0596912, Final residual = 0.00535372, No Iterations 9
time step continuity errors : sum local = 1.24653e-06, global = 9.30614e-19, cumulative = 1.23404e-16
nonePCG:  Solving for p, Initial residual = 0.00552749, Final residual = 8.77802e-07, No Iterations 149
time step continuity errors : sum local = 2.05781e-10, global = 9.19636e-19, cumulative = 1.24324e-16
PIMPLE: iteration 2
nonePCG:  Solving for p, Initial residual = 0.0596912, Final residual = 0.00535372, No Iterations 9
time step continuity errors : sum local = 1.24653e-06, global = 9.30614e-19, cumulative = 1.23404e-16
nonePCG:  Solving for p, Initial residual = 0.00552749, Final residual = 8.77802e-07, No Iterations 149
time step continuity errors : sum local = 2.05781e-10, global = 9.19636e-19, cumulative = 1.24324e-16
""".split(
        "\n"
    )
    fn = "tests/log"
    logFile = lfp.LogFile(fn)
    matcher = [
        lfp.transportEqn("p"),
    ]

    splitter = lfp.PimpleMatcher()
    parseResults = [
        d for d in logFile._LogFile__parse_inner_loops(lines, matcher, splitter, {})
    ]
    assert parseResults == [
        {
            "PIMPLEIteration": "1",
            "PIMPLE_count": 1,
            "p_FinalResidual": "0.00535372",
            "p_InitialResidual": "0.0596912",
            "p_NoIterations": "9",
            "p_count": 1,
            "p_solverName": "nonePCG",
        },
        {
            "PIMPLEIteration": "1",
            "PIMPLE_count": 1,
            "p_FinalResidual": "8.77802e-07",
            "p_InitialResidual": "0.00552749",
            "p_NoIterations": "149",
            "p_count": 2,
            "p_solverName": "nonePCG",
        },
        {
            "PIMPLEIteration": "2",
            "PIMPLE_count": 2,
            "p_FinalResidual": "0.00535372",
            "p_InitialResidual": "0.0596912",
            "p_NoIterations": "9",
            "p_count": 1,
            "p_solverName": "nonePCG",
        },
        {
            "PIMPLEIteration": "2",
            "PIMPLE_count": 2,
            "p_FinalResidual": "8.77802e-07",
            "p_InitialResidual": "0.00552749",
            "p_NoIterations": "149",
            "p_count": 2,
            "p_solverName": "nonePCG",
        },
    ]


def test_parseInnerLoops_innerCount_multiMatcher():
    lines = """
PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484754, Final residual = 4.87714e-07, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0596912, Final residual = 0.00535372, No Iterations 9
time step continuity errors : sum local = 1.24653e-06, global = 9.30614e-19, cumulative = 1.23404e-16
nonePCG:  Solving for p, Initial residual = 0.00552749, Final residual = 8.77802e-07, No Iterations 149
time step continuity errors : sum local = 2.05781e-10, global = 9.19636e-19, cumulative = 1.24324e-16
PIMPLE: iteration 2
smoothSolver:  Solving for Ux, Initial residual = 0.00584754, Final residual = 5.87714e-07, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0596912, Final residual = 0.00535372, No Iterations 9
time step continuity errors : sum local = 1.24653e-06, global = 9.30614e-19, cumulative = 1.23404e-16
nonePCG:  Solving for p, Initial residual = 0.00552749, Final residual = 8.77802e-07, No Iterations 149
time step continuity errors : sum local = 2.05781e-10, global = 9.19636e-19, cumulative = 1.24324e-16
""".split(
        "\n"
    )
    fn = "tests/log"
    logFile = lfp.LogFile(fn)
    matcher = [
        lfp.transportEqn("Ux"),
        lfp.transportEqn("p"),
    ]

    splitter = lfp.PimpleMatcher()
    parseResults = [
        d for d in logFile._LogFile__parse_inner_loops(lines, matcher, splitter, {})
    ]
    assert len(parseResults) == 6
    assert parseResults == [
        {
            "PIMPLEIteration": "1",
            "PIMPLE_count": 1,
            "Ux_solverName": "smoothSolver",
            "Ux_FinalResidual": "4.87714e-07",
            "Ux_InitialResidual": "0.00484754",
            "Ux_NoIterations": "2",
            "Ux_count": 1,
        },
        {
            "PIMPLEIteration": "1",
            "PIMPLE_count": 1,
            "p_FinalResidual": "0.00535372",
            "p_InitialResidual": "0.0596912",
            "p_NoIterations": "9",
            "p_count": 1,
            "p_solverName": "nonePCG",
        },
        {
            "PIMPLEIteration": "1",
            "PIMPLE_count": 1,
            "p_FinalResidual": "8.77802e-07",
            "p_InitialResidual": "0.00552749",
            "p_NoIterations": "149",
            "p_count": 2,
            "p_solverName": "nonePCG",
        },
        {
            "PIMPLEIteration": "2",
            "PIMPLE_count": 2,
            "Ux_solverName": "smoothSolver",
            "Ux_FinalResidual": "5.87714e-07",
            "Ux_InitialResidual": "0.00584754",
            "Ux_NoIterations": "2",
            "Ux_count": 1,
        },
        {
            "PIMPLEIteration": "2",
            "PIMPLE_count": 2,
            "p_FinalResidual": "0.00535372",
            "p_InitialResidual": "0.0596912",
            "p_NoIterations": "9",
            "p_count": 1,
            "p_solverName": "nonePCG",
        },
        {
            "PIMPLEIteration": "2",
            "PIMPLE_count": 2,
            "p_FinalResidual": "8.77802e-07",
            "p_InitialResidual": "0.00552749",
            "p_NoIterations": "149",
            "p_count": 2,
            "p_solverName": "nonePCG",
        },
    ]


def test_parseToRecords():
    fn = "tests/log"
    matcher = [
        lfp.transportEqn("Ux"),
        lfp.transportEqn("p"),
    ]

    logFile = lfp.LogFile(fn, matcher=matcher)

    records = list(logFile.parse_to_records())

    assert len(records) > 1
    assert records[0]["Time"] == 0.2
    assert records[0]["Ux_count"] == 1
    assert records[1]["Time"] == 0.2
    assert records[1]["p_count"] == 1


def test_parseToDataFrame():
    fn = "tests/log"
    matcher = [
        lfp.transportEqn("Ux"),
        lfp.transportEqn("Uy"),
        lfp.transportEqn("p"),
    ]

    logFile = lfp.LogFile(fn, matcher=matcher)

    df = logFile.parse_to_df()
