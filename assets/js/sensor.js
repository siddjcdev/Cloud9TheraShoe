// const sensorValues = document.querySelector("#sensor-values");

// const sensorData = [];

// /*
//   Plotly.js graph and chart setup code
// */
// var sensorChartDiv = document.getElementById("sensor-chart");

// // History Data
// var sensorTrace = {
//   x: [],
//   y: [],
//   name: "LDR/Photoresistor",
//   mode: "lines+markers",
//   type: "line",
// };

// var sensorLayout = {
//   autosize: false,
//   width: 800,
//   height: 500,
//   colorway: ["#05AD86"],
//   margin: { t: 40, b: 40, l: 80, r: 80, pad: 0 },
//   xaxis: {
//     gridwidth: "2",
//     autorange: true,
//   },
//   yaxis: {
//     gridwidth: "2",
//     autorange: true,
//   },
// };
// var config = { responsive: true };

// Plotly.newPlot(sensorChartDiv, [sensorTrace], sensorLayout, config);

// // Will hold the sensor reads
// let newSensorXArray = [];
// let newSensorYArray = [];

// // The maximum number of data points displayed on our scatter/line graph
// let MAX_GRAPH_POINTS = 50;
// let ctr = 0;

// function updateChart(sensorRead) {
//   if (newSensorXArray.length >= MAX_GRAPH_POINTS) {
//     newSensorXArray.shift();
//   }
//   if (newSensorYArray.length >= MAX_GRAPH_POINTS) {
//     newSensorYArray.shift();
//   }
//   newSensorXArray.push(ctr++);
//   newSensorYArray.push(sensorRead);

//   var data_update = {
//     x: [newSensorXArray],
//     y: [newSensorYArray],
//   };

//   Plotly.update(sensorChartDiv, data_update);
// }

// // WebSocket support
// var targetUrl = `ws://${location.host}/ws`;
// var websocket;
// window.addEventListener("load", onLoad);

// function onLoad() {
//   //initializeSocket();
  
// //   TESTER = document.getElementById('sensor-chart');
// //   const sensorValues = document.querySelector("#sensor-values");

// //     Plotly.plot( TESTER, [{
// //         x: [1, 2, 3, 4, 5],
// //         y: [1, 2, 4, 8, 16] }], { 
// //         margin: { t: 0 } }, {showSendToCloud:true} );

// //     /* Current Plotly.js version */
// //     console.log( Plotly.BUILD );


//     var data = [
//         {
//           x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
//           y: [1, 3, 6],
//           type: 'scatter'
//         }
//       ];
      
//       Plotly.newPlot('sensor-chart', data);

// }

// function initializeSocket() {
//   console.log("Opening WebSocket connection MicroPython Server...");
//   websocket = new WebSocket(targetUrl);
//   websocket.onopen = onOpen;
//   websocket.onclose = onClose;
//   websocket.onmessage = onMessage;
// }
// function onOpen(event) {
//   console.log("Starting connection to WebSocket server..");
// }
// function onClose(event) {
//   console.log("Closing connection to server..");
//   setTimeout(initializeSocket, 2000);
// }
// function onMessage(event) {
//   console.log("WebSocket message received:", event);
//   updateValues(event.data);
//   updateChart(event.data);
// }

// function sendMessage(message) {
//   websocket.send(message);
// }

// function updateValues(data) {
//   sensorData.unshift(data);
//   if (sensorData.length > 20) sensorData.pop();
//   sensorValues.value = sensorData.join("\r\n");
// }

var chartT = new Highcharts.Chart({
	chart:{ renderTo : "chart-accel" },
	title: { text: "ADXL345 acceleration measurement" },
	series: [{
	  name: 'X',
	  color: '#FF0000',
	  showInLegend: true,
	  data: []
	}, {
	  name: 'Y',
	  color: '#FF9B00',
	  showInLegend: true,
	  data: []
	}, {
	  name: 'Z',
	  color: '#0000FF',
	  showInLegend: true,
	  data: []
	}],
	plotOptions: {
	  line: { animation: false,
		dataLabels: { enabled: true }
	  },
	  series: { color: "#059e8a" }
	},
	xAxis: { type: "datetime",
	  dateTimeLabelFormats: { second: "%H:%M:%S" }
	},
	yAxis: {
	  title: { text: "Acceleration" }
	  //title: { text: "Temperature (Fahrenheit)" }
	},
	credits: { enabled: false }
  });

/* document.getElementById("gameStart").addEventListener("click", function() {
  var timeleft = 15;
  var downloadTimer = setInterval(function() {
      document.getElementById("countdown").innerHTML = timeleft + "&nbsp;seconds remaining";
      timeleft -= 1;
      if (timeleft <= 0) {
          clearInterval(downloadTimer);
          document.getElementById("countdown").innerHTML = "Time is up!";
      }
  }, 1000);
}); */

let timerId; // Holds the timer ID
const pitchArray = [];  // Holds pitch (x) data 
const rollArray = [];   // Holds roll (y) data


function startAccelerometer() {
  // Start the timer
  console.log('Starting diagnostics...');
  timerId = setInterval(function ( ) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
      console.log('responseText' + this.responseText);
      const data = JSON.parse(this.responseText);
      var d = (new Date()).getTime(),
        //y = parseFloat(data.data);
        x = parseFloat(data.pitch);
        y = parseFloat(data.roll);
        z = parseFloat(data.yaw);

        a = parseFloat(data.fore);
        b = parseFloat(data.mid);
        c = parseFloat(data.hind);

        pitchArray.push(x);
        rollArray.push(y);


      //ACCELERATION
      if(chartT.series[0].data.length > 40) {
        chartT.series[0].addPoint([d, x], true, true, true);
      } else {
        chartT.series[0].addPoint([d, x], true, false, true);
      }
      if(chartT.series[1].data.length > 40) {
        chartT.series[1].addPoint([d, y], true, true, true);
      } else {
        chartT.series[1].addPoint([d, y], true, false, true);
      }
      if(chartT.series[2].data.length > 40) {
        chartT.series[2].addPoint([d, z], true, true, true);
      } else {
        chartT.series[2].addPoint([d, z], true, false, true);
      }

      //LOAD
      if(chartL.series[0].data.length > 10) {
        chartL.series[0].addPoint([d, a], true, true, true);
      } else {
        chartL.series[0].addPoint([d, a], true, false, true);
      }
      if(chartL.series[1].data.length > 10) {
        chartL.series[1].addPoint([d, b], true, true, true);
      } else {
        chartL.series[1].addPoint([d, b], true, false, true);
      }
      if(chartL.series[2].data.length > 10) {
        chartL.series[2].addPoint([d, c], true, true, true);
      } else {
        chartL.series[2].addPoint([d, c], true, false, true);
      }


      }
    };
    xhttp.open("GET", "/accel", true);
    xhttp.send();
    }, 1000 ) ;// Update every second

}

function stopAccelerometer() {
  // Stop the timer
  clearInterval(timerId);

  // Calculates average of dataset
  const avgPitch = pitchArray
                  .map((value) => value / pitchArray.length)
                  .reduce((a, b) => a + b);
  const avgRoll = rollArray
                  .map((value) => value / rollArray.length)
                  .reduce((a, b) => a + b);
  $('#spnResults').text("Pitch average:"+avgPitch.toFixed(2));
  $('#spnResults').append(";Roll average:"+avgRoll.toFixed(2));

  console.log('Stopped diagnostics');
}

		
var chartL = new Highcharts.Chart({
	chart:{ renderTo : "chart-load" },
	title: { text: "Load distribution" },
	series: [{
	  name: 'Forefoot',
	  color: '#FE5000',
	  showInLegend: true,
	  data: []
	}, {
	  name: 'Midfoot',
	  color: '#028A0F',
	  showInLegend: true,
	  data: []
	}, {
	  name: 'Hindfoot',
	  color: '#A45EE5',
	  showInLegend: true,
	  data: []
	}],
	plotOptions: {
	  line: { animation: false,
		dataLabels: { enabled: true }
	  },
	  series: { color: "#059e8a" }
	},
	xAxis: { type: "datetime",
	  dateTimeLabelFormats: { second: "%H:%M:%S" }
	},
	yAxis: {
	  title: { text: "load" }
	  //title: { text: "Temperature (Fahrenheit)" }
	},
	credits: { enabled: false }
  });


  