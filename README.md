# mTSP-Solver
A simple visualizer that will be able to determine an efficient solution for the Vehicle Routing Problem (Multiple TSP variant) based on user’s input criteria.

![alt text](https://github.com/vyasmm/mTSP-Solver/blob/main/output.png "Output")
![alt text](https://github.com/vyasmm/mTSP-Solver/blob/main/vehicleRoutingGoogleMapsDirections.png "Visualization")

It works with keeping the following set of constraints in mind -
1. Minimize the operational cost (A function purely based on distance).
2. Keeping in-mind Capacity each vehicle can carry.
3. Keeping in-mind Time window to reach destination.


The input consists of -
1. Main Depot from where the trucks will start from and return to.
2. All delivery locations.
3. Max number of Trucks available.
4. Algorithm to use.
My approach has been implementing few types of Approximation (Greedy and Local Search) Algorithms using Google’s OR-TOOLS powered by data from Google Maps API and visualizing the result on a simple webpage.
