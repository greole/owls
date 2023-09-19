import Owls.parser.LogFile as lfp
import pathlib
import pytest


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
    timesteps = {time: cnt for time, cnt in logFile.time_steps_()}
    assert len(timesteps) == 100

    final_timestep_str = """
PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484754, Final residual = 4.87714e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234891, Final residual = 2.9262e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230027, Final residual = 2.57245e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0628781, Final residual = 0.00590879, No Iterations 9
time step continuity errors : sum local = 1.37969e-06, global = 9.72129e-19, cumulative = 1.25296e-16
nonePCG:  Solving for p, Initial residual = 0.0060665, Final residual = 7.59284e-07, No Iterations 149
time step continuity errors : sum local = 1.77299e-10, global = 1.04468e-18, cumulative = 1.26341e-16
ExecutionTime = 1.05 s  ClockTime = 2 s
"""
    assert timesteps[20] == final_timestep_str

    logFile = lfp.LogFile(fn)
    timesteps = {time: cnt for time, cnt in logFile.time_steps_(frequency=5)}
    assert len(timesteps) == 20


def test_lineParser():
    fn = "tests/log"
    line = (
        "smoothSolver:  Solving for Ux, Initial residual = 0.00484754, Final residual ="
        " 4.87714e-07, No Iterations 2"
    )
    logFile = lfp.LogFile(fn)

    parseResults = logFile.apply_line_parser_(line, lfp.transportEqn("Ux"))
    assert parseResults["solverName"] == "smoothSolver"
    assert parseResults["InitialResidual"] == "0.00484754"
    assert parseResults["FinalResidual"] == "4.87714e-07"
    assert parseResults["NoIterations"] == "2"
