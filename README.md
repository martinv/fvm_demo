# Finite Volume Demo

This is a simple implementation of a cell-centered finite volume method in two dimensions,.

## Governing Law

We are interested in solving governing equations for ideal compressible and inviscid fluid, known also as Euler equations:
$$
\frac{\partial}{\partial t}\left(\begin{array}{c}\rho\\\rho v_1\\ \rho v_2\\ e\end{array}\right) + 
\frac{\partial}{\partial x}\left(\begin{array}{c}\rho v_1\\ \rho v_1^2 + p\\ \rho v_1 v_2\\ (e+p)v_1\end{array}\right) + 
\frac{\partial}{\partial y}\left(\begin{array}{c}\rho v_2\\ \rho v_1v_2\\  \rho v_2^2 + p\\ (e+p)v_2\end{array}\right) = \boldsymbol{0}
$$
where $\rho$ is density, $\boldsymbol{v} = (v_1, v_2)$ velocity field and $e$ is internal gas energy. Pressure $p$ is defined
by the equation of state for ideal gas as
$$
p = (\gamma - 1)\biggl(e - \frac{1}{2} \rho (v_1^2 + v_2^2)\biggr),
$$
where $\gamma$ is the ratio of specific heats $\gamma = \frac{c_p}{c_v} = 1.4$ for ideal gas.

In order to discretize the system with finite volumes, we rewrite the equations in conservation form
$$
\frac{\partial \boldsymbol{w}}{\partial t}
+ \frac{\partial}{\partial x} \boldsymbol{f}_1(\boldsymbol{w})
+ \frac{\partial}{\partial y} \boldsymbol{f}_2(\boldsymbol{w}) = \boldsymbol{0}
$$
which can be written in conservative variables $\boldsymbol{w} = (w_1, w_2, w_3, w_4)^T$, where $w_1 = \rho$, $w_2 = \rho v_1$, $w_3 = \rho v_2$, $w_4 = e$.

Euler equations in conservative form now read
$$
\frac{\partial}{\partial t}\left(\begin{array}{c}w_1\\ w_2\\ w_3\\ w_4\end{array}\right) + 
\frac{\partial}{\partial x}\left(\begin{array}{c} 
w_2 \\ \frac{w_2^2}{w_1} + p \\ \frac{w_2 w_3}{w_1}\\ (w_4 + p) \frac{w_2}{w_1}
\end{array}\right) + 
\frac{\partial}{\partial x}\left(\begin{array}{c}
w_3 \\ \frac{w_2 w_3}{w_1}\\ \frac{w_3^2}{w_1} + p \\ (w_4 + p) \frac{w_3}{w_1}
\end{array}\right) = \boldsymbol{0} 
$$
The constitutive law for ideal gas rewritten in conservative variables becomes
$$
p = (\gamma - 1)\biggl(w_4 - \frac{1}{2} \frac{w_2^2 + w_3^2}{w_1}\biggr)
$$

## Discretization
The unkown $\boldsymbol{w}$ is from now on discrete and located in cell centers. After discretization of space derivatives, the time-change of
$\boldsymbol{w}$ in the mesh cell/element with index $i$ is given by
$$
\frac{\boldsymbol{w}_i(t)}{\partial t} = -\frac{1}{|C_i|} \sum\limits_{j \in N(i)} \mathbf{H}\bigl(w_i(t), w_j(t), n_{ij}\bigr) l_{ij}
$$
with the following notation:

- $|C_i|$ is the surface/area of element $i$ in the mesh
- $N(i)$ denotes the set of all indices of neighbours of element $i$, i.e. all elements $j$ that share an edge with element $i$
- $n_{ij} is an oriented edge normal perpendicular to edge between elements $i$ and $j$ and pointing from element $i$ towards element $j$
- $l_{ij}$ is the length of edge separating elements $i$ and $j$
- $\mathbf{H}$ is the numerical flux function. The implementation uses [AUSM flux splitting scheme](https://ntrs.nasa.gov/api/citations/19940032139/downloads/19940032139.pdf)

For time discretization, an explicit Euler method was used. The discretization is only first-order accurate in time and space.

## Implementation and Numerical Test
The numerical test runs a [2D Riemann problem](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=f65f14aa0c0885c47ac06437505125ea1b5832b5) configuration number 3:

![Riemann setup](/pics/Riemann_setup.png)

The initial condition in this configuration is


| Quadrant |   $\rho$   |   $v_1$   |    $v_2$   |     p     |
| -------- | ---------- | --------- | ---------- | --------- |
|    1     |     1.5    |    0.0    |    0.0     |    1.5    |
|    2     |  0.5322581 | 1.2060454 |    0.0     |    0.3    |
|    3     |  0.1379928 | 1.2060454 | 1.2060454  | 0.0290323 |
|    4     |  0.5322581 |    0.0    | 1.2060454  |    0.3    |

The obtained solution at time $T = 0.3$ on a Cartesian mesh with $200 \times 200$ cells:

![Riemann solution](/pics/Riemann_density_small.png)
