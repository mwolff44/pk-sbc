$(function() {
	//$.getJSON('http://www.highcharts.com/samples/data/jsonp.php?filename=aapl-ohlcv.json&callback=?', function(data) {
	

	$.getJSON(jsonUrl, function(data) {
		// split the data set into ohlc and volume
		var ohlc = [],
			volume = [],
			dataLength = data.length;
			
		for (i = 0; i < dataLength; i++) {
			ohlc.push([
				data[i][0], // the date
				data[i][1], // open
				data[i][2], // high
				data[i][3], // low
				data[i][4] // close
			]);
			
			volume.push([
				data[i][0], // the date
				data[i][5] // the volume
			])
		}

		// set the allowed units for data grouping
		var groupingUnits = [[
			'week',                         // unit name
			[1]                             // allowed multiples
		], [
			'month',
			[1, 2, 3, 4, 6]
		]];

		// create the chart
		$('#container').highcharts('StockChart', {
		    
		    rangeSelector: {
				inputEnabled: $('#container').width() > 480,
		        selected: 1
		    },

		    title: {
		        text: 'Business Historical'
		    },

		    yAxis: [{
		        labels: {
		    		align: 'right',
		    		x: -3
		    	},
		        title: {
		            text: 'Sell-Cost'
		        },
		        height: '60%',
		        offset: 0,
		        lineWidth: 2
		    }, {
		    	labels: {
		    		align: 'right',
		    		x: -3
		    	},
		        title: {
		            text: 'Volume in Min'
		        },
		        top: '65%',
		        height: '35%',
		        offset: 0,
		        lineWidth: 2
		    }],
		    
		    series: [{
		        type: 'candlestick',
		        name: 'Sell Cost in main money unit',
		        data: ohlc,
		        dataGrouping: {
					units: groupingUnits
		        }
		    }, {
		        type: 'column',
		        name: 'Volume in minutes',
		        data: volume,
		        yAxis: 1,
		        dataGrouping: {
					units: groupingUnits
		        }
		    }]
		});
	});
});