// Honestly this might just do nothing but I feel like it helps lmao
window.addEventListener("DOMContentLoaded", function() {
const linkToImage = document.querySelector("a.rackCall");

linkToImage.addEventListener("mouseover", preloadImages, true);
linkToImage.myParam = ["/static/fullFrontalRack.JPG"]

function preloadImages(eventImade) {
    if (!preloadImages.list) {
        preloadImages.list = [];


    }

    var list = preloadImages.list;
  console.log(list)
    for (var i = 0; i < eventImade.currentTarget.myParam.length; i++) {

        var img = new Image();
      console.log(img)
        img.onload = function() {
            var index = list.indexOf(this);
            if (index !== -1) {
                list.splice(index, 1);
            }
        }
        list.push(img);
        img.src = eventImade.currentTarget.myParam[i];
    }
}
}, {once : true});
