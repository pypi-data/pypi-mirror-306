
heating-coil
############

.. code-block:: turtle

    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix ns1: <urn:___param___#> .
    
    ns1:name a brick:Heating_Coil ;
        brick:hasPart ns1:valve_command .
    
    

Parameters
----------

- valve_command
- name

Dependencies
------------

- `https://brickschema.org/schema/Brick#Valve_Command <https://ontology.brickschema.org/brick/Valve_Command.html>`_


Backlinks
---------

- :doc:`rvav`

Graphviz
--------

.. graphviz::

        digraph G {
    node [fontname="DejaVu Sans"];
    node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
    node0 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPart</font> >];
    node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
    node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Heating_Coil</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Heating_Coil' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Heating_Coil</font></td></tr></table> >];
    node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>valve_command</B></td></tr><tr><td href='urn:___param___#valve_command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#valve_command</font></td></tr></table> >];
    }
    

.. collapse:: Template With Inline Dependencies

    .. graphviz::

                digraph G {
        node [fontname="DejaVu Sans"];
        node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPart</font> >];
        node0 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node1 -> node3 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
        node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>valve_command</B></td></tr><tr><td href='urn:___param___#valve_command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#valve_command</font></td></tr></table> >];
        node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Heating_Coil</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Heating_Coil' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Heating_Coil</font></td></tr></table> >];
        node3 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Valve_Command</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Valve_Command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Valve_Command</font></td></tr></table> >];
        }
        
