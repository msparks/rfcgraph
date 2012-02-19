# rfcgraph

rfcgraph is a simple Python script that uses Graphviz to generate a very large
graph showing the relations between RFCs.

![rfcgraph full](http://farm8.staticflickr.com/7184/6900099151_117c14f616.jpg)

![rfcgraph zoom](http://farm8.staticflickr.com/7057/6900099197_61bb710c80.jpg)

Green arrows indicate an update:

* "RFCx <span style="color:green">&rarr;</span> RFCy" is read as "RFCx is
updated by RFCy".

Red arrows indicate an obsoletion:

* "RFCx <span style="color:red">&rarr;</span> RFCy" is read as "RFCx is
obsoleted by RFCy".

## Dependencies

* [Python](http://www.python.org)
* [Graphviz](http://www.graphviz.org)
* [pydot](http://dkbza.org/pydot.html)

## Running

To run rfcgraph, you'll need to get a copy of the RFC index XML file
`rfc-index.xml` from [rfc-editor.org](http://rfc-editor.org/getbulk.html). Then run:

    ./rfcgraph.py -h

to see the usage.

Note that rfcgraph and graphviz are very memory intensive. On the order of
2-2.5GB of RAM is needed to generate the full graph.
