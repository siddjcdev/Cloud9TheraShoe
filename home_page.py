def build_home(led_state):
    print ("Building homepage...")
    
    html_page = """   
      <!DOCTYPE HTML><html>
<!-- Rui Santos - Complete project details at https://RandomNerdTutorials.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files.
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. -->
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <script src="https://code.highcharts.com/highcharts.js"></script>
  <style>
    body {
      min-width: 310px;
    	max-width: 800px;
    	height: 400px;
      margin: 0 auto;
    }
    h2 {
      font-family: Arial;
      font-size: 2.5rem;
      text-align: center;
    }
  </style>
</head>
<body>
  <h2>ESP Weather Station</h2>
  <div id="chart-temperature" class="container"></div>
  <div id="chart-humidity" class="container"></div>
  <div id="chart-pressure" class="container"></div>
</body>
<script>
var chartT = new Highcharts.Chart({
  chart:{ renderTo : "chart-temperature" },
  title: { text: "BME280 Temperature" },
  series: [{
    showInLegend: false,
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
    title: { text: "Temperature (Celsius)" }
    //title: { text: "Temperature (Fahrenheit)" }
  },
  credits: { enabled: false }
});
setInterval(function ( ) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log('response' + this);
      console.log('responseText' + this.responseText);
      const data = JSON.parse(this.responseText);
      console.log('data' + data.data);
      var x = (new Date()).getTime(),
          y = parseFloat(data.data);
      
      if(chartT.series[0].data.length > 40) {
        chartT.series[0].addPoint([x, y], true, true, true);
      } else {
        chartT.series[0].addPoint([x, y], true, false, true);
      }
    }
  };
  xhttp.open("GET", "/temp", true);
  xhttp.send();
}, 10000 ) ;
</script>
        <center>   
         <form>   
          <button name="LED" type="submit" value="1"> LED ON </button>   
          <button name="LED" type="submit" value="0"> LED OFF </button>   
         </form>   
        </center>   
        <center><p>LED is now <strong>""" + led_state + """</strong>.</p></center>   
      </body>   
      </html>"""  
    return html_page   