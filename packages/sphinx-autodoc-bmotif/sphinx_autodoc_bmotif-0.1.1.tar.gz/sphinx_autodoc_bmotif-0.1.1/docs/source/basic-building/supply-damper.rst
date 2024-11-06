
supply-damper
#############

.. code-block:: turtle

    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix ns1: <urn:___param___#> .
    
    ns1:name a brick:Supply_Damper ;
        brick:hasPoint ns1:position .
    
    

Parameters
----------

- position
- name

Dependencies
------------

- `https://brickschema.org/schema/Brick#Damper_Position_Command <https://ontology.brickschema.org/brick/Damper_Position_Command.html>`_


Backlinks
---------

- :doc:`vav`

Graphviz
--------

.. graphviz::

        digraph G {
    node [fontname="DejaVu Sans"];
    node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
    node0 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
    node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
    node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Supply_Damper</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Supply_Damper' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Supply_Damper</font></td></tr></table> >];
    node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>position</B></td></tr><tr><td href='urn:___param___#position' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#position</font></td></tr></table> >];
    }
    

.. collapse:: Template With Inline Dependencies

    .. graphviz::

                digraph G {
        node [fontname="DejaVu Sans"];
        node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node2 -> node0 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node2 -> node3 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>position</B></td></tr><tr><td href='urn:___param___#position' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#position</font></td></tr></table> >];
        node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Damper_Position_Command</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Damper_Position_Command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Damper_Position_Command</font></td></tr></table> >];
        node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
        node3 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Supply_Damper</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Supply_Damper' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Supply_Damper</font></td></tr></table> >];
        }
        
