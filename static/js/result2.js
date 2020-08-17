var impact_button = document.getElementsByClassName(
	"card-shadow-danger mb-3 widget-chart widget-chart2 text-left card"
  )[0];
  var brevity_button = document.getElementsByClassName(
	"card-shadow-success mb-3 widget-chart widget-chart2 text-left card"
  )[0];
  var style_button = document.getElementsByClassName(
	"card-shadow-warning mb-3 widget-chart widget-chart2 text-left card"
  )[0];
  var soft_skills_button = document.getElementsByClassName(
	"card-shadow-info mb-3 widget-chart widget-chart2 text-left card"
  )[0];

  var section = document.getElementsByClassName("section-criteria");

  var preview = document.getElementsByClassName("pdfPreview");


  function setNone() {
	
	for (var i = 0; i < section.length; i++) {
	  section[i].style.display = "none";
	  preview[i].style.width = "0";
	  preview[i].style.height = "0";
	}
  }
  
  impact_button.onclick = function () {
	var title = document.getElementsByClassName("card-header-title")[0];
	title.innerText = "Impact";
	setNone();
	document.getElementById('impact-section').style.display = "block";
	document.getElementById('impact-preview').style.width = "100%";
	document.getElementById('impact-preview').style.height = "960px";
  };

  brevity_button.onclick = function () {
	var title = document.getElementsByClassName("card-header-title")[0];
	title.innerText = "Brevity";
	setNone();
	document.getElementById('brevity-section').style.display = "block";
	document.getElementById('brevity-preview').style.width = "100%";
	document.getElementById('brevity-preview').style.height = "960px";
  };

  style_button.onclick = function () {
	var title = document.getElementsByClassName("card-header-title")[0];
	title.innerText = "Style";
	setNone();
	document.getElementById('style-section').style.display = "block";
	document.getElementById('style-preview').style.width = "100%";
	document.getElementById('style-preview').style.height = "960px";
  };

  soft_skills_button.onclick = function () {
	var title = document.getElementsByClassName("card-header-title")[0];
	title.innerText = "Soft Skills";
	setNone();
	document.getElementById('soft-skills-section').style.display = "block";
	document.getElementById('soft-skills-preview').style.width = "100%";
	document.getElementById('soft-skills-preview').style.height = "960px";
  };

  //Default value
  impact_button.click();

  var impactScore = parseInt(document.getElementById('impact-score').innerText.split('%').join(""));
  var brevityScore = parseInt(document.getElementById('brevity-score').innerText.split('%').join(""));
  var styleScore = parseInt(document.getElementById('style-score').innerText.split('%').join(""));
  var softskillsScore = parseInt(document.getElementById('soft-skills-score').innerText.split('%').join(""));
  var overallScore = ((impactScore + brevityScore + styleScore + softskillsScore)/4.0).toFixed(1);
  var overallScoreString = overallScore.toString() + "%";

  Chart.pluginService.register({
	beforeDraw: function(chart) {
	  if (chart.config.options.elements.center) {
		// Get ctx from string
		var ctx = chart.chart.ctx;

		// Get options from the center object in options
		var centerConfig = chart.config.options.elements.center;
		var fontStyle = centerConfig.fontStyle || 'Arial';
		var txt = centerConfig.text;
		var color = centerConfig.color || '#000';
		var maxFontSize = centerConfig.maxFontSize || 75;
		var sidePadding = centerConfig.sidePadding || 20;
		var sidePaddingCalculated = (sidePadding / 100) * (chart.innerRadius * 2)
		// Start with a base font of 30px
		ctx.font = "30px " + fontStyle;

		// Get the width of the string and also the width of the element minus 10 to give it 5px side padding
		var stringWidth = ctx.measureText(txt).width;
		var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

		// Find out how much the font can grow in width.
		var widthRatio = elementWidth / stringWidth;
		var newFontSize = Math.floor(30 * widthRatio);
		var elementHeight = (chart.innerRadius * 2);

		// Pick a new font size so it will not be larger than the height of label.
		var fontSizeToUse = Math.min(newFontSize, elementHeight, maxFontSize);
		var minFontSize = centerConfig.minFontSize;
		var lineHeight = centerConfig.lineHeight || 25;
		var wrapText = false;

		if (minFontSize === undefined) {
		  minFontSize = 20;
		}

		if (minFontSize && fontSizeToUse < minFontSize) {
		  fontSizeToUse = minFontSize;
		  wrapText = true;
		}

		// Set font settings to draw it correctly.
		ctx.textAlign = 'center';
		ctx.textBaseline = 'middle';
		var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
		var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
		ctx.font = fontSizeToUse + "px " + fontStyle;
		ctx.fillStyle = color;

		if (!wrapText) {
		  ctx.fillText(txt, centerX, centerY);
		  return;
		}

		var words = txt.split(' ');
		var line = '';
		var lines = [];

		// Break words up into multiple lines if necessary
		for (var n = 0; n < words.length; n++) {
		  var testLine = line + words[n] + ' ';
		  var metrics = ctx.measureText(testLine);
		  var testWidth = metrics.width;
		  if (testWidth > elementWidth && n > 0) {
			lines.push(line);
			line = words[n] + ' ';
		  } else {
			line = testLine;
		  }
		}

		// Move the center up depending on line height and number of lines
		centerY -= (lines.length / 2) * lineHeight;

		for (var n = 0; n < lines.length; n++) {
		  ctx.fillText(lines[n], centerX, centerY);
		  centerY += lineHeight;
		}
		//Draw text in center
		ctx.fillText(line, centerX, centerY);
	  }
	}
  });


var config = {
type: 'doughnut',
data: {
  datasets: [{
	data: [overallScore, 100 - overallScore],
	backgroundColor: [
	  "#FF6347",
	  "#D3D3D3",
	],
	hoverBackgroundColor: [
	  "#FF6347",
	  "#D3D3D3",
	]
  }],
  labels: ["Your Score"]
},
options: {
	legend: {
		reverse: true,
		display: true
	},
	title: {
		display: true,
		text: 'Overall Score',
		position: 'bottom'
	},
	tooltips: {
		enabled: false
	},
  	elements: {
	center: {
	  text: overallScoreString,
	  color: '#FF6347', // Default is #000000
	  fontStyle: 'Arial', // Default is Arial
	  sidePadding: 20, // Default is 20 (as a percentage)
	  minFontSize: 15, // Default is 20 (in px), set to false and text will not wrap.
	  lineHeight: 25 // Default is 25 (in px), used for when text wraps
	}
  }
}
};

var ctx = document.getElementById("overall-chart").getContext("2d");
var myChart = new Chart(ctx, config);