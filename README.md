# License Compliance Verifier (LCV) and Compatibility Matrix (CM)

This is the Python version of the License Compliance Verifier (LCV).

LCV's task is to establish if all the inbound licenses are compatible with the outbound or not, including a few exceptional cases that will be matched depending on the use case (DUC).

To perform the assessment, it will check the Compatibility Matrix (CM) to retrieve compatibilities rules. 

LCV offers endpoints APIs to provide flag or verbose assessments.

The LCV compatibility flag output can be `True` or `false` or `DUC`.
E.g., Source code released under Apache 2.0 license can be used within a project released under the GPL3.0 license, but not vice-versa.

## How does the interaction between LCV and Compatibility Matrix functions :

The CM is represented in the [`licenses.csv`](https://github.com/fasten-project/LCV-CM/blob/develop/csv/licenses_tests.csv) file.
The rows represent `inbound` licenses and the columns `outbound` licenses.

The `LCV` will match all the inbound license array elements against the outbound one and check the rules.

It generates an array containing these associations and interprets in this way:
 - `True` if all the elements are true.
 - `False` if only one element contained is false (it does not matter what the other elements of the array are).
 - `DUC` if there are at least one `DUC` element and the rest is `True`.

The [`licenses.csv`](https://github.com/fasten-project/LCV-CM/blob/develop/csv/licenses_tests.csv) represents *True* with *1* and *False* with *0* because originally this Matrix was thought to be imported as a Postgres table, that makes use of bit data type to represent them.

# Integration with FASTEN 

We are currently working on the integration within the FASTEN REST APIs.

# Endpoints description
Coming soon.

# Running it with Docker locally :
LCVServer.py implements the APIs to interact with the LCV algorithm that is performing License Compliance assessments.
While using Main.py and Tests.py, the LCV algorithm is collecting a single instance of each inbound license found in a given JSON (so far is accepting the QMSTR JSON Output and can be easily adapted to the Scancode JSON Output), the APIs require to insert a list of inbound licenses. The outbound license is declared for a given project.
Given these two inputs, the LCV algorithm can perform the verification.
To build the APIs, build the docker image locally:
```
docker build -f DockerfileExternal -t lcv-cm .
```
or
```
docker build -f DockerfileExternal --no-cache -t lcv-cm .
```
To avoid Docker build from using cache.

The dockerfile clones this repository, so if it is required to update the docker image with code added recently, `--no-cache` would be the right option to apply the changes.

Running it:
```
docker run -it -p 3251:3251 lcv-cm
```
The LCVServer will run at the 3251 port of your localhost and be reachable via `http://0.0.0.0:3251/APIEndpoints`.
