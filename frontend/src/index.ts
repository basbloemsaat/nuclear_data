
import './index.css';

const rootEl = document.querySelector('#root');
if (rootEl) {
  rootEl.innerHTML = `
  <div class="content">
    <h1>Vanilla Rsbuild</h1>
    <p>Start building amazing things with Rsbuild. x</p>
    <div id="nuclide-chart-mount"></div>
  </div>
`;
  // Import after DOM is ready
  import('./nuclide_chart');
}
