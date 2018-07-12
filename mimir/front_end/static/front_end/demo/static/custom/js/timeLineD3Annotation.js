// line chart code: https://bl.ocks.org/d3noob/402dd382a51a4f6eea487f9a35566de0
    // time series from: http://bl.ocks.org/mbostock/3883245
    // set the dimensions and margins of the graph

// Set Margin
// seg_width from html
function d3PriceLinefunction() {
  const margin = {top: 20, right: 40, bottom: 30, left: 40},
        height = 500 - margin.top - margin.bottom;
  const margin2  = {top: 210, right: 20, bottom: 20, left: 50};
  let width = seg_width -50- margin.left - margin.right;

  // parseTime func  [2010-07-18 %Y-%m-%d]  [14-Oct-08 %d-%b-%y]
  const parseTime = d3.timeParse("%Y-%m-%d");
  const timeFormat = d3.timeFormat("%Y-%m-%d");

  // Set x, y scale-range
  const x = d3.scaleTime().range([0, width]);
  const y = d3.scaleLinear().range([height, 0]);

  // Create valueline based on data, close
  const valueline = d3.line()
      .x(d => x(d.date))   //x(function (d) {return x(d.date)
      .y(d => y(d.close)); //y(function (d) {return y(d.close)
      
  // svg initial set , Add 'g' at svg place setting. 
  const svg = d3.select("svg") 
      .attr("class", "lineChart")
      .attr("width", 960)
      .attr("height", height + margin.top + margin.bottom)

  // 遮色片：用於裁剪
  svg.append('defs').append('clipPath')
    .attr('id', 'clip')
      .append('rect')
      .attr('width', width)
      .attr('height', height);

  // focus:主資訊區
  const focus = svg.append("g")
      .attr('class', 'focus')
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  // legend: 上方Title位置區
  const legend = svg.append("g")
      .attr('class', 'chart_legend')
      .attr('width', width)
      .attr('height', 30)
      .attr('transform', 'translate(' + margin2.left + ', 10)');

  // legeng's Title: 
  legend.append('text')
      .attr('class', 'chart__symbol')
      .text('BTC')

  // lngend's chart_range-selection
  var rangeSelection =  legend
      .append('g')
      .attr('class', 'chart_range-selection')
      .attr('transform', 'translate(110, 0)');

  // context: 下方調整用來放bar位置
  var context = svg.append('g')
  .attr('class', 'context')
  .attr('transform', 'translate(' + margin2.left + ',' + (margin2.top + 360) + ')');


  // Read data and main func.
  d3.tsv(btc_tsv_data, function(error, data) {
    if (error) throw error;
    // use forEach func to get every data with func(d)
    data.forEach(function(d) {
      d.date = parseTime(d.Datee);
      d.close = +d.Close;
    });

    // Set domain range
    x.domain(d3.extent(data, d => d.date));
    y.domain([0, d3.max(data, d => d.close)]);

    // Add path-valueline at svg
    focus.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", valueline);

    // Add g to show x-axis
    focus.append("g")
      .attr("class", "x-axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    // Add g to show y
    focus.append("g")
      .attr("class", "y-axis")
      .call(d3.axisLeft(y));

    //////////////////////////////////////////////////////////////////////////
    // Add annotations info
    // mark_list Data <- from html 
    const annotations = mark_list.map(l => {
      l.note = Object.assign({}, 
                            l.note, 
                            { title: `Close: ${l.data.close}`,
                              label: `${l.data.date}`
                            })
      l.subject = { radius: 10 }

      return l
    })

    // Set Annotation type.
    const type = d3.annotationCalloutCircle;
    // Make Annotations 
    window.makeAnnotations = d3.annotation()
      .annotations(annotations)
      .type(type)
      .accessors({ x: d => x(parseTime(d.date)), 
                  y: d => y(d.close)
      })
      .accessorsInverse({
        date: d => timeFormat(x.invert(d.x)),
        close: d => y.invert(d.y) 
      })
      .on('subjectover', function(annotation) {
        annotation.type.a.selectAll("g.annotation-connector, g.annotation-note")
          .classed("hidden", true)
      })
      .on('subjectout', function(annotation) {
        annotation.type.a.selectAll("g.annotation-connector, g.annotation-note")
          .classed("hidden", true)
      })
    // Add annotation in focus
    focus.append("g")
      .attr("class", "annotation-test")
      .call(makeAnnotations)
    // Set default annotation-connector and annogtation-note as hidden
    focus.selectAll("g.annotation-connector, g.annotation-note")
      .classed("hidden", true)

    //////////////////////////////////////////////////////////////////////////////
  })
}