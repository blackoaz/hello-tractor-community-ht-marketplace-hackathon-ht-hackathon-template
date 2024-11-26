console.log('Vehicle details JavaScript loaded');

// JavaScript for handling image carousel
const images = JSON.parse('{{ images_json|escapejs }}'); 
let currentIndex = 0;

function showPreviousImage() {
    if (images.length > 0) {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        document.getElementById('current-image').src = images[currentIndex].url;
    }
}

function showNextImage() {
    if (images.length > 0) {
        currentIndex = (currentIndex + 1) % images.length;
        document.getElementById('current-image').src = images[currentIndex].url;
    }
}
