console.log('Another Hello from main.js');

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

  // admin dashboard
  document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.querySelector('.toggle-sidebar-btn');
    const sidebar = document.querySelector('.sidebar');

    if (toggleButton && sidebar) {
        toggleButton.addEventListener('click', () => {
            sidebar.classList.toggle('visible');
        });
    }
});

// filtered search script
    const priceInput = document.getElementById('price');
    const priceValue = document.getElementById('price-value');
    let yearVal = document.getElementById('year')
    let startYear = 2000;
    let endYear = new Date().getFullYear();
    console.log(startYear)

    for (let i = endYear; i >= startYear; i--) {
      const option = document.createElement('option');
      option.value = i;
      option.textContent = i;
      yearVal.appendChild(option);
    }

    priceInput.addEventListener('input', (e) => {
    const value = e.target.value;
    priceValue.textContent = `KSH 0 - ${parseInt(value).toLocaleString()}`;
});

    
  

