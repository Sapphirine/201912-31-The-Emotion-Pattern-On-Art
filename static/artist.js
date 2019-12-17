$(document).ready(function(){
    const emotions = ["Amusement", "Anger", "Awe", "Content", "Disgust", "Excitement", "Fear", "Sad"];
    var width = 850,
        height = 850,
        margin = 200;

    // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
    var radius = Math.min(width, height) / 2 - margin;

    // append the svg object to the div called 'artist_chart'
    var svg = d3.select("#artist_chart")
      .append("svg")
        .attr("width", width)
        .attr("height", height)
      .append("g")
        .attr("transform", "translate(" + width / 3 + "," + height / 3 + ")");


   // A function that create / update the plot for a given variable:
    function update(data) {
      // set the color scale
        var color = d3.scaleOrdinal()
          .domain(emotions)
          .range(["#69b3a2", "steelblue", "rgba(198, 45, 205, 0.8)", "rgb(12,240,233)", "gold", "green", "pink", "grey"]);

      // Compute the position of each group on the pie:
      var pie = d3.pie()
        .value(function(d) {return d.value; })
        .sort(function(a, b) { console.log(a, b) ; return d3.ascending(a.key, b.key);} ); // This make sure that group order remains the same in the pie chart
      var data_ready = pie(d3.entries(data));

      // map to data
      var u = svg.selectAll("path")
        .data(data_ready);

      // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
      u
        .enter()
        .append('path')
        .merge(u)
        .transition()
        .duration(1000)
        .attr('d', d3.arc()
          .innerRadius(0)
          .outerRadius(radius)
        )
        .attr('fill', function(d){ return(color(d.data.key)) })
        .attr("stroke", "white")
        .style("stroke-width", "2px")
        .style("opacity", 1);

      // remove the group that is not present anymore
      u
        .exit()
        .remove();

    var legend = svg.selectAll(".myLegend")
        .data(data_ready)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) {
            return "translate(-500," + i * 19 + ")";
        });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", function(d) {
            return color(d.data.key);
        });

    legend.append("text")
        .attr("x", width + 5)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "start")
        .style("font-family", "sans-serif")
        .style("font-size", "13px")
        .style("fill", "black")
        .text(function(d) {
            return d.data.key;
        });

    }

    // load datasets
    let artist_scores = [];
    for (let i=0; i<artist_names.length; i++) {
        d3.csv('../static/artist_emotion/'+artist_names[i]+'_scores.csv').then(function(data){
            data.forEach(function(d){
                for(let i=0; i<emotions.length; i++) {
                    d[emotions[i]] = +d[emotions[i]]
                }
            });
            console.log(data[0]);
            artist_scores.push(data[0]);
            if (i === 0){
                update(data[0])
            }
        });

    }

    for (let i=0; i<artist_names.length; i++) {
        console.log(artist_names[i]);
        let artist_choice = $('<option></option>');
        artist_choice.append(artist_names[i].split('_').join(' '));
        $('#artist_menu').append(artist_choice);
    }

    $('#artist_menu').change(function(){
        let name_selected = $(this).val().split(' ').join('_');
        let idx = artist_names.indexOf(name_selected);
        update(artist_scores[idx]);
    });

});