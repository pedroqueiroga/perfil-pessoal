let grafo = null;
let clickedNodes = [];
let hidingNodes = false;
let hideButton = null;
let slider = null;
let grafoMaxWidth;
let grafoMaxHeight;

window.onload = function() {
  grafo = document.getElementById('grafo');
  slider = document.getElementById('slider');
  hideButton = document.getElementById('hide');

  hideButton.addEventListener('click', event => {
    hidingNodes = !hidingNodes;
    triggerHide();
    if (hidingNodes) {
      hideButton.value = 'Mostrar arestas';
    } else {
      hideButton.value = 'Esconder arestas';
    }
  });
  const svg = grafo.getElementsByTagName('svg')[0];
  grafoMaxWidth = svg.getAttribute('width');
  grafoMaxHeight = svg.getAttribute('height');
  scaleGrafo(slider.value / 100);

  slider.oninput = function() {
    scaleGrafo(slider.value / 100);
  };


  // Get one of the SVG items by ID;
  const nodes = grafo.getElementsByClassName('node');

  for (const node of nodes) {
    // should only have one text
    const text = node.getElementsByTagName('text')[0];

    node.onclick = function(e) {
      console.log(this);
      if (clickedNodes.includes(this)) {
        clickedNodes.remove(this);
      } else {
        clickedNodes.push(this);
      }
    };

    node.onmouseover = function(e) {
      if (e.relatedTarget === text) {
        // from text inside node to node, visually the same
      } else {
        triggerHide();
        highlightEdges(this);
        highlightNode(this);
      }
    };
    node.onmouseout = function(e) {
      if (e.relatedTarget === text) {
        // from node to text inside node, visually still node
      } else if (!clickedNodes.includes(this)) {
        unHighlightEdges(this);
        unHighlightNode(this);
        triggerHide();
      }
    };

    // the following is useful to keep the text inside the nodes
    // from triggering these events
    text.onmouseout = function(e) {
      e.stopPropagation();
    };
    text.onmouseover = function(e) {
      e.stopPropagation();
    };
  }
};

function scaleGrafo(percentage) {
  const svg = grafo.getElementsByTagName('svg')[0];
  const newWidth = parseInt(grafoMaxWidth) * percentage;
  const newHeight = parseInt(grafoMaxHeight) * percentage;
  svg.setAttribute('width', newWidth);
  svg.setAttribute('height', newHeight);
}

function triggerHide() {
  if (!hidingNodes) {
    showUnclickedNodesEdges();
  } else {
    hideUnclickedNodesEdges();
  }
}

function hideUnclickedNodesEdges() {
  if (clickedNodes.length === 0) {
    hideAllEdges();
  } else {
    for (const node of clickedNodes) {
      hideOtherEdges(node);
    }
  }
}

function showUnclickedNodesEdges() {
  if (clickedNodes.length === 0) {
    showAllEdges();
  } else {
    for (const node of clickedNodes) {
      showOtherEdges(node);
    }
  }
}

function hideAllEdges() {
  const edges = grafo.getElementsByClassName('edge');
  for (const edge of edges) {
    hideEdge(edge);
  }
}

function showAllEdges() {
  const edges = grafo.getElementsByClassName('edge');
  for (const edge of edges) {
    showEdge(edge);
  }
}

function hideOtherEdges(node) {
  const edges = grafo.getElementsByClassName('edge');
  for (const edge of edges) {
    if (!isEdgeOfNode(node, edge)) {
      hideEdge(edge, true);
    }
  }
}

function showOtherEdges(node) {
  const edges = grafo.getElementsByClassName('edge');
  for (const edge of edges) {
    if (!isEdgeOfNode(node, edge)) {
      showEdge(edge);
    }
  }
}

function highlightEdges(node) {
  const edges = grafo.getElementsByClassName('edge');
  for (const edge of edges) {
    if (isEdgeOfNode(node, edge)) {
      highlightEdge(edge);
    }
  }
}

function unHighlightEdges(node) {
  const edges = grafo.getElementsByClassName('edge');
  for (const edge of edges) {
    if (!isEdgeOfClickedNodes(edge) && isEdgeOfNode(node, edge)) {
      unHighlightEdge(edge);
    }
  }
}

function isEdgeOfClickedNodes(edge) {
  for (const node of clickedNodes) {
    if (isEdgeOfNode(node, edge)) {
      return true;
    }
  }
  return false;
}

function hideEdge(edge, keepHighlit) {
  if (!keepHighlit || !isEdgeHighlit(edge)) {
    edge.setAttribute('visibility', 'hidden');
  }
}

function isEdgeHighlit(edge) {
  if (edge.getAttribute('stroke-width')) {
    return true;
  }
  return false;
}

function showEdge(edge) {
  edge.removeAttribute('visibility');
}

function highlightEdge(edge) {
  const highlightColor = 'purple';
  const highlightWidth = 5;
  const paths = edge.getElementsByTagName('path');
  const arrows = edge.getElementsByTagName('polygon');

  edge.setAttribute('stroke-width', highlightWidth);
  for (const path of paths) {
    path.setAttribute('stroke', highlightColor);
  }
  for (const arrow of arrows) {
    arrow.setAttribute('stroke', highlightColor);
    arrow.setAttribute('fill', highlightColor);
  }

  showEdge(edge);
}

function unHighlightEdge(edge) {
  const normalColor = 'black';
  const paths = edge.getElementsByTagName('path');
  const arrows = edge.getElementsByTagName('polygon');

  edge.removeAttribute('stroke-width');
  for (const path of paths) {
    path.setAttribute('stroke', normalColor);
  }
  for (const arrow of arrows) {
    arrow.setAttribute('stroke', normalColor);
    arrow.setAttribute('fill', normalColor);
  }

}

function highlightNode(node) {
  const highlightColor = 'mediumpurple';
  // should only have one ellipse
  const ellipse = node.getElementsByTagName('ellipse')[0];

  ellipse.setAttribute('fill', highlightColor);
}

function unHighlightNode(node) {
  const normalColor = 'lightgray';
  // should only have one ellipse
  const ellipse = node.getElementsByTagName('ellipse')[0];
  ellipse.setAttribute('fill', normalColor);
}

function isEdgeOfNode(node, edge) {
  const nodeTitle = node.getElementsByTagName('title')[0].textContent;
  const edgeTitle = edge.getElementsByTagName('title')[0].textContent;
  return edgeTitle.indexOf(nodeTitle) !== -1;
}

function isEdgeBidirectional(edge) {
  return edge.childNodes.length == 9;
}

Array.prototype.remove = function() {
  var what, a = arguments, L = a.length, ax;
  while (L && this.length) {
    what = a[--L];
    while ((ax = this.indexOf(what)) !== -1) {
      this.splice(ax, 1);
    }
  }
  return this;
};
