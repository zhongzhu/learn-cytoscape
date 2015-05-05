$(function(){ // on dom ready

  $('#cy').cytoscape({
    style: cytoscape.stylesheet()
    .selector('node')
    .css({
      'content': 'data(name)',
      'text-valign': 'center',
      'color': 'white',
      'text-outline-width': 2,
      'text-outline-color': '#888'
    })
    .selector('edge')
      .css({
        'target-arrow-shape': 'triangle',
        'width': 4        
      })
    .selector(':selected')
      .css({
        'background-color': 'black',
        'line-color': 'black',
        'target-arrow-color': 'black',
        'source-arrow-color': 'black'
      })
    .selector('.faded')
      .css({
        'opacity': 0.25,
        'text-opacity': 0
      }),

    elements: {
      nodes: [
        { data: { id: 'j', name: 'Jerry' } },
        { data: { id: 'e', name: 'Elaine' } },
        { data: { id: 'k', name: 'Kramer' } },
        { data: { id: 'g', name: 'George' } }
      ],
      edges: [
        { data: { source: 'j', target: 'e' } },
        { data: { source: 'j', target: 'k' } },
        { data: { source: 'j', target: 'g' } },
        { data: { source: 'e', target: 'j' } },
        { data: { source: 'e', target: 'k' } },
        { data: { source: 'k', target: 'j' } },
        { data: { source: 'k', target: 'e' } },
        { data: { source: 'k', target: 'g' } },
        { data: { source: 'g', target: 'j' } }
      ]
    },

    layout: {
      name: 'circle',
      padding: 10
    },

    // on graph initial layout done (could be async depending on layout...)
    ready: function(){
      window.cy = this;

      // giddy up...

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
  });

}); // on dom ready