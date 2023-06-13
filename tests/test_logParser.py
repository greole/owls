from Owls.parser.LogFile import LogFile, LogKey

log_str = """
/*---------------------------------------------------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  2212                                  |
|   \\  /    A nd           | Website:  www.openfoam.com                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
Build  : 51ed7a6034-20230103 OPENFOAM=2212 version=v2212
Arch   : "LSB;label=32;scalar=64"
Exec   : pimpleFoam -parallel
Date   : Jun 13 2023
Time   : 09:48:05
Host   : MacBook-Pro-8.local
PID    : 71972
I/O    : uncollated
Case   : /Users/go/Downloads/periodicPlaneChannel100
nProcs : 4
Hosts  :
(
    (MacBook-Pro-8.local 4)
)
Pstream initialized with:
    floatTransfer      : 0
    nProcsSimpleSum    : 0
    commsType          : nonBlocking
    polling iterations : 0
trapFpe: Floating point exception trapping enabled (FOAM_SIGFPE).
fileModificationChecking : Monitoring run-time modified files using timeStampMaster (fileModificationSkew 5, maxFileModificationPolls 20)
allowSystemOperations : Allowing user-supplied system call operations

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
Create time

--> FOAM Warning :
    From void *Foam::dlLibraryTable::openLibrary(const Foam::fileName &, bool)
    in file db/dynamicLibrary/dlLibraryTable/dlLibraryTable.C at line 188
    Could not load "libOGL.so"
dlopen(libOGL.dylib, 0x0009): tried: '/Users/go/OpenFOAM/openfoam/platforms/darwin64ClangDPInt32Opt/lib/sys-openmpi/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/openfoam/platforms/darwin64ClangDPInt32Opt/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64ClangDPInt32/lib/sys-openmpi/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64ClangDPInt32/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64Clang/fftw-3.3.10/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64Clang/boost_1_74_0/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64Clang/ADIOS2-2.8.3/lib/libOGL.dylib' (no such file), '/usr/local/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/openfoam/platforms/darwin64ClangDPInt32Opt/lib/dummy/libOGL.dylib' (no such file), 'libOGL.dylib' (no such file), '/usr/local/lib/libOGL.dylib' (no such file), '/usr/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/openfoam/platforms/darwin64ClangDPInt32Opt/lib/sys-openmpi/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/openfoam/platforms/darwin64ClangDPInt32Opt/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64ClangDPInt32/lib/sys-openmpi/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64ClangDPInt32/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64Clang/fftw-3.3.10/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64Clang/boost_1_74_0/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/ThirdParty-v2212/platforms/darwin64Clang/ADIOS2-2.8.3/lib/libOGL.dylib' (no such file), '/usr/local/lib/libOGL.dylib' (no such file), '/Users/go/OpenFOAM/openfoam/platforms/darwin64ClangDPInt32Opt/lib/dummy/libOGL.dylib' (no such file), '/Users/go/Downloads/periodicPlaneChannel100/libOGL.dylib' (no such file)
Create mesh for time = 0


PIMPLE: Operating solver in PISO mode

Reading field p

Reading field U

Reading/calculating face flux field phi

Selecting incompressible transport model Newtonian
Selecting turbulence model type LES
Selecting LES turbulence model WALE
Selecting LES delta type cubeRootVol
LES
{
    LESModel        WALE;
    turbulence      on;
    printCoeffs     on;
    delta           cubeRootVol;
    cubeRootVolCoeffs
    {
        deltaCoeff      1;
    }
    PrandtlCoeffs
    {
        delta           cubeRootVol;
        cubeRootVolCoeffs
        {
            deltaCoeff      1;
        }
        smoothCoeffs
        {
            delta           cubeRootVol;
            cubeRootVolCoeffs
            {
                deltaCoeff      1;
            }
            maxDeltaRatio   1.1;
        }
        Cdelta          0.158;
    }
    vanDriestCoeffs
    {
        delta           cubeRootVol;
        cubeRootVolCoeffs
        {
            deltaCoeff      1;
        }
        smoothCoeffs
        {
            delta           cubeRootVol;
            cubeRootVolCoeffs
            {
                deltaCoeff      1;
            }
            maxDeltaRatio   1.1;
        }
        Aplus           26;
        Cdelta          0.158;
    }
    smoothCoeffs
    {
        delta           cubeRootVol;
        cubeRootVolCoeffs
        {
            deltaCoeff      1;
        }
        maxDeltaRatio   1.1;
    }
    Ck              0.094;
    Cw              0.325;
}

No MRF models present

Creating finite volume options from "constant/fvOptions"

No finite volume options present
Courant Number mean: 0.0775689 max: 0.113959
Courant Number mean: 0.0775689 max: 0.113959

Starting time loop

fieldAverage fieldAverage1:
    Restarting averaging for fields:
        U: starting averaging at time 0
        p: starting averaging at time 0

Courant Number mean: 0.0775689 max: 0.113959
Time = 0.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00866523, Final residual = 2.13805e-06, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0247056, Final residual = 6.78964e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0231872, Final residual = 5.74961e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.933003, Final residual = 0.0920767, No Iterations 10
time step continuity errors : sum local = 0.000356771, global = 9.08019e-20, cumulative = 9.08019e-20
nonePCG:  Solving for p, Initial residual = 0.0511721, Final residual = 9.52115e-07, No Iterations 175
time step continuity errors : sum local = 6.85349e-09, global = 2.8329e-19, cumulative = 3.74092e-19
ExecutionTime = 0.02 s  ClockTime = 0 s

fieldAverage fieldAverage1:
    Reading/initialising field UMean
    Reading/initialising field pMean
    Reading/initialising field UPrime2Mean
    Reading/initialising field pPrime2Mean

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0767906 max: 0.104539
Time = 0.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0075392, Final residual = 7.77319e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.108984, Final residual = 2.62263e-07, No Iterations 3
smoothSolver:  Solving for Uz, Initial residual = 0.0631878, Final residual = 6.11538e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.799871, Final residual = 0.0717895, No Iterations 13
time step continuity errors : sum local = 0.000234277, global = 1.96978e-19, cumulative = 5.7107e-19
nonePCG:  Solving for p, Initial residual = 0.136301, Final residual = 9.68444e-07, No Iterations 179
time step continuity errors : sum local = 1.69448e-09, global = 4.04749e-20, cumulative = 6.11545e-19
ExecutionTime = 0.04 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0767218 max: 0.103603
Time = 0.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00496642, Final residual = 5.62883e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0388166, Final residual = 4.64524e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0293799, Final residual = 3.0385e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.625657, Final residual = 0.0591432, No Iterations 13
time step continuity errors : sum local = 7.6953e-05, global = 1.45097e-19, cumulative = 7.56641e-19
nonePCG:  Solving for p, Initial residual = 0.0875038, Final residual = 8.08714e-07, No Iterations 177
time step continuity errors : sum local = 7.24788e-10, global = 9.9709e-20, cumulative = 8.5635e-19
ExecutionTime = 0.05 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0766379 max: 0.103013
Time = 0.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00464983, Final residual = 5.15802e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.027728, Final residual = 3.18566e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0235997, Final residual = 2.58276e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.182985, Final residual = 0.0132486, No Iterations 9
time step continuity errors : sum local = 1.01037e-05, global = 3.42032e-19, cumulative = 1.19838e-18
nonePCG:  Solving for p, Initial residual = 0.015757, Final residual = 8.79849e-07, No Iterations 153
time step continuity errors : sum local = 5.73571e-10, global = 2.3497e-19, cumulative = 1.43335e-18
ExecutionTime = 0.05 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0765511 max: 0.102522
Time = 1

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00457077, Final residual = 5.06845e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0251227, Final residual = 2.99315e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0228033, Final residual = 2.51832e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.129493, Final residual = 0.0127638, No Iterations 8
time step continuity errors : sum local = 7.65979e-06, global = 1.42884e-19, cumulative = 1.57624e-18
nonePCG:  Solving for p, Initial residual = 0.0142687, Final residual = 9.10159e-07, No Iterations 147
time step continuity errors : sum local = 4.93849e-10, global = 1.98354e-19, cumulative = 1.77459e-18
ExecutionTime = 0.07 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0764852 max: 0.102024
Time = 1.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00453777, Final residual = 5.0351e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0241919, Final residual = 2.89995e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225646, Final residual = 2.51807e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0968136, Final residual = 0.00934279, No Iterations 8
time step continuity errors : sum local = 4.76251e-06, global = 2.33105e-19, cumulative = 2.00769e-18
nonePCG:  Solving for p, Initial residual = 0.0100967, Final residual = 9.16673e-07, No Iterations 139
time step continuity errors : sum local = 4.33496e-10, global = 2.2459e-19, cumulative = 2.23228e-18
ExecutionTime = 0.08 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0764424 max: 0.101493
Time = 1.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00452057, Final residual = 5.00985e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0238303, Final residual = 2.87536e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022529, Final residual = 2.52086e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0813877, Final residual = 0.00748356, No Iterations 8
time step continuity errors : sum local = 3.41081e-06, global = 4.13161e-19, cumulative = 2.64545e-18
nonePCG:  Solving for p, Initial residual = 0.00800433, Final residual = 9.20149e-07, No Iterations 138
time step continuity errors : sum local = 3.93223e-10, global = 3.47149e-19, cumulative = 2.99259e-18
ExecutionTime = 0.09 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0764043 max: 0.101424
Time = 1.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00450975, Final residual = 4.99241e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236446, Final residual = 2.86698e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225604, Final residual = 2.53105e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0662081, Final residual = 0.00587871, No Iterations 8
time step continuity errors : sum local = 2.4566e-06, global = 1.40285e-19, cumulative = 3.13288e-18
nonePCG:  Solving for p, Initial residual = 0.00616094, Final residual = 7.59922e-07, No Iterations 147
time step continuity errors : sum local = 3.0523e-10, global = 3.34049e-21, cumulative = 3.13622e-18
ExecutionTime = 0.1 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0763717 max: 0.102103
Time = 1.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00450951, Final residual = 4.98617e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235527, Final residual = 2.86729e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225227, Final residual = 2.54493e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0657621, Final residual = 0.00445993, No Iterations 9
time step continuity errors : sum local = 1.74306e-06, global = 4.53073e-19, cumulative = 3.58929e-18
nonePCG:  Solving for p, Initial residual = 0.00469466, Final residual = 9.84568e-07, No Iterations 145
time step continuity errors : sum local = 3.73693e-10, global = 2.21674e-19, cumulative = 3.81097e-18
ExecutionTime = 0.11 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0763437 max: 0.103139
Time = 2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00450966, Final residual = 4.97874e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234828, Final residual = 2.85831e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022546, Final residual = 2.56605e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0662688, Final residual = 0.00644866, No Iterations 8
time step continuity errors : sum local = 2.37658e-06, global = 4.59476e-19, cumulative = 4.27044e-18
nonePCG:  Solving for p, Initial residual = 0.0067794, Final residual = 8.75822e-07, No Iterations 148
time step continuity errors : sum local = 3.1336e-10, global = 3.34788e-19, cumulative = 4.60523e-18
ExecutionTime = 0.12 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0763223 max: 0.104131
Time = 2.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00451424, Final residual = 4.98107e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235348, Final residual = 2.86401e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225376, Final residual = 2.569e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0612224, Final residual = 0.00419372, No Iterations 9
time step continuity errors : sum local = 1.47974e-06, global = 3.75251e-19, cumulative = 4.98048e-18
nonePCG:  Solving for p, Initial residual = 0.00442864, Final residual = 9.26859e-07, No Iterations 148
time step continuity errors : sum local = 3.17028e-10, global = 3.20488e-19, cumulative = 5.30097e-18
ExecutionTime = 0.13 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0763042 max: 0.105075
Time = 2.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00451802, Final residual = 4.98935e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235437, Final residual = 2.87473e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022571, Final residual = 2.57031e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0603406, Final residual = 0.00444528, No Iterations 9
time step continuity errors : sum local = 1.51508e-06, global = 2.70923e-19, cumulative = 5.57189e-18
nonePCG:  Solving for p, Initial residual = 0.00472019, Final residual = 9.72938e-07, No Iterations 135
time step continuity errors : sum local = 3.18824e-10, global = 5.35281e-19, cumulative = 6.10718e-18
ExecutionTime = 0.14 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762913 max: 0.10598
Time = 2.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00451986, Final residual = 5.01165e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235792, Final residual = 2.88434e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225785, Final residual = 2.56984e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0631653, Final residual = 0.00506705, No Iterations 9
time step continuity errors : sum local = 1.62935e-06, global = 3.91785e-19, cumulative = 6.49896e-18
nonePCG:  Solving for p, Initial residual = 0.00534288, Final residual = 8.13973e-07, No Iterations 149
time step continuity errors : sum local = 2.57217e-10, global = 6.25998e-19, cumulative = 7.12496e-18
ExecutionTime = 0.15 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762812 max: 0.106815
Time = 2.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00452313, Final residual = 5.0264e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235649, Final residual = 2.91446e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226155, Final residual = 2.57705e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0559779, Final residual = 0.00424713, No Iterations 9
time step continuity errors : sum local = 1.32793e-06, global = 5.08379e-19, cumulative = 7.63334e-18
nonePCG:  Solving for p, Initial residual = 0.00444295, Final residual = 9.4083e-07, No Iterations 146
time step continuity errors : sum local = 2.8928e-10, global = 3.69826e-19, cumulative = 8.00316e-18
ExecutionTime = 0.16 s  ClockTime = 0 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762713 max: 0.107597
Time = 3

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00452937, Final residual = 5.03072e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236135, Final residual = 2.93996e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.02259, Final residual = 2.58286e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0581903, Final residual = 0.0048978, No Iterations 9
time step continuity errors : sum local = 1.48866e-06, global = 4.69299e-19, cumulative = 8.47246e-18
nonePCG:  Solving for p, Initial residual = 0.00510181, Final residual = 7.81726e-07, No Iterations 149
time step continuity errors : sum local = 2.33462e-10, global = 2.29402e-19, cumulative = 8.70186e-18
ExecutionTime = 0.17 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762631 max: 0.108313
Time = 3.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00453534, Final residual = 5.01044e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236376, Final residual = 2.95918e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226081, Final residual = 2.60696e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0564203, Final residual = 0.00456974, No Iterations 9
time step continuity errors : sum local = 1.35377e-06, global = 5.48644e-19, cumulative = 9.25051e-18
nonePCG:  Solving for p, Initial residual = 0.00478735, Final residual = 9.87371e-07, No Iterations 145
time step continuity errors : sum local = 2.8756e-10, global = 5.30628e-19, cumulative = 9.78114e-18
ExecutionTime = 0.18 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762618 max: 0.108958
Time = 3.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00454095, Final residual = 4.99751e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236418, Final residual = 2.96909e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226289, Final residual = 2.61909e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0596302, Final residual = 0.0053514, No Iterations 9
time step continuity errors : sum local = 1.53469e-06, global = 4.96785e-19, cumulative = 1.02779e-17
nonePCG:  Solving for p, Initial residual = 0.00560467, Final residual = 9.77896e-07, No Iterations 148
time step continuity errors : sum local = 2.76053e-10, global = 2.61287e-19, cumulative = 1.05392e-17
ExecutionTime = 0.2 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762609 max: 0.109533
Time = 3.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00454417, Final residual = 4.98283e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237178, Final residual = 2.97975e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226248, Final residual = 2.63068e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.054665, Final residual = 0.00511939, No Iterations 9
time step continuity errors : sum local = 1.42448e-06, global = 5.38051e-19, cumulative = 1.10773e-17
nonePCG:  Solving for p, Initial residual = 0.00534889, Final residual = 8.4864e-07, No Iterations 148
time step continuity errors : sum local = 2.34303e-10, global = 4.97618e-19, cumulative = 1.15749e-17
ExecutionTime = 0.2 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762612 max: 0.11004
Time = 3.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00454871, Final residual = 4.96478e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237661, Final residual = 2.98224e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225921, Final residual = 2.6352e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0550489, Final residual = 0.00527746, No Iterations 9
time step continuity errors : sum local = 1.43056e-06, global = 3.91605e-19, cumulative = 1.19665e-17
nonePCG:  Solving for p, Initial residual = 0.0055083, Final residual = 8.54109e-07, No Iterations 149
time step continuity errors : sum local = 2.28613e-10, global = 4.52482e-19, cumulative = 1.2419e-17
ExecutionTime = 0.21 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762597 max: 0.110475
Time = 4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00455646, Final residual = 4.95446e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237397, Final residual = 2.97232e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226276, Final residual = 2.64474e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0506643, Final residual = 0.0046463, No Iterations 9
time step continuity errors : sum local = 1.24339e-06, global = 2.6231e-19, cumulative = 1.26813e-17
nonePCG:  Solving for p, Initial residual = 0.00478854, Final residual = 9.13825e-07, No Iterations 148
time step continuity errors : sum local = 2.40656e-10, global = 4.0369e-19, cumulative = 1.3085e-17
ExecutionTime = 0.23 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762539 max: 0.110833
Time = 4.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00456399, Final residual = 4.94754e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237094, Final residual = 2.96854e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022598, Final residual = 2.64163e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0513725, Final residual = 0.00504826, No Iterations 9
time step continuity errors : sum local = 1.32503e-06, global = 3.067e-19, cumulative = 1.33917e-17
nonePCG:  Solving for p, Initial residual = 0.00520834, Final residual = 9.87013e-07, No Iterations 146
time step continuity errors : sum local = 2.53589e-10, global = 4.12761e-19, cumulative = 1.38044e-17
ExecutionTime = 0.23 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762447 max: 0.111116
Time = 4.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00456921, Final residual = 4.9495e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236479, Final residual = 2.96493e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225658, Final residual = 2.64275e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0504315, Final residual = 0.00383068, No Iterations 9
time step continuity errors : sum local = 9.91354e-07, global = 2.87348e-19, cumulative = 1.40918e-17
nonePCG:  Solving for p, Initial residual = 0.00400653, Final residual = 8.34449e-07, No Iterations 146
time step continuity errors : sum local = 2.12378e-10, global = 1.79611e-19, cumulative = 1.42714e-17
ExecutionTime = 0.24 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762325 max: 0.111323
Time = 4.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00457824, Final residual = 4.95423e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.023623, Final residual = 2.94485e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225364, Final residual = 2.63838e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0513276, Final residual = 0.00463789, No Iterations 9
time step continuity errors : sum local = 1.17478e-06, global = 3.30756e-19, cumulative = 1.46021e-17
nonePCG:  Solving for p, Initial residual = 0.00481103, Final residual = 9.97223e-07, No Iterations 135
time step continuity errors : sum local = 2.53044e-10, global = 2.65926e-19, cumulative = 1.48681e-17
ExecutionTime = 0.26 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762206 max: 0.111449
Time = 4.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00458462, Final residual = 4.96173e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.023602, Final residual = 2.90876e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0224986, Final residual = 2.64076e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0498604, Final residual = 0.00456179, No Iterations 9
time step continuity errors : sum local = 1.15217e-06, global = 3.4051e-19, cumulative = 1.52086e-17
nonePCG:  Solving for p, Initial residual = 0.004713, Final residual = 9.69333e-07, No Iterations 135
time step continuity errors : sum local = 2.44631e-10, global = 3.83603e-19, cumulative = 1.55922e-17
ExecutionTime = 0.26 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0762091 max: 0.111498
Time = 5

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00458425, Final residual = 4.987e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236237, Final residual = 2.88031e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0224772, Final residual = 2.63006e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0521602, Final residual = 0.00516519, No Iterations 9
time step continuity errors : sum local = 1.29285e-06, global = 4.13667e-19, cumulative = 1.60058e-17
nonePCG:  Solving for p, Initial residual = 0.00533693, Final residual = 8.86447e-07, No Iterations 148
time step continuity errors : sum local = 2.21554e-10, global = 2.50102e-19, cumulative = 1.62559e-17
ExecutionTime = 0.27 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0761949 max: 0.111471
Time = 5.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00459211, Final residual = 5.02006e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236326, Final residual = 2.86472e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022484, Final residual = 2.61784e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0508371, Final residual = 0.00437229, No Iterations 10
time step continuity errors : sum local = 1.09286e-06, global = 4.53237e-19, cumulative = 1.67092e-17
nonePCG:  Solving for p, Initial residual = 0.00451322, Final residual = 8.94799e-07, No Iterations 146
time step continuity errors : sum local = 2.2392e-10, global = 2.49347e-19, cumulative = 1.69585e-17
ExecutionTime = 0.28 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0761847 max: 0.111359
Time = 5.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00459937, Final residual = 5.04012e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236561, Final residual = 2.84054e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0224915, Final residual = 2.61966e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0575251, Final residual = 0.00545868, No Iterations 10
time step continuity errors : sum local = 1.35244e-06, global = 8.66938e-20, cumulative = 1.70452e-17
nonePCG:  Solving for p, Initial residual = 0.00574752, Final residual = 8.92204e-07, No Iterations 148
time step continuity errors : sum local = 2.17605e-10, global = 4.46397e-19, cumulative = 1.74916e-17
ExecutionTime = 0.29 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0761706 max: 0.111175
Time = 5.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00459997, Final residual = 5.06634e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236716, Final residual = 2.80483e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225122, Final residual = 2.63187e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0508198, Final residual = 0.00438093, No Iterations 10
time step continuity errors : sum local = 1.06836e-06, global = 3.93455e-19, cumulative = 1.78851e-17
nonePCG:  Solving for p, Initial residual = 0.00452443, Final residual = 8.60653e-07, No Iterations 146
time step continuity errors : sum local = 2.10827e-10, global = 2.88041e-19, cumulative = 1.81731e-17
ExecutionTime = 0.3 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.076155 max: 0.110917
Time = 5.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0046024, Final residual = 5.09167e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237178, Final residual = 2.77518e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225239, Final residual = 2.64006e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0504292, Final residual = 0.00467464, No Iterations 9
time step continuity errors : sum local = 1.14342e-06, global = 2.61299e-19, cumulative = 1.84344e-17
nonePCG:  Solving for p, Initial residual = 0.00480735, Final residual = 8.42845e-07, No Iterations 146
time step continuity errors : sum local = 2.06637e-10, global = 2.19475e-19, cumulative = 1.86539e-17
ExecutionTime = 0.31 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0761397 max: 0.110582
Time = 6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00460668, Final residual = 5.11883e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237662, Final residual = 2.74328e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225292, Final residual = 2.63749e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0530749, Final residual = 0.00479284, No Iterations 10
time step continuity errors : sum local = 1.1739e-06, global = 2.90135e-19, cumulative = 1.8944e-17
nonePCG:  Solving for p, Initial residual = 0.00497185, Final residual = 8.9342e-07, No Iterations 146
time step continuity errors : sum local = 2.17808e-10, global = 5.12292e-19, cumulative = 1.94563e-17
ExecutionTime = 0.33 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0761228 max: 0.110174
Time = 6.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00460429, Final residual = 5.12911e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237518, Final residual = 2.69233e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0225883, Final residual = 2.66138e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0481432, Final residual = 0.00471798, No Iterations 9
time step continuity errors : sum local = 1.15665e-06, global = 2.84232e-20, cumulative = 1.94847e-17
nonePCG:  Solving for p, Initial residual = 0.00483813, Final residual = 9.56962e-07, No Iterations 138
time step continuity errors : sum local = 2.33983e-10, global = 4.81922e-20, cumulative = 1.95329e-17
ExecutionTime = 0.33 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0761043 max: 0.109691
Time = 6.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00460526, Final residual = 5.14361e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237553, Final residual = 2.6758e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226251, Final residual = 2.66789e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0528439, Final residual = 0.00505077, No Iterations 10
time step continuity errors : sum local = 1.23423e-06, global = 9.85311e-20, cumulative = 1.96315e-17
nonePCG:  Solving for p, Initial residual = 0.00522622, Final residual = 9.58588e-07, No Iterations 140
time step continuity errors : sum local = 2.30501e-10, global = 1.11537e-20, cumulative = 1.96426e-17
ExecutionTime = 0.34 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0760861 max: 0.109139
Time = 6.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00460946, Final residual = 5.17521e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237363, Final residual = 2.65715e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226569, Final residual = 2.66681e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0552327, Final residual = 0.00491514, No Iterations 9
time step continuity errors : sum local = 1.1912e-06, global = 3.24519e-20, cumulative = 1.96751e-17
nonePCG:  Solving for p, Initial residual = 0.00512363, Final residual = 7.15948e-07, No Iterations 135
time step continuity errors : sum local = 1.73005e-10, global = 8.76768e-20, cumulative = 1.97627e-17
ExecutionTime = 0.36 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0760679 max: 0.108521
Time = 6.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0046144, Final residual = 5.20455e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236728, Final residual = 2.6244e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226698, Final residual = 2.66492e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.053973, Final residual = 0.00531502, No Iterations 9
time step continuity errors : sum local = 1.28196e-06, global = 4.2034e-20, cumulative = 1.98048e-17
nonePCG:  Solving for p, Initial residual = 0.00544228, Final residual = 8.29529e-07, No Iterations 148
time step continuity errors : sum local = 2.00465e-10, global = -3.19358e-21, cumulative = 1.98016e-17
ExecutionTime = 0.36 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0760487 max: 0.107834
Time = 7

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00461738, Final residual = 5.22194e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236286, Final residual = 2.59371e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022652, Final residual = 2.66476e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.053471, Final residual = 0.00501965, No Iterations 9
time step continuity errors : sum local = 1.20854e-06, global = -1.34022e-19, cumulative = 1.96676e-17
nonePCG:  Solving for p, Initial residual = 0.00513762, Final residual = 9.66416e-07, No Iterations 145
time step continuity errors : sum local = 2.33152e-10, global = 1.53079e-19, cumulative = 1.98206e-17
ExecutionTime = 0.37 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.076031 max: 0.10708
Time = 7.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00462001, Final residual = 5.25807e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235902, Final residual = 2.57267e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022633, Final residual = 2.66856e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0538931, Final residual = 0.00516711, No Iterations 9
time step continuity errors : sum local = 1.24564e-06, global = 1.71471e-20, cumulative = 1.98378e-17
nonePCG:  Solving for p, Initial residual = 0.0053217, Final residual = 8.49168e-07, No Iterations 140
time step continuity errors : sum local = 2.004e-10, global = 1.70809e-19, cumulative = 2.00086e-17
ExecutionTime = 0.38 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0760106 max: 0.106262
Time = 7.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00462877, Final residual = 5.29564e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235565, Final residual = 2.57242e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226313, Final residual = 2.66451e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0524505, Final residual = 0.00498606, No Iterations 9
time step continuity errors : sum local = 1.20392e-06, global = 3.84119e-19, cumulative = 2.03927e-17
nonePCG:  Solving for p, Initial residual = 0.00512192, Final residual = 9.12228e-07, No Iterations 146
time step continuity errors : sum local = 2.2124e-10, global = 1.19956e-19, cumulative = 2.05127e-17
ExecutionTime = 0.4 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0759889 max: 0.105383
Time = 7.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00464054, Final residual = 5.32366e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235405, Final residual = 2.56812e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226427, Final residual = 2.67002e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0567037, Final residual = 0.00552837, No Iterations 10
time step continuity errors : sum local = 1.3331e-06, global = 2.00307e-19, cumulative = 2.0713e-17
nonePCG:  Solving for p, Initial residual = 0.00574586, Final residual = 9.3701e-07, No Iterations 146
time step continuity errors : sum local = 2.25603e-10, global = 1.84305e-19, cumulative = 2.08973e-17
ExecutionTime = 0.4 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0759658 max: 0.10444
Time = 7.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00464985, Final residual = 5.34715e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235798, Final residual = 2.57745e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0226972, Final residual = 2.6794e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0539775, Final residual = 0.00480391, No Iterations 10
time step continuity errors : sum local = 1.1585e-06, global = 4.12399e-19, cumulative = 2.13097e-17
nonePCG:  Solving for p, Initial residual = 0.00495776, Final residual = 8.96196e-07, No Iterations 146
time step continuity errors : sum local = 2.182e-10, global = 4.89766e-19, cumulative = 2.17995e-17
ExecutionTime = 0.41 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0759456 max: 0.10362
Time = 8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00465854, Final residual = 5.35745e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235469, Final residual = 2.57202e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0227666, Final residual = 2.68372e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0624798, Final residual = 0.00559145, No Iterations 10
time step continuity errors : sum local = 1.34594e-06, global = 3.43435e-19, cumulative = 2.21429e-17
nonePCG:  Solving for p, Initial residual = 0.00587539, Final residual = 8.59461e-07, No Iterations 148
time step continuity errors : sum local = 2.05776e-10, global = 6.5219e-19, cumulative = 2.27951e-17
ExecutionTime = 0.43 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0759262 max: 0.103789
Time = 8.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00467051, Final residual = 5.35927e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235413, Final residual = 2.56274e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0228283, Final residual = 2.69956e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0549198, Final residual = 0.00520018, No Iterations 10
time step continuity errors : sum local = 1.24007e-06, global = 4.37016e-19, cumulative = 2.32321e-17
nonePCG:  Solving for p, Initial residual = 0.00536878, Final residual = 9.91951e-07, No Iterations 135
time step continuity errors : sum local = 2.34939e-10, global = 4.98186e-19, cumulative = 2.37303e-17
ExecutionTime = 0.43 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0759107 max: 0.103897
Time = 8.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00467941, Final residual = 5.35846e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.023543, Final residual = 2.56601e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0228648, Final residual = 2.69823e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0596685, Final residual = 0.0058003, No Iterations 9
time step continuity errors : sum local = 1.37046e-06, global = 4.73375e-19, cumulative = 2.42037e-17
nonePCG:  Solving for p, Initial residual = 0.00594305, Final residual = 8.80829e-07, No Iterations 148
time step continuity errors : sum local = 2.07317e-10, global = 4.78648e-19, cumulative = 2.46823e-17
ExecutionTime = 0.44 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758965 max: 0.103928
Time = 8.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00468506, Final residual = 5.36565e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235168, Final residual = 2.56513e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0228627, Final residual = 2.69011e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0566034, Final residual = 0.00525534, No Iterations 9
time step continuity errors : sum local = 1.24558e-06, global = 5.84749e-19, cumulative = 2.52671e-17
nonePCG:  Solving for p, Initial residual = 0.00536246, Final residual = 9.40917e-07, No Iterations 145
time step continuity errors : sum local = 2.24814e-10, global = 6.02179e-19, cumulative = 2.58692e-17
ExecutionTime = 0.46 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758797 max: 0.103874
Time = 8.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00468898, Final residual = 5.36452e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235239, Final residual = 2.56746e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022874, Final residual = 2.68218e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.055594, Final residual = 0.00494152, No Iterations 9
time step continuity errors : sum local = 1.1899e-06, global = 6.76181e-19, cumulative = 2.65454e-17
nonePCG:  Solving for p, Initial residual = 0.00505419, Final residual = 9.91843e-07, No Iterations 148
time step continuity errors : sum local = 2.40369e-10, global = 5.19426e-19, cumulative = 2.70648e-17
ExecutionTime = 0.47 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758655 max: 0.103742
Time = 9

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00469294, Final residual = 5.35505e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234945, Final residual = 2.56547e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0228971, Final residual = 2.66533e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0607834, Final residual = 0.0058878, No Iterations 9
time step continuity errors : sum local = 1.4198e-06, global = 3.52186e-19, cumulative = 2.7417e-17
nonePCG:  Solving for p, Initial residual = 0.00607304, Final residual = 9.6885e-07, No Iterations 149
time step continuity errors : sum local = 2.31782e-10, global = 5.29838e-19, cumulative = 2.79469e-17
ExecutionTime = 0.47 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758544 max: 0.103526
Time = 9.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00469747, Final residual = 5.35405e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234631, Final residual = 2.57496e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229457, Final residual = 2.64793e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0609032, Final residual = 0.00591734, No Iterations 9
time step continuity errors : sum local = 1.40993e-06, global = 3.89963e-19, cumulative = 2.83368e-17
nonePCG:  Solving for p, Initial residual = 0.00612639, Final residual = 9.22679e-07, No Iterations 149
time step continuity errors : sum local = 2.20162e-10, global = 2.96094e-19, cumulative = 2.86329e-17
ExecutionTime = 0.49 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758451 max: 0.103239
Time = 9.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00470538, Final residual = 5.35166e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234083, Final residual = 2.56537e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229511, Final residual = 2.6359e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.056109, Final residual = 0.00525287, No Iterations 9
time step continuity errors : sum local = 1.24729e-06, global = 4.9112e-19, cumulative = 2.9124e-17
nonePCG:  Solving for p, Initial residual = 0.00539155, Final residual = 8.51681e-07, No Iterations 148
time step continuity errors : sum local = 2.01277e-10, global = 6.03233e-19, cumulative = 2.97273e-17
ExecutionTime = 0.5 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758346 max: 0.102863
Time = 9.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00471, Final residual = 5.33804e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0233216, Final residual = 2.55434e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.02297, Final residual = 2.61557e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0566506, Final residual = 0.0056115, No Iterations 9
time step continuity errors : sum local = 1.33015e-06, global = 6.56895e-19, cumulative = 3.03842e-17
nonePCG:  Solving for p, Initial residual = 0.00572847, Final residual = 8.86621e-07, No Iterations 146
time step continuity errors : sum local = 2.09616e-10, global = 6.86791e-19, cumulative = 3.1071e-17
ExecutionTime = 0.5 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758255 max: 0.103028
Time = 9.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00471127, Final residual = 5.31999e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0232646, Final residual = 2.56439e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229949, Final residual = 2.59484e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0566573, Final residual = 0.00532695, No Iterations 10
time step continuity errors : sum local = 1.2665e-06, global = 8.11129e-19, cumulative = 3.18821e-17
nonePCG:  Solving for p, Initial residual = 0.00554109, Final residual = 8.15523e-07, No Iterations 146
time step continuity errors : sum local = 1.92051e-10, global = 4.88988e-19, cumulative = 3.23711e-17
ExecutionTime = 0.52 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758154 max: 0.103167
Time = 10

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00471074, Final residual = 5.30282e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0232658, Final residual = 2.56192e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230285, Final residual = 2.57493e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0590047, Final residual = 0.00554243, No Iterations 9
time step continuity errors : sum local = 1.31288e-06, global = 5.32837e-19, cumulative = 3.29039e-17
nonePCG:  Solving for p, Initial residual = 0.00567644, Final residual = 9.53149e-07, No Iterations 149
time step continuity errors : sum local = 2.26151e-10, global = 6.17086e-19, cumulative = 3.3521e-17
ExecutionTime = 0.53 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.075811 max: 0.103307
Time = 10.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00471168, Final residual = 5.27639e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0232966, Final residual = 2.56601e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230371, Final residual = 2.54072e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0601866, Final residual = 0.00511829, No Iterations 9
time step continuity errors : sum local = 1.21095e-06, global = 5.31164e-19, cumulative = 3.40522e-17
nonePCG:  Solving for p, Initial residual = 0.00525439, Final residual = 9.84723e-07, No Iterations 145
time step continuity errors : sum local = 2.32746e-10, global = 4.76358e-19, cumulative = 3.45285e-17
ExecutionTime = 0.54 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758111 max: 0.103904
Time = 10.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00470874, Final residual = 5.26229e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234298, Final residual = 2.57572e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230223, Final residual = 2.50512e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0586598, Final residual = 0.0053787, No Iterations 9
time step continuity errors : sum local = 1.27262e-06, global = 7.06357e-19, cumulative = 3.52349e-17
nonePCG:  Solving for p, Initial residual = 0.00555639, Final residual = 8.63992e-07, No Iterations 148
time step continuity errors : sum local = 2.03558e-10, global = 5.15242e-19, cumulative = 3.57501e-17
ExecutionTime = 0.55 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758132 max: 0.10445
Time = 10.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00470907, Final residual = 5.24406e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235132, Final residual = 2.59113e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022987, Final residual = 2.47279e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0603455, Final residual = 0.00578103, No Iterations 10
time step continuity errors : sum local = 1.35248e-06, global = 5.09424e-19, cumulative = 3.62595e-17
nonePCG:  Solving for p, Initial residual = 0.00604173, Final residual = 8.24563e-07, No Iterations 148
time step continuity errors : sum local = 1.92104e-10, global = 4.82947e-19, cumulative = 3.67425e-17
ExecutionTime = 0.56 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758159 max: 0.10494
Time = 10.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00471176, Final residual = 5.22486e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235365, Final residual = 2.61323e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229659, Final residual = 2.45403e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0558198, Final residual = 0.00468779, No Iterations 9
time step continuity errors : sum local = 1.09275e-06, global = 5.07796e-19, cumulative = 3.72503e-17
nonePCG:  Solving for p, Initial residual = 0.00481511, Final residual = 8.36612e-07, No Iterations 135
time step continuity errors : sum local = 1.96982e-10, global = 5.65011e-19, cumulative = 3.78153e-17
ExecutionTime = 0.57 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758206 max: 0.105373
Time = 11

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00471595, Final residual = 5.20926e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235618, Final residual = 2.63089e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229478, Final residual = 2.43042e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0625493, Final residual = 0.00623577, No Iterations 9
time step continuity errors : sum local = 1.45501e-06, global = 5.47395e-19, cumulative = 3.83627e-17
nonePCG:  Solving for p, Initial residual = 0.00647152, Final residual = 9.6815e-07, No Iterations 149
time step continuity errors : sum local = 2.25225e-10, global = 6.40814e-19, cumulative = 3.90035e-17
ExecutionTime = 0.58 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758263 max: 0.10575
Time = 11.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00471883, Final residual = 5.19539e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236113, Final residual = 2.63254e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229252, Final residual = 2.41858e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0545344, Final residual = 0.00519914, No Iterations 9
time step continuity errors : sum local = 1.21075e-06, global = 4.12246e-19, cumulative = 3.94158e-17
nonePCG:  Solving for p, Initial residual = 0.00535488, Final residual = 9.73357e-07, No Iterations 150
time step continuity errors : sum local = 2.26188e-10, global = 6.13279e-19, cumulative = 4.0029e-17
ExecutionTime = 0.59 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758329 max: 0.106069
Time = 11.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00472715, Final residual = 5.20386e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236142, Final residual = 2.64471e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229206, Final residual = 2.40724e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0556664, Final residual = 0.00543001, No Iterations 9
time step continuity errors : sum local = 1.25644e-06, global = 5.71821e-19, cumulative = 4.06009e-17
nonePCG:  Solving for p, Initial residual = 0.00556391, Final residual = 7.60718e-07, No Iterations 149
time step continuity errors : sum local = 1.75682e-10, global = 6.36398e-19, cumulative = 4.12373e-17
ExecutionTime = 0.6 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758389 max: 0.106334
Time = 11.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00473393, Final residual = 5.21768e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235791, Final residual = 2.65482e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0229794, Final residual = 2.40513e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0546005, Final residual = 0.00534108, No Iterations 9
time step continuity errors : sum local = 1.23493e-06, global = 6.7197e-19, cumulative = 4.19092e-17
nonePCG:  Solving for p, Initial residual = 0.00549939, Final residual = 9.56624e-07, No Iterations 142
time step continuity errors : sum local = 2.21747e-10, global = 7.41384e-19, cumulative = 4.26506e-17
ExecutionTime = 0.61 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758482 max: 0.106537
Time = 11.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00474445, Final residual = 5.22437e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235784, Final residual = 2.6621e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230213, Final residual = 2.4129e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0610833, Final residual = 0.00585212, No Iterations 9
time step continuity errors : sum local = 1.35416e-06, global = 6.50786e-19, cumulative = 4.33014e-17
nonePCG:  Solving for p, Initial residual = 0.00603879, Final residual = 9.38196e-07, No Iterations 145
time step continuity errors : sum local = 2.16064e-10, global = 4.56109e-19, cumulative = 4.37575e-17
ExecutionTime = 0.62 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758569 max: 0.106638
Time = 12

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00475063, Final residual = 5.22142e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.023539, Final residual = 2.67438e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0231144, Final residual = 2.41815e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0576927, Final residual = 0.00521214, No Iterations 10
time step continuity errors : sum local = 1.2003e-06, global = 5.19197e-19, cumulative = 4.42767e-17
nonePCG:  Solving for p, Initial residual = 0.00539555, Final residual = 9.70838e-07, No Iterations 145
time step continuity errors : sum local = 2.21956e-10, global = 5.38704e-19, cumulative = 4.48154e-17
ExecutionTime = 0.63 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758665 max: 0.10666
Time = 12.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0047568, Final residual = 5.21972e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234981, Final residual = 2.68048e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.023192, Final residual = 2.41236e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0567092, Final residual = 0.00513913, No Iterations 10
time step continuity errors : sum local = 1.17987e-06, global = 6.71189e-19, cumulative = 4.54866e-17
nonePCG:  Solving for p, Initial residual = 0.0053886, Final residual = 9.64453e-07, No Iterations 145
time step continuity errors : sum local = 2.19244e-10, global = 5.60396e-19, cumulative = 4.6047e-17
ExecutionTime = 0.65 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758728 max: 0.106615
Time = 12.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00476212, Final residual = 5.22424e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.023466, Final residual = 2.68577e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232108, Final residual = 2.40711e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0526512, Final residual = 0.00510299, No Iterations 9
time step continuity errors : sum local = 1.15839e-06, global = 7.81245e-19, cumulative = 4.68282e-17
nonePCG:  Solving for p, Initial residual = 0.00520372, Final residual = 7.83931e-07, No Iterations 135
time step continuity errors : sum local = 1.78611e-10, global = 4.71914e-19, cumulative = 4.73001e-17
ExecutionTime = 0.65 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758743 max: 0.106499
Time = 12.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00476986, Final residual = 5.24202e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234401, Final residual = 2.69097e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232514, Final residual = 2.40372e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0533227, Final residual = 0.00531046, No Iterations 9
time step continuity errors : sum local = 1.20228e-06, global = 5.07373e-19, cumulative = 4.78075e-17
nonePCG:  Solving for p, Initial residual = 0.00548452, Final residual = 8.31891e-07, No Iterations 149
time step continuity errors : sum local = 1.87543e-10, global = 5.36161e-19, cumulative = 4.83437e-17
ExecutionTime = 0.66 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758727 max: 0.106308
Time = 12.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0047801, Final residual = 5.2528e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234504, Final residual = 2.70367e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232824, Final residual = 2.40161e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0515749, Final residual = 0.00470139, No Iterations 9
time step continuity errors : sum local = 1.05606e-06, global = 7.11285e-19, cumulative = 4.9055e-17
nonePCG:  Solving for p, Initial residual = 0.00483784, Final residual = 9.93782e-07, No Iterations 148
time step continuity errors : sum local = 2.22948e-10, global = 7.45541e-19, cumulative = 4.98005e-17
ExecutionTime = 0.68 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.075869 max: 0.106033
Time = 13

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00479016, Final residual = 5.25594e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235325, Final residual = 2.71337e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232583, Final residual = 2.39581e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0542382, Final residual = 0.00536146, No Iterations 9
time step continuity errors : sum local = 1.21151e-06, global = 6.72317e-19, cumulative = 5.04728e-17
nonePCG:  Solving for p, Initial residual = 0.00547959, Final residual = 8.89685e-07, No Iterations 139
time step continuity errors : sum local = 2.01964e-10, global = 7.63627e-19, cumulative = 5.12365e-17
ExecutionTime = 0.68 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758624 max: 0.105656
Time = 13.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00479424, Final residual = 5.24915e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235486, Final residual = 2.71854e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.023274, Final residual = 2.39631e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0544018, Final residual = 0.00528717, No Iterations 10
time step continuity errors : sum local = 1.20005e-06, global = 9.92966e-19, cumulative = 5.22294e-17
nonePCG:  Solving for p, Initial residual = 0.00545366, Final residual = 9.68754e-07, No Iterations 147
time step continuity errors : sum local = 2.1891e-10, global = 8.04949e-19, cumulative = 5.30344e-17
ExecutionTime = 0.69 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758555 max: 0.105262
Time = 13.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00479399, Final residual = 5.22333e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235344, Final residual = 2.71617e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232548, Final residual = 2.39789e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0538512, Final residual = 0.0043576, No Iterations 13
time step continuity errors : sum local = 9.82775e-07, global = 8.91068e-19, cumulative = 5.39254e-17
nonePCG:  Solving for p, Initial residual = 0.00458198, Final residual = 8.53798e-07, No Iterations 146
time step continuity errors : sum local = 1.92173e-10, global = 9.76207e-19, cumulative = 5.49016e-17
ExecutionTime = 0.71 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758445 max: 0.104804
Time = 13.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00478681, Final residual = 5.19113e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235424, Final residual = 2.72731e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232517, Final residual = 2.39373e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.055173, Final residual = 0.00480931, No Iterations 9
time step continuity errors : sum local = 1.0884e-06, global = 9.96606e-19, cumulative = 5.58982e-17
nonePCG:  Solving for p, Initial residual = 0.00498151, Final residual = 9.37026e-07, No Iterations 148
time step continuity errors : sum local = 2.11552e-10, global = 1.13845e-18, cumulative = 5.70367e-17
ExecutionTime = 0.71 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758331 max: 0.104269
Time = 13.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477908, Final residual = 5.15418e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235907, Final residual = 2.7439e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232382, Final residual = 2.3933e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0554555, Final residual = 0.00525726, No Iterations 9
time step continuity errors : sum local = 1.19186e-06, global = 9.24547e-19, cumulative = 5.79612e-17
nonePCG:  Solving for p, Initial residual = 0.00539354, Final residual = 8.62345e-07, No Iterations 148
time step continuity errors : sum local = 1.94944e-10, global = 1.03479e-18, cumulative = 5.8996e-17
ExecutionTime = 0.72 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0758189 max: 0.103656
Time = 14

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477626, Final residual = 5.11959e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236316, Final residual = 2.74975e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232287, Final residual = 2.39425e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0532982, Final residual = 0.00529399, No Iterations 9
time step continuity errors : sum local = 1.20897e-06, global = 1.03755e-18, cumulative = 6.00336e-17
nonePCG:  Solving for p, Initial residual = 0.00539741, Final residual = 7.56896e-07, No Iterations 149
time step continuity errors : sum local = 1.73103e-10, global = 1.00894e-18, cumulative = 6.10425e-17
ExecutionTime = 0.73 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.075805 max: 0.104112
Time = 14.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477056, Final residual = 5.09915e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236566, Final residual = 2.74853e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232465, Final residual = 2.39383e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0594989, Final residual = 0.0055475, No Iterations 11
time step continuity errors : sum local = 1.27032e-06, global = 8.88241e-19, cumulative = 6.19308e-17
nonePCG:  Solving for p, Initial residual = 0.00577975, Final residual = 7.72925e-07, No Iterations 148
time step continuity errors : sum local = 1.76996e-10, global = 9.28353e-19, cumulative = 6.28591e-17
ExecutionTime = 0.74 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757893 max: 0.104665
Time = 14.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00476481, Final residual = 5.07789e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236659, Final residual = 2.7428e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232203, Final residual = 2.40491e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0534934, Final residual = 0.00523102, No Iterations 9
time step continuity errors : sum local = 1.19904e-06, global = 9.45712e-19, cumulative = 6.38048e-17
nonePCG:  Solving for p, Initial residual = 0.00536286, Final residual = 9.42956e-07, No Iterations 146
time step continuity errors : sum local = 2.16031e-10, global = 8.19119e-19, cumulative = 6.4624e-17
ExecutionTime = 0.75 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757749 max: 0.105136
Time = 14.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0047678, Final residual = 5.05735e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236288, Final residual = 2.72627e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0231736, Final residual = 2.4222e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0537901, Final residual = 0.00482064, No Iterations 9
time step continuity errors : sum local = 1.10229e-06, global = 7.52218e-19, cumulative = 6.53762e-17
nonePCG:  Solving for p, Initial residual = 0.00496323, Final residual = 8.66164e-07, No Iterations 148
time step continuity errors : sum local = 1.97517e-10, global = 8.74823e-19, cumulative = 6.6251e-17
ExecutionTime = 0.77 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757644 max: 0.10553
Time = 14.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0047717, Final residual = 5.04057e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235773, Final residual = 2.71621e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.023116, Final residual = 2.43521e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0524797, Final residual = 0.00476238, No Iterations 10
time step continuity errors : sum local = 1.08568e-06, global = 8.32803e-19, cumulative = 6.70838e-17
nonePCG:  Solving for p, Initial residual = 0.00495788, Final residual = 9.16587e-07, No Iterations 146
time step continuity errors : sum local = 2.07027e-10, global = 7.0732e-19, cumulative = 6.77911e-17
ExecutionTime = 0.78 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757555 max: 0.105853
Time = 15

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477612, Final residual = 5.03689e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235717, Final residual = 2.71782e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230919, Final residual = 2.44141e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0562786, Final residual = 0.00549537, No Iterations 9
time step continuity errors : sum local = 1.2467e-06, global = 8.30982e-19, cumulative = 6.86221e-17
nonePCG:  Solving for p, Initial residual = 0.00562084, Final residual = 8.92058e-07, No Iterations 149
time step continuity errors : sum local = 2.02029e-10, global = 9.95942e-19, cumulative = 6.9618e-17
ExecutionTime = 0.78 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757418 max: 0.106103
Time = 15.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477373, Final residual = 5.02135e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235866, Final residual = 2.72268e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230763, Final residual = 2.4571e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0506352, Final residual = 0.00488726, No Iterations 9
time step continuity errors : sum local = 1.11135e-06, global = 9.51673e-19, cumulative = 7.05697e-17
nonePCG:  Solving for p, Initial residual = 0.00496751, Final residual = 9.04717e-07, No Iterations 146
time step continuity errors : sum local = 2.08295e-10, global = 7.13274e-19, cumulative = 7.1283e-17
ExecutionTime = 0.79 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757333 max: 0.106268
Time = 15.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477105, Final residual = 5.00755e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235853, Final residual = 2.72888e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230266, Final residual = 2.47363e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0636358, Final residual = 0.00532885, No Iterations 10
time step continuity errors : sum local = 1.22506e-06, global = 1.12334e-18, cumulative = 7.24063e-17
nonePCG:  Solving for p, Initial residual = 0.00558902, Final residual = 9.24186e-07, No Iterations 148
time step continuity errors : sum local = 2.11805e-10, global = 7.77136e-19, cumulative = 7.31835e-17
ExecutionTime = 0.81 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757301 max: 0.106349
Time = 15.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477, Final residual = 4.98658e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235562, Final residual = 2.7279e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.023004, Final residual = 2.48268e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0546738, Final residual = 0.00507466, No Iterations 10
time step continuity errors : sum local = 1.1683e-06, global = 7.06725e-19, cumulative = 7.38902e-17
nonePCG:  Solving for p, Initial residual = 0.00522295, Final residual = 9.78615e-07, No Iterations 139
time step continuity errors : sum local = 2.26331e-10, global = 8.95778e-19, cumulative = 7.4786e-17
ExecutionTime = 0.81 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757366 max: 0.106348
Time = 15.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477615, Final residual = 4.98103e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235726, Final residual = 2.72331e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022946, Final residual = 2.49505e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0609218, Final residual = 0.00557227, No Iterations 10
time step continuity errors : sum local = 1.27773e-06, global = 1.05134e-18, cumulative = 7.58373e-17
nonePCG:  Solving for p, Initial residual = 0.00584154, Final residual = 9.30314e-07, No Iterations 149
time step continuity errors : sum local = 2.11325e-10, global = 8.989e-19, cumulative = 7.67362e-17
ExecutionTime = 0.83 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757422 max: 0.106271
Time = 16

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477387, Final residual = 4.97512e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234971, Final residual = 2.70951e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.022965, Final residual = 2.504e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0518637, Final residual = 0.0051047, No Iterations 9
time step continuity errors : sum local = 1.16929e-06, global = 9.01203e-19, cumulative = 7.76374e-17
nonePCG:  Solving for p, Initial residual = 0.0051698, Final residual = 8.89361e-07, No Iterations 139
time step continuity errors : sum local = 2.04363e-10, global = 1.10622e-18, cumulative = 7.87436e-17
ExecutionTime = 0.84 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757461 max: 0.106122
Time = 16.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477393, Final residual = 4.97292e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234388, Final residual = 2.70099e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230122, Final residual = 2.51318e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0524613, Final residual = 0.00497889, No Iterations 9
time step continuity errors : sum local = 1.15104e-06, global = 7.78815e-19, cumulative = 7.95224e-17
nonePCG:  Solving for p, Initial residual = 0.00507781, Final residual = 9.98037e-07, No Iterations 148
time step continuity errors : sum local = 2.28342e-10, global = 1.01371e-18, cumulative = 8.05362e-17
ExecutionTime = 0.86 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757464 max: 0.105912
Time = 16.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477392, Final residual = 4.96664e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234083, Final residual = 2.6967e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230423, Final residual = 2.52067e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0564381, Final residual = 0.00534514, No Iterations 9
time step continuity errors : sum local = 1.22353e-06, global = 1.0349e-18, cumulative = 8.1571e-17
nonePCG:  Solving for p, Initial residual = 0.00544996, Final residual = 9.49607e-07, No Iterations 149
time step continuity errors : sum local = 2.17767e-10, global = 9.93447e-19, cumulative = 8.25645e-17
ExecutionTime = 0.86 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757459 max: 0.105655
Time = 16.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477674, Final residual = 4.96698e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0233802, Final residual = 2.69934e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0231096, Final residual = 2.53536e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0574248, Final residual = 0.00539633, No Iterations 9
time step continuity errors : sum local = 1.23218e-06, global = 1.05846e-18, cumulative = 8.3623e-17
nonePCG:  Solving for p, Initial residual = 0.00556741, Final residual = 8.83546e-07, No Iterations 139
time step continuity errors : sum local = 1.99532e-10, global = 8.45678e-19, cumulative = 8.44686e-17
ExecutionTime = 0.87 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757419 max: 0.105859
Time = 16.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477523, Final residual = 4.95992e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234251, Final residual = 2.69967e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0231703, Final residual = 2.54229e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0557636, Final residual = 0.00540492, No Iterations 9
time step continuity errors : sum local = 1.22746e-06, global = 9.07617e-19, cumulative = 8.53763e-17
nonePCG:  Solving for p, Initial residual = 0.0055614, Final residual = 9.81803e-07, No Iterations 149
time step continuity errors : sum local = 2.22241e-10, global = 1.0389e-18, cumulative = 8.64152e-17
ExecutionTime = 0.89 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757384 max: 0.106267
Time = 17

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477136, Final residual = 4.95426e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.023506, Final residual = 2.70866e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232063, Final residual = 2.5396e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0575404, Final residual = 0.00547464, No Iterations 11
time step continuity errors : sum local = 1.23683e-06, global = 1.07312e-18, cumulative = 8.74883e-17
nonePCG:  Solving for p, Initial residual = 0.0056785, Final residual = 9.00215e-07, No Iterations 148
time step continuity errors : sum local = 2.03785e-10, global = 9.12049e-19, cumulative = 8.84003e-17
ExecutionTime = 0.89 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757353 max: 0.106607
Time = 17.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00477565, Final residual = 4.95947e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.023522, Final residual = 2.72664e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232419, Final residual = 2.53746e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0590526, Final residual = 0.0051454, No Iterations 9
time step continuity errors : sum local = 1.16364e-06, global = 1.32283e-18, cumulative = 8.97232e-17
nonePCG:  Solving for p, Initial residual = 0.00530094, Final residual = 9.27234e-07, No Iterations 148
time step continuity errors : sum local = 2.10448e-10, global = 1.36496e-18, cumulative = 9.10881e-17
ExecutionTime = 0.9 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757336 max: 0.106875
Time = 17.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0047798, Final residual = 4.96373e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235536, Final residual = 2.74197e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232531, Final residual = 2.53425e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0577842, Final residual = 0.00553856, No Iterations 9
time step continuity errors : sum local = 1.24122e-06, global = 1.46951e-18, cumulative = 9.25576e-17
nonePCG:  Solving for p, Initial residual = 0.0057629, Final residual = 9.99126e-07, No Iterations 148
time step continuity errors : sum local = 2.21798e-10, global = 1.3381e-18, cumulative = 9.38957e-17
ExecutionTime = 0.92 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.075731 max: 0.107067
Time = 17.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00478059, Final residual = 4.96403e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236219, Final residual = 2.75701e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232529, Final residual = 2.53316e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.052715, Final residual = 0.00525199, No Iterations 9
time step continuity errors : sum local = 1.16538e-06, global = 1.25284e-18, cumulative = 9.51486e-17
nonePCG:  Solving for p, Initial residual = 0.00535813, Final residual = 7.82751e-07, No Iterations 149
time step continuity errors : sum local = 1.73978e-10, global = 1.40235e-18, cumulative = 9.65509e-17
ExecutionTime = 0.93 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757259 max: 0.107185
Time = 17.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00478994, Final residual = 4.97249e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236139, Final residual = 2.75587e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232406, Final residual = 2.53039e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0541682, Final residual = 0.00534728, No Iterations 9
time step continuity errors : sum local = 1.18785e-06, global = 1.31775e-18, cumulative = 9.78687e-17
nonePCG:  Solving for p, Initial residual = 0.00546738, Final residual = 9.31523e-07, No Iterations 149
time step continuity errors : sum local = 2.07838e-10, global = 1.19906e-18, cumulative = 9.90677e-17
ExecutionTime = 0.93 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757193 max: 0.107228
Time = 18

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00479573, Final residual = 4.96535e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236264, Final residual = 2.75784e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232314, Final residual = 2.53045e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0542756, Final residual = 0.00533926, No Iterations 9
time step continuity errors : sum local = 1.19288e-06, global = 1.32659e-18, cumulative = 1.00394e-16
nonePCG:  Solving for p, Initial residual = 0.00545747, Final residual = 9.54578e-07, No Iterations 149
time step continuity errors : sum local = 2.13608e-10, global = 1.26768e-18, cumulative = 1.01662e-16
ExecutionTime = 0.95 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757137 max: 0.107199
Time = 18.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00480757, Final residual = 4.9653e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236641, Final residual = 2.76172e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0232062, Final residual = 2.52069e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0584832, Final residual = 0.00582241, No Iterations 9
time step continuity errors : sum local = 1.30353e-06, global = 1.29985e-18, cumulative = 1.02962e-16
nonePCG:  Solving for p, Initial residual = 0.00598842, Final residual = 9.10366e-07, No Iterations 148
time step continuity errors : sum local = 2.03999e-10, global = 1.09162e-18, cumulative = 1.04053e-16
ExecutionTime = 0.96 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0757075 max: 0.107094
Time = 18.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00481731, Final residual = 4.97628e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237504, Final residual = 2.7768e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0231675, Final residual = 2.5073e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0565305, Final residual = 0.00545501, No Iterations 10
time step continuity errors : sum local = 1.21816e-06, global = 1.23144e-18, cumulative = 1.05285e-16
nonePCG:  Solving for p, Initial residual = 0.00565698, Final residual = 8.94617e-07, No Iterations 148
time step continuity errors : sum local = 1.99318e-10, global = 1.44903e-18, cumulative = 1.06734e-16
ExecutionTime = 0.96 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.075702 max: 0.106923
Time = 18.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00482845, Final residual = 4.98658e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0238069, Final residual = 2.7833e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.023146, Final residual = 2.51697e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0536457, Final residual = 0.00484721, No Iterations 9
time step continuity errors : sum local = 1.07929e-06, global = 1.49024e-18, cumulative = 1.08224e-16
nonePCG:  Solving for p, Initial residual = 0.00500718, Final residual = 9.88549e-07, No Iterations 146
time step continuity errors : sum local = 2.20278e-10, global = 1.56455e-18, cumulative = 1.09789e-16
ExecutionTime = 0.98 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0756938 max: 0.106685
Time = 18.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00483788, Final residual = 4.98286e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0238056, Final residual = 2.79859e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0231282, Final residual = 2.52193e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0524208, Final residual = 0.00476434, No Iterations 10
time step continuity errors : sum local = 1.06694e-06, global = 1.48673e-18, cumulative = 1.11275e-16
nonePCG:  Solving for p, Initial residual = 0.00488575, Final residual = 8.26099e-07, No Iterations 146
time step continuity errors : sum local = 1.86981e-10, global = 1.38385e-18, cumulative = 1.12659e-16
ExecutionTime = 0.99 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0756814 max: 0.106381
Time = 19

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484416, Final residual = 4.96874e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0238582, Final residual = 2.83476e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230878, Final residual = 2.52423e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0553459, Final residual = 0.00552518, No Iterations 9
time step continuity errors : sum local = 1.25733e-06, global = 1.25496e-18, cumulative = 1.13914e-16
nonePCG:  Solving for p, Initial residual = 0.00559801, Final residual = 9.65717e-07, No Iterations 137
time step continuity errors : sum local = 2.21132e-10, global = 1.23404e-18, cumulative = 1.15148e-16
ExecutionTime = 0.99 s  ClockTime = 1 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0756716 max: 0.106176
Time = 19.2

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484657, Final residual = 4.95212e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0238343, Final residual = 2.84388e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230289, Final residual = 2.53209e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0596763, Final residual = 0.00571869, No Iterations 10
time step continuity errors : sum local = 1.31071e-06, global = 1.18374e-18, cumulative = 1.16332e-16
nonePCG:  Solving for p, Initial residual = 0.00596056, Final residual = 8.52544e-07, No Iterations 148
time step continuity errors : sum local = 1.94683e-10, global = 1.37599e-18, cumulative = 1.17708e-16
ExecutionTime = 1.01 s  ClockTime = 2 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0756615 max: 0.106435
Time = 19.4

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484356, Final residual = 4.92818e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0237489, Final residual = 2.85153e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230448, Final residual = 2.55124e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0529436, Final residual = 0.00511785, No Iterations 9
time step continuity errors : sum local = 1.17098e-06, global = 1.14863e-18, cumulative = 1.18857e-16
nonePCG:  Solving for p, Initial residual = 0.00524666, Final residual = 9.50185e-07, No Iterations 136
time step continuity errors : sum local = 2.17603e-10, global = 1.13469e-18, cumulative = 1.19991e-16
ExecutionTime = 1.02 s  ClockTime = 2 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0756532 max: 0.106614
Time = 19.6

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484518, Final residual = 4.90492e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0236771, Final residual = 2.87356e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.02303, Final residual = 2.56629e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0535895, Final residual = 0.00523159, No Iterations 9
time step continuity errors : sum local = 1.21269e-06, global = 1.31611e-18, cumulative = 1.21307e-16
nonePCG:  Solving for p, Initial residual = 0.00533832, Final residual = 8.25686e-07, No Iterations 149
time step continuity errors : sum local = 1.90802e-10, global = 1.16625e-18, cumulative = 1.22474e-16
ExecutionTime = 1.04 s  ClockTime = 2 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0756439 max: 0.106713
Time = 19.8

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.0048488, Final residual = 4.89018e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0235963, Final residual = 2.89808e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230199, Final residual = 2.57601e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0596912, Final residual = 0.00535372, No Iterations 9
time step continuity errors : sum local = 1.24653e-06, global = 9.30614e-19, cumulative = 1.23404e-16
nonePCG:  Solving for p, Initial residual = 0.00552749, Final residual = 8.77802e-07, No Iterations 149
time step continuity errors : sum local = 2.05781e-10, global = 9.19636e-19, cumulative = 1.24324e-16
ExecutionTime = 1.04 s  ClockTime = 2 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

Courant Number mean: 0.0756377 max: 0.106734
Time = 20

PIMPLE: iteration 1
smoothSolver:  Solving for Ux, Initial residual = 0.00484754, Final residual = 4.87714e-07, No Iterations 2
smoothSolver:  Solving for Uy, Initial residual = 0.0234891, Final residual = 2.9262e-06, No Iterations 2
smoothSolver:  Solving for Uz, Initial residual = 0.0230027, Final residual = 2.57245e-06, No Iterations 2
nonePCG:  Solving for p, Initial residual = 0.0628781, Final residual = 0.00590879, No Iterations 9
time step continuity errors : sum local = 1.37969e-06, global = 9.72129e-19, cumulative = 1.25296e-16
nonePCG:  Solving for p, Initial residual = 0.0060665, Final residual = 7.59284e-07, No Iterations 149
time step continuity errors : sum local = 1.77299e-10, global = 1.04468e-18, cumulative = 1.26341e-16
ExecutionTime = 1.05 s  ClockTime = 2 s

fieldAverage fieldAverage1 write:
    Calculating averages

    Writing average fields

End

Finalising parallel run
"""


def test_logParser():
    log_keys = [LogKey("Solving for p", ["InitialResidual", "FinalResidual", "Iter"])]
    log_parser = LogFile(keys=log_keys)

    records = log_parser.parse_to_records(log_str)
    expected_record = {
        "FinalResidual": 0.0920767,
        "InitialResidual": 0.933003,
        "Iter": 10.0,
        "Time": 0.2,
    }
    assert records[0] == expected_record
