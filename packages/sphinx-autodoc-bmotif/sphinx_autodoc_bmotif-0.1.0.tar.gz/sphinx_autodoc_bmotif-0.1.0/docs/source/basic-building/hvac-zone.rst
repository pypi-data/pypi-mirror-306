
hvac-zone
#########

.. code-block:: turtle

    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix ns1: <urn:___param___#> .
    
    ns1:name a brick:HVAC_Zone ;
        brick:area ns1:area .
    
    

Parameters
----------

- name
- area

Dependencies
------------

- :doc:`floor-area`


Backlinks
---------

- :doc:`thermostat`
- :doc:`vav`

Graphviz
--------

.. graphviz::

        digraph G {
    node [fontname="DejaVu Sans"];
    node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
    node0 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:area</font> >];
    node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
    node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>HVAC_Zone</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#HVAC_Zone' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#HVAC_Zone</font></td></tr></table> >];
    node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>area</B></td></tr><tr><td href='urn:___param___#area' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#area</font></td></tr></table> >];
    }
    

.. collapse:: Template With Inline Dependencies

    .. graphviz::

                digraph G {
        node [fontname="DejaVu Sans"];
        node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasUnit</font> >];
        node2 -> node3 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node0 -> node4 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasValue</font> >];
        node2 -> node0 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:area</font> >];
        node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>area</B></td></tr><tr><td href='urn:___param___#area' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#area</font></td></tr></table> >];
        node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>FT2</B></td></tr><tr><td href='http://qudt.org/vocab/unit#FT2' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>http://qudt.org/vocab/unit#FT2</font></td></tr></table> >];
        node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
        node3 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>HVAC_Zone</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#HVAC_Zone' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#HVAC_Zone</font></td></tr></table> >];
        node4 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>area-value</B></td></tr><tr><td href='urn:___param___#area-value' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#area-value</font></td></tr></table> >];
        }
        
