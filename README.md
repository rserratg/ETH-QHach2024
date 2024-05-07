ETH Quantum Hackathon 2024
==============

**Team:** *SovrapponiMi & Platyrinchos* 

**Challenge:** *NVIDIA - Distributed Quantum Computing and the Vehicle Routing Problem*

## Overview

The goals of the challenge were to:

- Create a novel and useful application for the Vehicle Routing Problem (VRP)
- Translate the VRP to an instance of the Max Cut Problem
- Implement QAOA on a GPU using CUDA-Q to solve a small Max Cut Problem
- Investigate options to scale QAOA to handle large max cut problems, including circuit cutting and distributed computing
- Relate the solution to the max cut problem back to the original VRP

We proposed a situation where multiple fires need to be extinguished around a single source of water, and we need to find an optimal way to route several canadairs. Our approach is to reduce the VRP to several Travelling Salesman Problem (TSP) instances - i.e. finding the optimal way for one agent to visit multiple cities and circle back to the original location -, which we do by applying an heuristic clustering algorithm. We then implemented the reduction from the TSP to a MaxCut graph, following ref. [1], as well as a QAOA solver based on CUDA-Q. Both of these steps have been tested, though there was no time to benchmark the performance of QAOA (note that it requires a large number of connected qubits even for small graphs). The solution to the MaxCut (ideally, the state with the largest amplitude after optimization) can easily be translated into a solution of the TSP as follows. Each node in the maxCut graph (except the first one) can be numbered as (i,k), with i labelling a node in the original TSP and k being the time when it is visited. Nodes that belong to the same partition as the first node (in the same state as node 0) are part of the optimal path. Finally, we introduced a graph shrinking step to reduce the complexity of the MaxCut graph. Unfortunately, time ran out before we could integrate all of the steps.

## Contents

- Pdf file for our presentation
- Sources:
  - Clustering (Jupyter notebook): reduce CVRP to multiple instances of TSP by clustering the nodes
  - Qubo 2 MaxCut (Python script): reduction of the TSP problem to MaxCut via QUBO formulation
  - Graph shrinking (Jupyter notebook): graph-size reduction of a MaxCut instance into smaller instances
  - QAOA MaxCut: QAOA solver for MaxCut problem
 
## References

[1] Herzog et al. [arXiv:2404.05551](https://arxiv.org/abs/2404.05551)

