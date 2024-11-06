# AlgoGEARS
AlgoGEARS (**Algo**rithms of (Computational) **G**eometry with **E**ntities **A**vailable for **R**euse and **S**erialization) is a library that provides implementations of certain computational geometry algorithms adapted for educational purposes.

The basic entities it uses, such as geometric objects and binary trees, are constructed as Pydantic models that can be easily reused and serialized.

This library is a continuation of PyCompGeomAlgorithms https://pypi.org/project/PyCompGeomAlgorithms/, a library by the same author as this one--artandfi (Artem Fisunenko)."

## Contents
This library contains adapted implementations of computational geometry algorithms described in Franco P. Preparata and Michael I. Shamos' book "Computational Geometry: An Introduction". These algorithms are subdivided into three topics: geometric searching, constructing convex hulls, and proximity problems.
#### Geometric searching
* Point location
  * *Slab method*: locate a point in a planar graph between its two edges.
  * *Chain method*: locate a point in a planar graph between its two monotone chains connecting its lower-most and upper-most vertices.
  * *Triangulation refinement method **(TBD)***: locate a point in a triangulated planar graph in one of the triangles.
* Range-searching
  * *k-D tree method*: find out which or how many points of a given set lie in a specified range, using a multidimensional binary tree (here, 2-*D* tree).
  * *Range-tree method **(TBD)***: find out which or how many points of a given set lie in a specified range, using a range tree data structure.
#### Constructing convex hulls
* Static problem
  * *Graham's scan*: construct the convex hull of a given set of points, using a stack of points.
  * *Quickhull*: construct the convex hull of a given set of points, using the partitioning of the set and merging the subsets similar to those in Quicksort algorithm.
  * *Jarvis' march*: construct the convex hull of a given set of points, using the so-called gift wrapping technique.
* Dynamic problem
  * *Preparata's algorithm*: construct the convex hull of a set of points being dynamically added to a current hull.
  * *Dynamic convex hull maintenance*: construct the convex hull of a set of points and re-construct it on addition or deletion of a point.
#### Proximity problems
* *Divide-and-conquer closest pair search **(TBD)***: given a set of points, find the two points with the smallest mutual distance, using divide-and-conquer approach.
* *Divide-and-conquer Voronoi diagram constructing **(TBD)***: given a set points, construct their Voronoi diagram, using divide-and-conquer approach.
