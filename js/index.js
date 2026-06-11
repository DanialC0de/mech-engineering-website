let aboutLink = document.querySelector('.nav-links a:nth-child(2)');
let aboutUl= document.getElementById('ul-about');

aboutLink.addEventListener('mouseover', function() {
    aboutUl.classList.add('show');
});
aboutLink.addEventListener('mouseout', function() {
    aboutUl.classList.remove("show");
});

aboutUl.addEventListener('mouseover', function() {
    aboutUl.classList.add('show');
});
aboutUl.addEventListener('mouseout', function() {
    aboutUl.classList.remove("show");
});



let relationLink = document.querySelector('.nav-links a:nth-child(3)');
let relationUl= document.getElementById('ul-relation');

relationLink.addEventListener('mouseover', function() {
    relationUl.classList.add('show');
});
relationLink.addEventListener('mouseout', function() {
    relationUl.classList.remove("show");
});

relationUl.addEventListener('mouseover', function() {
    relationUl.classList.add('show');
});
relationUl.addEventListener('mouseout', function() {
    relationUl.classList.remove("show");
});
