var addr = "localhost";
var port = "8080";
var manuf = "Ghat road Railway Bridge, Great Nag Rd, Dhantoli, Nagpur, Maharashtra 440012";
var distb1 = "Lokmanya Tilak Terminus Railway Yard, Mumbai, Maharashtra";
var distb2 = "Lohana Para, Rajkot, Gujarat 360001";
var distb3 = "Row Houses, Maruti Nagar, Khasmahal, Mithapur, Patna, Bihar 800001";
var distb4 = "Ashoka Police Ln, Teen Murti Marg Area, New Delhi, Delhi 110011";
var distb5 = "Kannappar Thidal, Poongavanapuram, Chennai, Tamil Nadu 600003";
var distb6 = "Sirsi Rd, Tipu Nagar, Chamrajpet, Bengaluru, Karnataka 560018";
var distb7 = "Department of Gynecology, Medical College, Calcutta Medical College, College Square, Kolkata, West Bengal 700073";
var distb_cntrs = [distb1, distb2, distb3, distb4, distb5, distb6, distb7];
var loc_names = ["Nagpur","Mumbai","Rajkot","Patna","Delhi","Chennai","Bengaluru","Kolkata"];

function fetchOptimizedRoute() {
  var prob_type =document.getElementById('opt_prob').value;
  var n_veh =document.getElementById('nVeh').value;
  var v_cap =document.getElementById('vCap').value;
  var scriptUrl = "http://" + addr + ":" + port + "/sampleJSON/"+prob_type+"/"+n_veh+"/"+v_cap;
  var result;
     $.ajax({
        url: scriptUrl,
        type: 'get',
        dataType: 'html',
        async: false,
        success: function(data) {
            result = data;
        } 
     });
     return JSON.parse(result);
}

function initMap() {
  var directionsService = new google.maps.DirectionsService();
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 10,
    center: {
      lat: 21.1458, 
      lng: 79.0882
    }
  });
  
  function directionsRenderer(pathno){
  	var routeAppearance1 = new google.maps.Polyline({
    		strokeColor: '#808080',
    		strokeOpacity: 0.6,
    		strokeWeight: 7});
    routeAppearance1.setMap(map);
    var routeAppearance2 = new google.maps.Polyline({
    		strokeColor: '#FEAA3A',
    		strokeOpacity: 0.6,
    		strokeWeight: 7});
    routeAppearance2.setMap(map);
    var renderer;
    if(pathno==0){renderer=new google.maps.DirectionsRenderer();}
		else if(pathno==1){
    	renderer = new google.maps.DirectionsRenderer({polylineOptions: routeAppearance1});}
    else if(pathno==2){
    	renderer = new google.maps.DirectionsRenderer({polylineOptions: routeAppearance2});}
    
		renderer.setMap(map);
		return renderer;
	}

  document.getElementById('submit').addEventListener('click', function() {
    var response = fetchOptimizedRoute();
    var list_of_routes = response.routesArr;
    for (var x=0; x<list_of_routes.length; x++) {
    	var directionsDisplay = directionsRenderer(x);
      plotRoute(directionsService, directionsDisplay, list_of_routes[x],response,x);
    }
    	printProblemConstraints(response);
  });
}

function plotRoute(directionsService,directionsDisplay,routeNodes,jsonResponse, routeIndx) {
//  var xyz1 = [];
  var waypts = [];
  var placeNames = [];
  placeNames.push(loc_names[0]);
  for (i = 1; i < routeNodes.length; i++) {
    var nodeIndx = routeNodes[i];
 //   xyz1.push(distb_cntrs[nodeIndx-1]);
    waypts.push({
      location: distb_cntrs[nodeIndx-1],
      stopover: true
    });
 //     document.getElementById('target-id').innerHTML = xyz1;   
    placeNames.push(loc_names[nodeIndx]);
  }

	var r_durtns=[];
  var r_dist=[];
  directionsService.route({
    origin: manuf,
    destination: manuf,
    waypoints: waypts,
    optimizeWaypoints: false,
    travelMode: 'DRIVING',
  }, function(response, status) {
    if (status === 'OK') {
      directionsDisplay.setDirections(response);
      var route = response.routes[0];
      for (var i = 0; i < route.legs.length; i++) {
      	r_durtns.push(route.legs[i].duration.text);
      	r_dist.push(route.legs[i].distance.text);
      }
      var fullRouteDetails = {
      	loc_lst:placeNames,durn_lst: r_durtns,dist_lst: r_dist};   printSummary(fullRouteDetails,jsonResponse,routeIndx);
    } 
    else {
      window.alert('Directions request failed due to ' + status);
    }
  });
}

function printSummary(route,jsonResponse,routeIndx){
	var prob_type =document.getElementById('opt_prob').value;
	var summaryPanel = document.getElementById('directions-panel');
  summaryPanel.innerHTML += '<br><b>------VEHICLE '+(routeIndx+1)+ ' ROUTE DETAILS-------- '+ '</b><br><br>';
  for (var i = 0; i < route.loc_lst.length; i++) {
        var routeSegment = i + 1;
        summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment + '</b><br>';
        summaryPanel.innerHTML += route.loc_lst[i] + ' - ' + ' to ' + ' - ';
        summaryPanel.innerHTML += route.loc_lst[i+1]?route.loc_lst[i+1]+'<br>':route.loc_lst[0]+'<br>';
        summaryPanel.innerHTML += '<b>Distance: </b>' + route.dist_lst[i] + ' ';
        if(prob_type=="a"||prob_type=="b"){
        	summaryPanel.innerHTML += '<b>Duration: </b>' + route.durn_lst[i] + '<br>';
        } else if(prob_type=="c"&& i<(route.loc_lst.length-1)){
        	summaryPanel.innerHTML += '<br><b>Earliest Delivery Tm: </b>'+jsonResponse.routesTW[routeIndx][i+1][0]+ ' s ';
          summaryPanel.innerHTML += '<b>Latest Delivery Tm: </b>'+jsonResponse.routesTW[routeIndx][i+1][1]+ ' s <br>';
        }
        if((prob_type=="b"||prob_type=="c") && i<(route.loc_lst.length-1)){
        	summaryPanel.innerHTML += '<b>Load Delivered: </b>' +jsonResponse.routesLoad[routeIndx][i+1] + '<br>';
        }
  summaryPanel.innerHTML += '<br>';
	}
}

function printProblemConstraints(response){
	var prob_type =document.getElementById('opt_prob').value;
	console.log("Problem Constraints:");
  console.log("No. of Vehicles: "+response.constraints.n_veh);
  if (prob_type != "a"){
  	console.log("Individual Vehicle load capacity: " +response.constraints.veh_ld_cap);
  }
  if (prob_type == "c"){
  	console.log("Unit Offloading time/ service time: " +response.constraints.unitOffloadTm+" s");
    console.log("Total Delivery Time Window: within "+ response.constraints.totDlvryTW+ "s post dispatch");
  }
}

