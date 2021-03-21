"""
Multivehicle Routing Problem
Created on Thur Feb 27 08:12:40 2020

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
distb_cntr7 = "Department of Gynecology, Medical College, Calcutta Medical College, College Square, Kolkata, West Bengal 700073" #Kol kata


distb_cntr_list = [distb_cntr1,distb_cntr2,distb_cntr3,distb_cntr4,distb_cntr5,
                   distb_cntr6,distb_cntr7]


def runMultiVehicleOptimzation(key,num_vehicles):
    locations = [manuf_cntr,distb_cntr1,distb_cntr2,distb_cntr3,distb_cntr4,
                 distb_cntr5,distb_cntr6,distb_cntr7]
    
    #Create GoogleMap instance to request information from Google Maps API
    gmap = Client(key)
    #my_dist = gmap.distance_matrix('Delhi','Mumbai')['rows'][0]['elements'][0]
   

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
            dist_mtrx[x][y]/=1000
            y+=1
        y=0
        x+=1
    print(dist_mtrx)
    
    
    ###################################
    # Distance callback and dimension #
    ####################################
    
    def CreateDistanceCallback(dist_matrix):
      def dist_callback(from_node, to_node):
        return dist_matrix[from_node][to_node]
      return dist_callback
    
    def add_distance_dimension(routing, dist_callback):
      """Add Global Span constraint"""
      distance = "Distance"
      maximum_distance = 90000000
      routing.AddDimension(
        dist_callback,
        0, # null slack
        maximum_distance, # maximum distance per vehicle
        True, # start cumul to zero
        distance)
      distance_dimension = routing.GetDimensionOrDie(distance)
      # Try to minimize the max distance among vehicles.
      distance_dimension.SetGlobalSpanCostCoefficient(100)
    
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
    
    ########
    # Main #
    ########
      
    # Create Routing Model
    routing = pywrapcp.RoutingModel(len(locations), num_vehicles, 0)
    # Define weight of each edge
    dist_callback = CreateDistanceCallback(dist_mtrx)
    routing.SetArcCostEvaluatorOfAllVehicles(dist_callback)
    add_distance_dimension(routing, dist_callback)
    # Setting first solution heuristic (cheapest addition).
    search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
    #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.GLOBAL_CHEAPEST_ARC)
    #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.SAVINGS)
    #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.CHRISTOFIDES	)
    #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.BEST_INSERTION)
    #search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.AUTOMATIC)
    search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.OBJECTIVE_TABU_SEARCH)
    #search_parameters.local_search_metaheuristic = (routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING)
    search_parameters.time_limit_ms = 300000
    search_parameters.log_search = True
    # Solve the problem.
    assignment = routing.SolveWithParameters(search_parameters)
    routes = get_routes_array(assignment, num_vehicles, routing)
    
    #calculating route lengths
    route_lengths = []
    for route in routes:
        r_len = 0
        prevNode = 0
        for node in route:
            if (node!=0):
                print(prevNode,node)
                r_len += dist_mtrx[prevNode][node]
            prevNode = node
        r_len += dist_mtrx[prevNode][route[0]]
        print(r_len)
        route_lengths.append(r_len)
    print("Routes array:")
    print(routes)
    print("Route lengths:")
    print(route_lengths)
    print("========")
    print(sum(route_lengths))
    
    optimizedResp = {"routesArr":routes,"routesLen":route_lengths,"constraints":{"n_veh":num_vehicles}}
    return optimizedResp