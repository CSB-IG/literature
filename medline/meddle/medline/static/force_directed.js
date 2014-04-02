var width = "800", height = "800";

var color = d3.scale.category20b();

var year_gray_scale = d3.scale.linear()
    .domain([1987, 2013])
    .range([1, 230]);

var degree_scale = d3.scale.linear()
    .domain([1, 20])
    .range([5,20]);


var force = d3.layout.force()
    .size([width, height])
    .friction(0.7)
    .gravity(0.09)
    .charge(-50)
    .linkDistance(30);

function dragstart(d) {
    d.fixed = true;
    d3.select(this).classed("fixed", true);
}


var drag = force.drag()
    .on("dragstart", dragstart);

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height);

svg.append("svg:defs").selectAll("marker")
    .data(["link"])
    .enter().append("svg:marker")
    .attr("id", String)
    .attr("refX", -2)
    .attr("refY", 0.5)
    .attr("markerWidth", 1)
    .attr("markerHeight", 1)
    .attr("orient", "auto")
    .append("svg:circle")
    .attr("cx", 6)
    .attr("cy", 6)
    .attr("r", 10)
    .attr("stroke", "green")
    .attr("fill", d3.rgb(200,200,200))





d3.json("trends_major_since_1987.json", function(error, graph) {
    force
	.nodes(graph.nodes)
	.links(graph.links)
	.start();

    var link = svg.selectAll(".link")
    	.data(graph.links)
    	.enter().append("line")
    	.attr("class", "link")
    	.attr("marker-start",  function(d) { return "url(#link)"; })
    	.style("stroke-width", function(d) { return d.weight+1; })




    var node = svg.selectAll(".node")
	.data(graph.nodes)
	.enter()
	.append("a")
	.attr("class", "node")
	.attr("xlink:href", function(d) { return "http://www.ncbi.nlm.nih.gov/pubmed/"+d.name;} )
	.append("circle")
	.attr("r", function(d) { return degree_scale(d.degree); } )
	.style("fill", function(d) { return d3.rgb(year_gray_scale(d.year)+9, year_gray_scale(d.year), 150); })
	.call(drag);

    node.append("text")
	.attr("x", 12)
	.attr("dy", ".35em")
	.text(function(d) { return d.name; });


    node.append("title")
	.text(function(d) { return d.year+" "+d.title; });


    force.on("tick", function() {
	link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

	node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    });

});
