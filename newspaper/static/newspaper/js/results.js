class BarPlot{
	/** 
	* BarPlot Constructor
	* @param id the div id in which we draw the BarPlot
	* @param data
	*/

	constructor(id, data, y_label){
		this.id = id;
		this.div = d3.select("#" + id);
		this.divHTML = document.getElementById(id);
		this.data = data;

		this.y_label = y_label;
		this.colors = ['#1368f2', '#00c69f', '#afaf00'];

		this.instantiateSVG();
		this.instantiateBar();
		this.render(this.data);
	}

	/**
	* Create SVG full size in div
	*/
	instantiateSVG(){
		let clientRect = this.divHTML.getBoundingClientRect();
		this.div.select("svg").remove();
		this.width = clientRect.width;
		this.height = clientRect.height;
		this.margin = {top: 20, right: 20, bottom: 30, left: 60};
		this.svg = this.div.append('svg')
						.attr('id', this.id)
						.attr('class', 'barplot-svg')
						.attr('width', this.width)
						.attr('height', this.height);

		this.innerWidth = this.width - (this.margin.right + this.margin.left);
		this.innerHeight = this.height - (this.margin.top + this.margin.bottom);

	}	

	instantiateBar(){
		// create x axis
		this.x = d3.scaleBand()
					.range([0, this.innerWidth])
					.padding(0.1);
		this.y = d3.scaleLinear()
					.range([this.innerHeight, 0]);

		this.g = this.svg.append('g')
				.attr('transform', 'translate(' + this.margin.left 
									+ ',' + this.margin.top +')');

		this.x.domain(this.data.map(d => d.abscisse));
		this.g.append("g")
      			.attr("transform", "translate(0," + this.innerHeight + ")")
      			.attr("class", "axisGrey")
      			.call(d3.axisBottom(this.x));
	}

	render(data){
		this.y.domain([0, d3.max(data, d => d.height_value)]);

		this.y_axis = this.g.append('g')
				.attr("class", "axisGrey")
				.call(d3.axisLeft(this.y));

		// text label for the y axis
		this.g.append("text")
		  .attr("transform", "rotate(-90)")
		  .attr("class", "Axis-Label")
		  .attr("y", 10 - this.margin.left)
		  .attr("x",10 - (this.innerHeight / 2))
		  .attr("dy", "1em")
		  .style("text-anchor", "middle")
		  .text(this.y_label);  


		this.g.selectAll(".bar")
			.data(data)
			.enter().append('rect')
				.attr('class', 'bar')
				.attr('x', d => this.x(d.abscisse))
				.attr('y', d => this.y(d.height_value))
				.attr('width', this.x.bandwidth())
				.attr('fill', (d, i) => this.colors[i])
				.attr('height', d => this.innerHeight - this.y(d.height_value))
				.on('mouseover', function (){
					d3.select(this).attr("stroke", 'black')
									.attr('stroke-width', 1);
				})
				.on('mouseout', function(d) {
					d3.select(this).attr('stroke-width', 0);
				});

		this.g.selectAll("text.bar")
  			.data(data)
			.enter().append("text")
  				.attr("class", "bar")
  				.attr("text-anchor", "middle")
  				.attr('fill', 'white')
  				.attr("x", d => this.x(d.abscisse) + this.x.bandwidth()/2)
  				.attr("y", d => this.y(d.height_value) + 2*this.margin.top)
  				.text(d => d.height_value + ' ' + d.unit);
	}


}
