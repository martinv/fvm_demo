# Finite Volume Demo

This is a simple implementation of a cell-centered finite volume method in two dimensions,.

## Governing Law

We are interested in solving governing equations for ideal compressible and inviscid fluid, known also as Euler equations:

![equation](pics/Euler_01.svg)

where $\rho$ is density, $\boldsymbol{v} = (v_1, v_2)$ velocity field and $e$ is internal gas energy. Pressure $p$ is defined
by the equation of state for ideal gas as

![equation](pics/state_eqn_01.svg)

where $\gamma$ is the ratio of specific heats $\gamma = \frac{c_p}{c_v} = 1.4$ for ideal gas.

In order to discretize the system with finite volumes, we rewrite the equations in conservation form

![equation](pics/conservation_law.svg)

which can be written in conservative variables $\boldsymbol{w} = (w_1, w_2, w_3, w_4)^T$, where $w_1 = \rho$, $w_2 = \rho v_1$, $w_3 = \rho v_2$, $w_4 = e$.

Euler equations in conservative form now read

![equation](pics/Euler_02.svg)

The constitutive law for ideal gas rewritten in conservative variables becomes

![equation](pics/state_eqn_02.svg)

## Discretization
The unkown $\boldsymbol{w}$ is from now on discrete and located in cell centers. After discretization of space derivatives, the time-change of
$\boldsymbol{w}$ in the mesh cell/element with index $i$ is given by

![equation](pics/discretization.svg)

with the following notation:

- $|C_i|$ is the surface/area of element $i$ in the mesh
- $N(i)$ denotes the set of all indices of neighbours of element $i$, i.e. all elements $j$ that share an edge with element $i$
- $n_{ij}$ is an oriented edge normal perpendicular to edge between elements $i$ and $j$ and pointing from element $i$ towards element $j$
- $l_{ij}$ is the length of edge separating elements $i$ and $j$
- $\mathbf{H}$ is the numerical flux function. The implementation uses [AUSM flux splitting scheme](https://ntrs.nasa.gov/api/citations/19940032139/downloads/19940032139.pdf)

For time discretization, an explicit Euler method was used. The discretization is only first-order accurate in time and space.

## Implementation and Numerical Test
The numerical test runs a [2D Riemann problem](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=f65f14aa0c0885c47ac06437505125ea1b5832b5) configuration number 3:

![Riemann setup](/pics/Riemann_setup.png)

The initial condition in this configuration is


| Quadrant |   $\rho$   |   $v_1$   |    $v_2$   |    $p$    |
| -------- | ---------- | --------- | ---------- | --------- |
|    1     |     1.5    |    0.0    |    0.0     |    1.5    |
|    2     |  0.5322581 | 1.2060454 |    0.0     |    0.3    |
|    3     |  0.1379928 | 1.2060454 | 1.2060454  | 0.0290323 |
|    4     |  0.5322581 |    0.0    | 1.2060454  |    0.3    |

The obtained solution at time $T = 0.3$ on a Cartesian mesh with $200 \times 200$ cells:

![Riemann solution](/pics/Riemann_density_small.png)
