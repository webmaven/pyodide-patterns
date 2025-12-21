document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('container');
  if (container) {
    const p = document.createElement('p');
    p.id = 'loaded-message';
    p.textContent = 'Script loaded successfully!';
    container.appendChild(p);
  }
});
