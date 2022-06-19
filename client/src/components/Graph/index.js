import "./styles.css";
import React, { useState, useRef, useEffect } from 'react'
import * as d3 from "d3";

function LineChart(props) {
    const [data] = useState([25, 50, 130, 115, 94, 10, 82, 74, 128, 100, 111, 64]);
    const svgRef = useRef();

    useEffect(() => {
        // setting up svg
        const w = 400;
        const h = 200;
        const svg = d3.select(svgRef.current)
            .attr('width', w)
            .attr('height', h)
            .style('overflow', 'visible');

        const xScale = d3.scaleLinear()
            .domain([0, data.length - 1])
            .range([0, 600]);
        const yScale = d3.scaleLinear()    
            .domain([0, 140])
            .range([h, 0]);
        const generateScaledLine = d3.line()
            .x((d, i) => xScale(i))
            .y(yScale);

        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        // setting up the axes
        const xAxis = d3.axisBottom(xScale)
            .tickFormat(i => months[i]);
        const yAxis = d3.axisLeft(yScale)
            .ticks(5)
        
        svg.append('g')
            .call(xAxis)
            .attr('transform', `translate(0, ${h})`)
        svg.append('g')
            .call(yAxis)


        // setting up the data for the svg
        svg.selectAll('.line')
            .data([data])
            .join('path')
                .attr('d', d => generateScaledLine(d))
                .attr('fill', 'none')
                .attr('stroke', 'steelblue');
    }, [data])

    return (
        <div>
            <div id="bar-graph"></div>
            <div id="line-graph">
                <svg ref={svgRef}></svg>
            </div>
        </div>
    )
}

export default LineChart