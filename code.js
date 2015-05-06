$(function(){ // on dom ready

  // get the graph data and graph style
  var graphP = $.ajax({
    type: 'GET',
    url: 'http://localhost:8899/haha',
    dataType: 'jsonp'
  });

  Promise.all([graphP]).then(initMyGraph);

  function initMyGraph(then) {
    var elements = then[0].elements;
    var style = then[0].style;

    var cy = window.cy = cytoscape({
      textureOnViewport: true,
      pixelRatio: 1,
      motionBlur: true,

      container: document.getElementById('cy'),
      layout: { name: 'cose' },
      style: style,
      elements: elements,
      ready: onReady
    });    
  }

  // on graph initial layout done (could be async depending on layout...)
  function onReady() {
    cy.elements().unselectify();

    cy.on('tap', 'node', function(e){
      var node = e.cyTarget; 
      var neighborhood = node.neighborhood().add(node);

      cy.elements().addClass('faded');
      neighborhood.removeClass('faded');
    });

    cy.on('tap', function(e){
      if( e.cyTarget === cy ){
        cy.elements().removeClass('faded');
      }
    });
  }

}); // on dom ready