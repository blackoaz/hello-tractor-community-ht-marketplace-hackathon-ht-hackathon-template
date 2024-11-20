console.log('Hello from main.js');
document.addEventListener('DOMContentLoaded', () => {
    const deals = document.querySelectorAll('.deal');
  
    deals.forEach(deal => {
      deal.addEventListener('click', () => {
        const url = deal.getAttribute('data-url');
        if (url) {
          window.location.href = url;
        }
      });
    });
  });
  

