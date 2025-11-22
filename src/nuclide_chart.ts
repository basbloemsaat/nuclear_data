
import * as d3 from 'd3';
import './index.css';


interface Isotope {
  Z: number;
  A: number;
  Symbol: string;
  Element_Name: string;
}


// Make chart full screen
const width = window.innerWidth;
const height = window.innerHeight;
const margin = { top: 40, right: 40, bottom: 60, left: 60 };


const mount = document.getElementById('nuclide-chart-mount');
if (mount) {
  // Remove previous chart if any
  mount.innerHTML = '';
  mount.style.width = '100vw';
  mount.style.height = '100vh';
  mount.style.position = 'fixed';
  mount.style.top = '0';
  mount.style.left = '0';
  mount.style.margin = '0';
  mount.style.padding = '0';
  mount.style.zIndex = '0';
  mount.style.background = '#fafafa';


  fetch('/data/isotopes.json')
    .then(res => res.json())
    .then(json => {
      const data: Isotope[] = json.isotopes;

      // N = A - Z
      const xMin = Math.max(0, d3.min(data, d => d.A - d.Z)! - 1);
      const xMax = d3.max(data, d => d.A - d.Z)! + 1;
      const yMin = Math.max(0, d3.min(data, d => d.Z)! - 1);
      const yMax = d3.max(data, d => d.Z)! + 1;

      const x = d3.scaleLinear()
        .domain([xMin, xMax])
        .range([margin.left, width - margin.right]);
      const y = d3.scaleLinear()
        .domain([yMin, yMax])
        .range([height - margin.bottom, margin.top]);

      const svg = d3.select(mount)
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .style('display', 'block')
        .style('width', '100vw')
        .style('height', '100vh')
        .style('border', 'none')
        .style('background', '#fafafa');

      // X Axis
      svg.append('g')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x).ticks(12).tickFormat(d3.format('d')))
        .call(g => g.select('.domain').attr('stroke', '#333').attr('stroke-width', 2))
        .call(g => g.selectAll('.tick line').attr('stroke', '#333'))
        .call(g => g.selectAll('.tick text').attr('fill', '#222').attr('font-size', '1.1rem'))
        .append('text')
        .attr('x', width - margin.right)
        .attr('y', -10)
        .attr('fill', '#000')
        .attr('text-anchor', 'end')
        .attr('font-size', '1.5rem')
        .text('Neutrons (N)');

      // Y Axis
      svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y).ticks(12).tickFormat(d3.format('d')))
        .call(g => g.select('.domain').attr('stroke', '#333').attr('stroke-width', 2))
        .call(g => g.selectAll('.tick line').attr('stroke', '#333'))
        .call(g => g.selectAll('.tick text').attr('fill', '#222').attr('font-size', '1.1rem'))
        .append('text')
        .attr('x', 10)
        .attr('y', margin.top)
        .attr('fill', '#000')
        .attr('text-anchor', 'start')
        .attr('font-size', '1.5rem')
        .text('Protons (Z)');

      // Points
      svg.selectAll('circle')
        .data(data)
        .enter()
        .append('circle')
        .attr('cx', d => x(d.A - d.Z))
        .attr('cy', d => y(d.Z))
        .attr('r', 6)
        .attr('fill', '#69b3a2')
        .attr('stroke', '#333')
        .append('title')
        .text(d => `${d.Symbol}-${d.A} (${d.Element_Name})`);
    });
}
