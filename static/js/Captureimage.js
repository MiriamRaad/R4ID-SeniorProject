let currentIndex = 0;
var imagesurls = null ;
document.addEventListener('DOMContentLoaded', function() {
    imagesurls = document.getElementById('myData').dataset.djangoVariable;
    imagesurls = imagesurls.substring(1, imagesurls.length - 1).split(', ');
});

function showImage(index) {
         var imageContainer = document.getElementById('cloudinaryImage');
         var imageUrl = imagesurls[index];
         imageUrl = imageUrl.slice(1, -1)
         imageContainer.src = imageUrl;}

function nextImage() {
         console.log(imagesurls);
         currentIndex = (currentIndex + 1) % imagesurls.length;
         console.log(currentIndex);
         showImage(currentIndex);}

function previousImage() {
         currentIndex = (currentIndex - 1 + imagesurls.length) % imagesurls.length;
         showImage(currentIndex);}