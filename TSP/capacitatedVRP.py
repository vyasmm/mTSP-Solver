"""
Capacitated vehicle routing problem
Created on Thur Feb 27 12:12:40 2020

@author: Mansh
"""

import googlemaps
from googlemaps import Client
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

manuf_cntr = "Ghat road Railway Bridge, Great Nag Rd, Dhantoli, Nagpur, Maharashtra 440012" #Nagpur
distb_cntr1 = "Lokmanya Tilak Terminus Railway Yard, Mumbai, Maharashtra" #Mumbai
distb_cntr2 = "Lohana Para, Rajkot, Gujarat 360001" #Rajkot
distb_cntr3 = "Row Houses, Maruti Nagar, Khasmahal, Mithapur, Patna, Bihar 800001" #Patna
distb_cntr4 = "Ashoka Police Ln, Teen Murti Marg Area, New Delhi, Delhi 110011" #Delhi
distb_cntr5 = "Kannappar Thidal, Poongavanapuram, Chennai, Tamil Nadu 600003" #Chennai
distb_cntr6 = "Sirsi Rd, Tipu Nagar, Chamrajpet, Bengaluru, Karnataka 560018" #Bangaluru
distb_cntr7 = "Department of Gynecology, Medical College, Calcutta Medical College, College Square, Kolkata, West Bengal 700073" #Kolkata

distb_cntr_list = [distb_cntr1,distb_cntr2,distb_cntr3,distb_cntr4,distb_cntr5,
                   distb_cntr6,distb_cntr7]

def runCapacitatedVRP(key,num_vehicles,vehicle_capacity):
    
    locations = [manuf_cntr,distb_cntr1,distb_cntr2,distb_cntr3,distb_cntr4,
                 distb_cntr5,distb_cntr6,distb_cntr7]
    demands = [0,10,20,50,10,30,20,40]
    print(vehicle_capacity)
    
    #Create GoogleMap instance to request information from Google Maps API
    gmap = Client(key)
    
    #Fetch inter-location distances from google maps api
    dist_mtrx_resp = gmap.distance_matrix(locations,locations,mode="driving")
    
    #Store the distancevalues in a distance matrix
    x = 0
    y = 0
    dist_mtrx=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]        
              ]
    while (x<len(locations)):
        while (y<len(locations)):
            dist_mtrx[x][y]=dist_mtrx_resp.get("rows")[x].get("elements")[y].get("distance").get("value")
            y+=1
        y=0
        x+=1

    #####################
    # Distance Callback #
    #####################
    
    def CreateDistanceCallback(dist_matrix):
      def dist_callback(from_node, to_node):
        return dist_matrix[from_node][to_node]
      return dist_callback
    
    #############################################
    # Capacity callback & constraint definition #
    ############################################
    
    def CreateDemandCallback(dmd):
      def demand_callback(from_node, to_node):
        return dmd[from_node]
      return demand_callback
    
    def add_capacity_constraints(routing, demand_callback):
        """Adds capacity constraint"""
        capacity = "Capacity"
        #vehicle_capacity = 100
        routing.AddDimension(
            demand_callback,
            0, # null capacity slack
            vehicle_capacity, # vehicle maximum capacity
            True, # start cumul to zero
            capacity)
        
    ####################
    # Get Routes Array #
    ####################
    def get_routes_array(assignment, num_vehicles, routing):
      # Get the routes for an assignent and return as a list of lists.
      routes = []
      for route_nbr in range(num_vehicles):
        node = routing.Start(route_nbr)
        route = []
    
        while not routing.IsEnd(node):
          index = routing.NodeToIndex(node)
          route.append(index)
          node = assignment.Value(routing.NextVar(node))
        routes.append(route)
      return routes
    
    ###################
    #       Main      #
    ###################
      
    # Create Routing Model
    routing = pywrapcp.RoutingModel(len(locations), num_vehicles, 0)
    # Define weight of each edge based on distance
    dist_callback = CreateDistanceCallback(dist_mtrx)
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    #add capacity constraints
    dmd_callback = CreateDemandCallback(demands)
    add_capacity_constraints(routing, dmd_callback)
    # Setting first solution heuristic (cheapest addition).
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    routes = get_routes_array(assignment, num_vehicles, routing)
    
    #calculating route lengths
    route_lengths = []
    route_loads = []
    for route in routes:
        r_len = 0
        prevNode = 0
        route_ld = []
        for node in route:
            if (node!=0):
                print(prevNode,node)
                r_len += dist_mtrx[prevNode][node]
            prevNode = node
            route_ld.append(demands[node])
        print(r_len)
        route_lengths.append(r_len)
        route_loads.append(route_ld)
    print("Routes array:")
    print(routes)
    print("Route lengths:")
    print(route_lengths)
    print("Route loads:")
    print(route_loads)
    print("========")

    optimizedResp = {"routesArr":routes,"routesLen":route_lengths,"routesLoad":route_loads,
                     "constraints":{"n_veh":num_vehicles,"veh_ld_cap":vehicle_capacity}}
    return optimizedResp