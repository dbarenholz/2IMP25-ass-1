# 2IMP25-ass-1
This is the github repository for the first assignment of the 2IMP25 course as taught by Eindhoven University of Technology. The name of the course is "Software Evolution".
The name of the first assignment is **Requirements Traceability**.  

## Requirements Traceability
One of the main topics related to evolution of software requirements is traceability of requirements. In this assignment we focus on linking high-level requirements to low-level requirements. The code in this repository implements a simple trace-link detection tool and evaluates it on a publicly available [dataset](#dataset). We have implemented a total of 4 trace-link generation methods that can be found in the code in method `get_linked_requirements()` of file `helpers.py`.


## Building and Running
All code is packaged in a Docker container, and can be run using following terminal command:

1. Build the docker container: `docker build -t 2imp25-assignment-1 ./`.
2. Run the container: `docker run --rm -v "$pwd\dataset-1:/input" -v "$pwd\output:/output" 2imp25-assignment-1 1`. (Powershell -- Linux users should use comparable command)

*If you get errors for the first command, check that Docker Desktop (Windows) is running. If the second command gives output similar to below, then you failed to accept sharing the correct drive / folder.*

```raw
C:\Program Files\Docker\Docker\resources\bin\docker.exe: Error response from daemon: status code not OK but 500: {"Message":"Unhandled exception: Drive has not been shared"}.
See 'C:\Program Files\Docker\Docker\resources\bin\docker.exe run --help'.
```

## Dataset
The dataset used is the Waterloo dataset. This dataset describes different variants of the same system; an IP-telephony service. The high-level requirements are described in the form of Functional Requirements and the low-level requirements in the form of Use-Case descriptions. Only 2 of the 24 different variants of this dataset are considered for evaluation for now.