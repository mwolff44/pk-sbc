(function() {
  // -------- chart_revenue -----
  d3.json(jsonUrlrevenue,function(error,data) {
    nv.addGraph(function() {
      var chart = nv.models.lineChart()
                    .margin({top: 30, right: 60, bottom: 50, left: 100})  //Adjust chart margins to give the x-axis some breathing room.
                    .useInteractiveGuideline(true)  //We want nice looking tooltips and a guideline!
                    //.transitionDuration(350)  //how fast do you want the lines to transition?
                    //.showLegend(true)       //Show the legend, allowing users to turn on/off line series.
                    //.showYAxis(true)        //Show the y-axis
                    //.showXAxis(true)        //Show the x-axis
                    .x(function(d,i) { return i })
                    .y(function(d,i) {return d[1] })
      ;

      chart.xAxis
          .tickFormat(function(d) {
            var dx = data[0].values[d] && data[0].values[d][0] || 0;
            return d3.time.format('%b %d')(new Date(dx))
          });
          //.rotateLabels(-45));

      chart.yAxis     //Chart y-axis settings
          .axisLabel('Revenue / Cost (in main currency)')
          .tickFormat(d3.format(',f'));

      /* Done setting the chart up? Time to render it!*/
      //var myData = sinAndCos();   //You need data...

      d3.select('#chart_revenue svg')    //Select the <svg> element you want to render the chart in.   
          .datum(data)         //Populate the <svg> element with chart data...
          .transition()
          .duration(0)
          .call(chart);          //Finally, render the chart!

      //Update the chart when window resizes.
      //nv.utils.windowResize(function() { chart.update() });
      nv.utils.windowResize(chart.update);
      chart_revenue = chart;
      return chart;
    });
  });

  // -------- chart_volume -----
  
  //datav = [{"values": [[1400281200000, 3.36], [1400367600000, 0.03], [1400454000000, 30.15], [1400540400000, 34.57], [1400626800000, 30.73], [1400713200000, 32.12], [1400799600000, 60.69], [1400886000000, 3.61], [1400972400000, 0.05], [1401058800000, 68.54], [1401145200000, 339.0], [1401231600000, 130.58], [1401318000000, 17.12], [1401404400000, 133.52], [1401490800000, 111.67], [1401577200000, 0.02], [1401663600000, 640.63], [1401750000000, 565.65], [1401836400000, 646.74], [1401922800000, 639.96], [1402009200000, 798.42], [1402095600000, 493.09], [1402182000000, 65.13], [1402268400000, 380.07], [1402354800000, 17.01], [1402441200000, 388.32], [1402527600000, 0], [1402614000000, 0], [1402700400000, 0], [1402786800000, 0], [1402873200000, 0]], "bar": ["true"], "key": ["Revenue"]}, {"values": [[1400281200000, 25562], [1400367600000, 65], [1400454000000, 232339], [1400540400000, 225068], [1400626800000, 225401], [1400713200000, 198695], [1400799600000, 257652], [1400886000000, 14543], [1400972400000, 92], [1401058800000, 295177], [1401145200000, 980922], [1401231600000, 467542], [1401318000000, 70453], [1401404400000, 369460], [1401490800000, 307402], [1401577200000, 84], [1401663600000, 1814630], [1401750000000, 1578658], [1401836400000, 1799965], [1401922800000, 2344407], [1402009200000, 2540328], [1402095600000, 1345970], [1402182000000, 21832], [1402268400000, 1010094], [1402354800000, 66511], [1402441200000, 1078292], [1402527600000, 0], [1402614000000, 0], [1402700400000, 0], [1402786800000, 0], [1402873200000, 0]], "key": ["Duration"]}]

  d3.json(jsonUrlvolume,function(error,datav) {
    nv.addGraph(function() {
        var chart = nv.models.linePlusBarChart()
          .margin({top: 30, right: 60, bottom: 50, left: 100})
          .x(function(d,i) { return i })
          .y(function(d,i) {return d[1] })
        ;

        chart.xAxis
            .tickFormat(function(d) {
              var dx = datav[0].values[d] && datav[0].values[d][0] || 0;
              return d3.time.format('%b %d')(new Date(dx))
            });

        chart.y1Axis
            .axisLabel('Total calls count')
            .tickFormat(d3.format(',f'));

        chart.y2Axis
            .axisLabel('Succes calls count')
            .tickFormat(d3.format(',f'));

        d3.select('#chart_volume svg')
            .datum(datav)
            .transition()
            .duration(0)
            .call(chart);

        nv.utils.windowResize(chart.update);
        chart_volume = chart;

        return chart;
    });
  });

  d3.json(jsonUrlminute,function(error,datav) {
    nv.addGraph(function() {
        var chart = nv.models.linePlusBarChart()
          .margin({top: 30, right: 60, bottom: 50, left: 100})
          .x(function(d,i) { return i })
          .y(function(d,i) {return d[1] })
        ;

        chart.xAxis
            .tickFormat(function(d) {
              var dx = datav[0].values[d] && datav[0].values[d][0] || 0;
              return d3.time.format('%b %d')(new Date(dx))
            });

        chart.y1Axis
            .axisLabel('Volume in minutes')
            .tickFormat(d3.format(',f'));

        chart.y2Axis
            .axisLabel('ACD in seconds')
            .tickFormat(d3.format(',f'));

        d3.select('#chart_minute svg')
            .datum(datav)
            .transition()
            .duration(0)
            .call(chart);

        nv.utils.windowResize(chart.update);
        chart_minute = chart;

        return chart;
    });
  });

})();