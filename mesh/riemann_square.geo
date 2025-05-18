lc = 0.4;
n_points = 201;

Point(1) = {0, 0, 0, lc};
Point(2) = {1, 0, 0, lc};
Point(3) = {1, 1, 0, lc};
Point(4) = {0, 1, 0, lc};

Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

Curve Loop(1) = {1, 2, 3, 4};

Plane Surface(1) = {1};

Transfinite Curve{1} = n_points;
Transfinite Curve{2} = n_points;
Transfinite Curve{3} = n_points;
Transfinite Curve{4} = n_points;
Transfinite Surface{1} = {1, 2, 3, 4};
Recombine Surface{1};

Physical Curve("bottom") = {1};
Physical Curve("top") = {3};
Physical Curve("left") = {4};
Physical Curve("right") = {2};

Physical Surface("inside") = {1};
