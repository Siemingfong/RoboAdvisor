function d3PriceLinefunction(seg_width, mark_list) {
  console.log("in d3PriceLinefunction", seg_width, mark_list);
  const margin = {
      top: 20,
      right: 20,
      bottom: 20,
      left: 40
    },
    height = 500 - margin.top - margin.bottom;
  const margin2 = {
    top: 210,
    right: 20,
    bottom: 20,
    left: 50
  };
  const width = 0.95 * seg_width - margin.left - margin.right;

  // parseTime func  [2010-07-18 %Y-%m-%d]  [14-Oct-08 %d-%b-%y]
  const parseTime = d3.timeParse("%Y-%m-%d");
  const timeFormat = d3.timeFormat("%Y-%m-%d");
  const bisectDate = d3.bisector(function (d) {
    return d.date;
  }).left;
  const legendFormat = d3.timeFormat('%b %d, %Y');
  // Set x, y scale-range
  const x = d3
    .scaleTime()
    .range([0, width]);
  const y = d3
    .scaleLinear()
    .range([height, 0]);

  // Create valueline based on data, close
  const valueline = d3
    .line()
    .x(d => x(d.date)) //x(function (d) {return x(d.date)
    .y(d => y(d.close)); //y(function (d) {return y(d.close)

  // svg initial set , Add 'g' at svg place setting.
  const svg = d3
    .select("#segment_w")
    .append('svg')
    .attr("class", "lineChart")
    .attr("id", "lineChart")
    .attr("style", "outline: 2px solid #b3abab;")
    .attr("width", 0.95 * seg_width)
    .attr("height", height + margin.top + margin.bottom)

  // 遮色片：用於裁剪
  svg
    .append('defs')
    .append('clipPath')
    .attr('id', 'clip')
    .append('rect')
    .attr('width', width)
    .attr('height', height);

  // focus:主資訊區
  const focus = svg
    .append("g")
    .attr('class', 'focus')
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // gridlines in x axis function
  function make_x_gridlines() {
    return d3
      .axisBottom(x)
      .ticks(10)
  }

  // gridlines in y axis function
  function make_y_gridlines() {
    return d3
      .axisLeft(y)
      .ticks(10)
  }
  // Read data and main func.
  d3
    .tsv(btc_tsv_data, function (error, data) {
      if (error) 
        throw error;
      
      // use forEach func to get every data with func(d)
      data
        .forEach(function (d) {
          d.date = parseTime(d.Datee);
          d.close = +d.Close;
        });

      // Set domain range
      x.domain(d3.extent(data, d => d.date));
      y.domain([
        0, d3.max(data, d => d.close)
      ]);

      // add the X gridlines
      focus
        .append("g")
        .attr("class", "grid")
        .attr("transform", "translate(0," + height + ")")
        .call(make_x_gridlines().tickSize(-height).tickFormat(""))

      // add the Y gridlines
      focus
        .append("g")
        .attr("class", "grid")
        .call(make_y_gridlines().tickSize(-width).tickFormat(""))

      // Add path-valueline at svg
      focus
        .append("path")
        .data([data])
        .attr("class", "line")
        .attr("d", valueline);

      // Add g to show x-axis
      focus
        .append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      // Add g to show y-axis
      focus
        .append("g")
        .attr("class", "y-axis")
        .call(d3.axisLeft(y));

      // Add upper hint region
      var helper = focus
        .append('g')
        .attr('class', 'chart__helper')
        .style('text-anchor', 'end')
        .attr('transform', 'translate(' + width + ', 0)');
      // Upper hint for data info
      var helperText = helper.append('text');

      // Follow circle with mouse movement
      var priceTooltip = focus
        .append('g')
        .attr('class', 'chart__tooltip--price')
        .append('circle')
        .style('display', 'none')
        .attr('r', 10.5);

      // Follow x line with mouse movement
      var pricetipLineX = focus
        .append('line')
        .classed('x', true)
        .attr('class', 'chart_price_x');

      // Follow y line with mouse movement
      var pricetipLineY = focus
        .append('line')
        .classed('y', true)
        .attr('class', 'chart_price_y');

      var pricetipText = focus
        .append('text')
        .attr('class', 'chart_price_text');

      // MouseArea to detect the mouse move, and callback the mosemove()
      var mouseArea = svg
        .append('g')
        .attr('class', 'chart__mouse')
        .append('rect')
        .attr('class', 'chart__overlay')
        .attr('width', width)
        .attr('height', height)
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
        .on('mouseover', function () {
          // helper.style('display', null);
          priceTooltip.style('display', null);
          pricetipLineX.style('display', null);
          pricetipLineY.style('display', null);
          pricetipText.style('display', null);
        })
        .on('mouseout', function () {
          // helper.style('display', 'none');
          priceTooltip.style('display', 'none');
          pricetipLineX.style('display', 'none');
          pricetipLineY.style('display', 'none');
          pricetipText.style('display', 'none');
        })
        .on('mousemove', mousemove);

      // Mousemove function
      function mousemove() {
        var x0 = x.invert(d3.mouse(this)[0]);
        var i = bisectDate(data, x0, 1);
        var d0 = data[i - 1];
        var d1 = data[i];
        var d = x0 - d0.date > d1.date - x0
          ? d1
          : d0;
        // helperText.text(legendFormat(new Date(d.date)) + ' - Close: ' + d.close);
        priceTooltip.attr('transform', 'translate(' + x(d.date) + ',' + y(d.close) + ')');
        pricetipText.attr('transform', 'translate(' + x(d.date) + ',' + y(d.close) + ')')
          .attr('x', -195)
          .attr('dy', -20)
          .style('fill', '#E8336D')
          .style('font-size', '14px')
          .text(legendFormat(new Date(d.date)) + "__$" + d.close);
        pricetipLineX.attr('transform', 'translate(' + x(d.date) + ',' + y(d.close) + ')')
          .attr('x1', 0)
          .attr('x2', -x(d.date))
          .attr('y1', 0)
          .attr('y2', 0);

        pricetipLineY.attr('transform', 'translate(' + x(d.date) + ',' + y(d.close) + ')')
          .attr('x1', 0)
          .attr('x2', 0)
          .attr('y1', 0)
          .attr('y2', height - y(d.close));
      }
      // //////////////////////////////////////////////////////////////////////// Add
      // annotations info mark_list Data <- from html
      var annotations = mark_list.map(l => {
        l.note = Object.assign({}, l.note, {
          title: `Close: ${l.data.close}`,
          label: `${l.data.date}`
        })
        l.subject = {
          radius: 10
        }

        return l
      })

      function check_type() {
        if (mark_list.length > 10) {
          let type = d3.annotationBadge;
          return type;
        } else {
          if (seg_width < 601) {
            let type = d3.annotationBadge;
            return type;
          } else {
            // Set Annotation type.
            let type = d3.annotationCustomType(d3.annotationXYThreshold, {
              "className": "custom",
              "connector": {
                "end": "dot"
              },
              "note": {
                "lineType": "vertical",
                "align": "dynamic"
              }
            })
            return type;
          }
        }
      }

      let type = check_type();
      // Make Annotations
      window.makeAnnotations = d3
        .annotation()
        .annotations(annotations)
        .type(type)
        .accessors({
          x: d => x(parseTime(d.date)),
          y: d => y(d.close)
        })
        .accessorsInverse({
          date: d => timeFormat(x.invert(d.x)),
          close: d => y.invert(d.y)
        })
        .on('subjectover', function (annotation) {
          annotation
            .type
            .a
            .selectAll("g.annotation-connector, g.annotation-note")
            .classed("hidden", false)
        })
        .on('subjectout', function (annotation) {
          annotation
            .type
            .a
            .selectAll("g.annotation-connector, g.annotation-note")
            .classed("hidden", false)
        })
      // Add annotation in focus
      svg
        .append("g")
        .attr("class", "annotation-test")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .call(makeAnnotations)
      // Set default annotation-connector and annogtation-note as hidden
      svg
        .selectAll("g.annotation-connector, g.annotation-note")
        .classed("hidden", false)

      //////////////////////////////////////////////////////////////////////////////
    })
}
