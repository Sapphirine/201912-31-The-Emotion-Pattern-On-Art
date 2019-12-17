$(document).ready(function() {
    function sortByYearAscending(a, b){
        return a.year - b.year;
    }
    // load 8 datasets
    var year_Amusement = [];
    d3.csv('../static/year_emotion/year_Amusement_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Amusement.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Amusement = year_Amusement.sort(sortByYearAscending);
        update(year_Amusement);
    });

    var year_Anger = [];
    d3.csv('../static/year_emotion/year_Anger_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Anger.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Anger = year_Anger.sort(sortByYearAscending);
    });

    var year_Awe = [];
    d3.csv('../static/year_emotion/year_Awe_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Awe.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Awe = year_Awe.sort(sortByYearAscending);
    });

    var year_Content = [];
    d3.csv('../static/year_emotion/year_Content_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Content.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Content = year_Content.sort(sortByYearAscending);
    });

    var year_Disgust = [];
    d3.csv('../static/year_emotion/year_Disgust_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Disgust.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Disgust = year_Disgust.sort(sortByYearAscending);
    });

    var year_Excitement = [];
    d3.csv('../static/year_emotion/year_Excitement_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Excitement.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Excitement = year_Excitement.sort(sortByYearAscending);
    });

    var year_Fear = [];
    d3.csv('../static/year_emotion/year_Fear_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Fear.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Fear = year_Fear.sort(sortByYearAscending);
        console.log(year_Fear)
    });

    var year_Sad = [];
    d3.csv('../static/year_emotion/year_Sad_scores.csv').then(function(data){
        for(var i=0; i< data.length; i++) {
            year_Sad.push({'year':new Date(+data[i].year, 0, 1), 'avg': parseFloat(data[i].avg), 'max': parseFloat(data[i].max), 'min': parseFloat(data[i].min)})
        }
        year_Sad = year_Sad.sort(sortByYearAscending);
    });
    // set the dimensions and margins of the graph
    var margin = {
            top: 10,
            right: 30,
            bottom: 50,
            left: 60
        },
        width = 800 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom,
        heightXaxis = height + 30;

    // append the svg object to the body of the page
    var svg = d3.select("#year_chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    // Initialise a X axis:
    // var x = d3.scalePoint().range([0, width]);
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // var x = d3.scaleLinear().range([0,width]);
    // var xAxis = d3.axisBottom().scale(x); //.tickFormat(quarter_tickformat);
    var xAxis = d3.axisBottom().scale(x).tickFormat(d3.timeFormat("%Y"));
    svg.append("g")
        .attr("transform", "translate(0," + heightXaxis + ")")
        .attr("class", "myXaxis")

    // Initialize an Y axis
    // var y = d3.scaleLinear().range([height, 0]);

    var yAxis = d3.axisLeft().scale(y);
    svg.append("g")
        .attr("class", "myYaxis")



    var colors = ["rgba(54, 30, 175, 0.2)", "rgba(54, 174, 175, 0.5)", "rgba(249, 208, 87, 0.2)"];

    var legend = svg.selectAll(".myLegend")
        .data(colors)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) {
            return "translate(-80," + i * 19 + ")";
        });

    legend.append("rect")
        .attr("x", width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", function(d, i) {
            return colors.slice()[i];
        });

    legend.append("text")
        .attr("x", width + 5)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "start")
        .style("font-family", "sans-serif")
        .style("font-size", "13px")
        .style("fill", "black")
        .text(function(d, i) {
            switch (i) {
                case 0:
                    return "Avg";
                case 1:
                    return "Max";
                case 2:
                    return "Min";
            }
        });

    svg.append("text")
        .attr("x", (width / 2))
        .attr("y", 10)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        //         .style("font-family", "sans-serif")
        .style("fill", "black")
        //         .style("text-decoration", "underline")
        .text("Emotion Percentage");

    // Create a function that takes a dataset as input and update the plot:
    function update(data) {

        // Create the X axis:
        x.domain(d3.extent(data, function(d) {
            return d.year;
        }));
        svg.selectAll(".myXaxis").transition()
            .duration(3000)
            .call(xAxis);

        // // create the Y axis
        y.domain([d3.min(data, function(d) {
            return d.min
        }), d3.max(data, function(d) {
            return d.max
        })]);

        svg.selectAll(".myYaxis")
            .transition()
            .duration(3000)
            .call(yAxis);

        // Create a update selection: bind to the new data
        var u = svg.selectAll(".areaA")
            .data([data], function(d) {
                return d.year
            });

        var color = d3.scaleOrdinal()
            .domain(["Avg", "Max", "Min"])
            // .range(["rgba(0, 0, 200, 0.7)", "rgba(54, 174, 175, 0.65)"]);
            .range(colors);
        // Updata the line
        u
            .enter()
            .append("path")
            .attr("class", "areaA")
            .merge(u)
            .transition()
            .duration(3000)
            .attr("d", d3.area()
                .curve(d3.curveMonotoneX)
                .x(function(d) {
                    return x(d.year);
                })
                .y0(y(0))
                .y1(function(d) {
                    return y(d.avg);
                }))
            .style("fill", function(d) {
                return color("Avg");
            });

        var v = svg.selectAll(".areaMax")
            .data([data], function(d) {
                return d.year
            });

        v
            .enter()
            .append("path")
            .attr("class", "areaMax")
            .merge(v)
            .transition()
            .duration(3000)
            .attr("d", d3.area()
                .curve(d3.curveMonotoneX)
                .x(function(d) {
                    return x(d.year);
                })
                .y0(y(0))
                .y1(function(d) {
                    return y(d.max);
                }))
            .style("fill", function(d) {
                return color("Max");
            });

        var w = svg.selectAll(".areaMin")
            .data([data], function(d) {
                return d.year
            });

        w
            .enter()
            .append("path")
            .attr("class", "areaMin")
            .merge(w)
            .transition()
            .duration(3000)
            .attr("d", d3.area()
                .curve(d3.curveMonotoneX)
                .x(function(d) {
                    return x(d.year);
                })
                .y0(y(0))
                .y1(function(d) {
                    return y(d.min);
                }))
            .style("fill", function(d) {
                return color("Min");
            });

    }

    // At the beginning, I run the update function on the first dataset:
    update(year_Amusement);


    $('#emotion_btn').click(function() {
        var emotion = $("input[name='emotion']:checked").val();
        console.log(emotion);
        if (emotion === "Amusement") {
            update(year_Amusement);
        } else if (emotion === "Anger") {
            update(year_Anger);
        } else if (emotion === "Awe") {
            update(year_Awe);
        } else if (emotion === "Content") {
            update(year_Content);
        } else if (emotion === "Disgust") {
            update(year_Disgust);
        } else if (emotion === "Excitement") {
            update(year_Excitement);
        } else if (emotion === "Fear") {
            update(year_Fear);
        } else if (emotion === "Sad") {
            update(year_Sad);
        }

    });



});