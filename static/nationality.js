$(document).ready(function() {

    // set the dimensions and margins of the graph
    let margin = {top: 20, right: 0, bottom: 0, left: 0},
        width = 700 - margin.left - margin.right,
        height = 700 - margin.top - margin.bottom,
        innerRadius = 90,
        outerRadius = Math.min(width, height) / 2;   // the outerRadius goes from the middle of the SVG area to the border
    const emotions = ["Amusement", "Anger", "Awe", "Content", "Disgust", "Excitement", "Fear", "Sad"];
    let colors = ["#69b3a2", "steelblue", "rgba(198, 45, 205, 0.8)", "rgb(12,240,233)", "gold", "green", "pink", "grey"];

    $('#emotion_buttons_nationality').change(function(){
        d3.select('#nationality_chart').select("svg").remove();
        $("input:checked").each(function(){
            let emotion_chosen = $(this).val();
            let idx = emotions.indexOf(emotion_chosen);
            d3.csv("./static/nationality_emotion/"+"nationality_" + emotion_chosen + "_scores.csv", function(data) {
                // append the svg object
                let svg = d3.select("#nationality_chart")
                  .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                  .append("g")
                    .attr("transform", "translate(" + (width / 2 + margin.left) + "," + (height / 2 + margin.top) + ")");

                // Scales
                let x = d3.scaleBand()
                  .range([0, 2 * Math.PI])    // X axis goes from 0 to 2pi = all around the circle. If I stop at 1Pi, it will be around a half circle
                  .align(0)                  // This does nothing
                  .domain(data.map(function(d) { return d.Nationality; })); // The domain of the X axis is the list of states.
                let y = d3.scaleRadial()
                  .range([innerRadius, outerRadius])   // Domain will be define later.
                  .domain([0, 0.4]); // Domain of Y is from 0 to the max seen in the data

                // Add the bars
                svg.append("g")
                .selectAll("path")
                .data(data)
                .enter()
                .append("path")
                  .attr("fill", colors[idx])
                  .attr("d", d3.arc()     // imagine your doing a part of a donut plot
                      .innerRadius(innerRadius)
                      .outerRadius(function(d) { return y(d['Value']); })
                      .startAngle(function(d) { return x(d.Nationality); })
                      .endAngle(function(d) { return x(d.Nationality) + x.bandwidth(); })
                      .padAngle(0.01)
                      .padRadius(innerRadius));

                // Add the labels
                svg.append("g")
                  .selectAll("g")
                  .data(data)
                  .enter()
                  .append("g")
                    .attr("text-anchor", function(d) { return (x(d.Nationality) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
                    .attr("transform", function(d) { return "rotate(" + ((x(d.Nationality) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d['Value'])+10) + ",0)"; })
                  .append("text")
                    .text(function(d){return(d.Nationality)})
                    .attr("transform", function(d) { return (x(d.Nationality) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
                    .style("font-size", "11px")
                    .attr("alignment-baseline", "middle")

            });

        });
    });


    // default to amusement

    d3.csv("./static/nationality_emotion/"+"nationality_Amusement_scores.csv", function(data) {
    // append the svg object
    let svg = d3.select("#nationality_chart")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + (width / 2 + margin.left) + "," + (height / 2 + margin.top) + ")");

    // Scales
    let x = d3.scaleBand()
      .range([0, 2 * Math.PI])    // X axis goes from 0 to 2pi = all around the circle. If I stop at 1Pi, it will be around a half circle
      .align(0)                  // This does nothing
      .domain(data.map(function(d) { return d.Nationality; })); // The domain of the X axis is the list of states.
    let y = d3.scaleRadial()
      .range([innerRadius, outerRadius])   // Domain will be define later.
      .domain([0, 0.4]); // Domain of Y is from 0 to the max seen in the data

    // Add the bars
    svg.append("g")
    .selectAll("path")
    .data(data)
    .enter()
    .append("path")
      .attr("fill", colors[0])
      .attr("d", d3.arc()     // imagine your doing a part of a donut plot
          .innerRadius(innerRadius)
          .outerRadius(function(d) { return y(d['Value']); })
          .startAngle(function(d) { return x(d.Nationality); })
          .endAngle(function(d) { return x(d.Nationality) + x.bandwidth(); })
          .padAngle(0.01)
          .padRadius(innerRadius));

    // Add the labels
    svg.append("g")
      .selectAll("g")
      .data(data)
      .enter()
      .append("g")
        .attr("text-anchor", function(d) { return (x(d.Nationality) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
        .attr("transform", function(d) { return "rotate(" + ((x(d.Nationality) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d['Value'])+10) + ",0)"; })
      .append("text")
        .text(function(d){return(d.Nationality)})
        .attr("transform", function(d) { return (x(d.Nationality) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
        .style("font-size", "11px")
        .attr("alignment-baseline", "middle")

    });

});