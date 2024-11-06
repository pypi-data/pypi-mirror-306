
thermostat
##########

.. code-block:: turtle

    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix ns1: <urn:___param___#> .
    
    ns1:name a brick:Thermostat_Equipment ;
        brick:hasLocation ns1:zone ;
        brick:hasPoint ns1:command,
            ns1:occ,
            ns1:sen,
            ns1:sp,
            ns1:status .
    
    

Parameters
----------

- status
- zone
- sen
- name
- occ
- sp
- command

Dependencies
------------

- `https://brickschema.org/schema/Brick#Mode_Status <https://ontology.brickschema.org/brick/Mode_Status.html>`_
- `https://brickschema.org/schema/Brick#Occupancy_Sensor <https://ontology.brickschema.org/brick/Occupancy_Sensor.html>`_
- `https://brickschema.org/schema/Brick#Mode_Command <https://ontology.brickschema.org/brick/Mode_Command.html>`_
- `https://brickschema.org/schema/Brick#Air_Temperature_Setpoint <https://ontology.brickschema.org/brick/Air_Temperature_Setpoint.html>`_
- `https://brickschema.org/schema/Brick#Air_Temperature_Sensor <https://ontology.brickschema.org/brick/Air_Temperature_Sensor.html>`_
- :doc:`hvac-zone`


Backlinks
---------

No templates depend on this template.

Graphviz
--------

.. graphviz::

        digraph G {
    node [fontname="DejaVu Sans"];
    node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
    node0 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasLocation</font> >];
    node0 -> node3 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
    node0 -> node4 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
    node0 -> node5 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
    node0 -> node6 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
    node0 -> node7 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
    node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
    node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Thermostat_Equipment</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Thermostat_Equipment' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Thermostat_Equipment</font></td></tr></table> >];
    node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>zone</B></td></tr><tr><td href='urn:___param___#zone' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#zone</font></td></tr></table> >];
    node3 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>sen</B></td></tr><tr><td href='urn:___param___#sen' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#sen</font></td></tr></table> >];
    node4 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>sp</B></td></tr><tr><td href='urn:___param___#sp' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#sp</font></td></tr></table> >];
    node5 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>occ</B></td></tr><tr><td href='urn:___param___#occ' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#occ</font></td></tr></table> >];
    node6 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>command</B></td></tr><tr><td href='urn:___param___#command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#command</font></td></tr></table> >];
    node7 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>status</B></td></tr><tr><td href='urn:___param___#status' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#status</font></td></tr></table> >];
    }
    

.. collapse:: Template With Inline Dependencies

    .. graphviz::

                digraph G {
        node [fontname="DejaVu Sans"];
        node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node0 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node3 -> node4 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node5 -> node6 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node7 -> node8 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasValue</font> >];
        node9 -> node10 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node0 -> node11 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node7 -> node12 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasUnit</font> >];
        node9 -> node7 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:area</font> >];
        node1 -> node13 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node0 -> node14 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node0 -> node9 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasLocation</font> >];
        node0 -> node3 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node0 -> node5 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node2 -> node15 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node11 -> node16 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
        node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>occ</B></td></tr><tr><td href='urn:___param___#occ' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#occ</font></td></tr></table> >];
        node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>status</B></td></tr><tr><td href='urn:___param___#status' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#status</font></td></tr></table> >];
        node3 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>sen</B></td></tr><tr><td href='urn:___param___#sen' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#sen</font></td></tr></table> >];
        node4 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Air_Temperature_Sensor</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Air_Temperature_Sensor' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Air_Temperature_Sensor</font></td></tr></table> >];
        node5 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>sp</B></td></tr><tr><td href='urn:___param___#sp' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#sp</font></td></tr></table> >];
        node6 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Air_Temperature_Setpoint</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Air_Temperature_Setpoint' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Air_Temperature_Setpoint</font></td></tr></table> >];
        node7 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>zone-area</B></td></tr><tr><td href='urn:___param___#zone-area' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#zone-area</font></td></tr></table> >];
        node8 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>zone-area-value</B></td></tr><tr><td href='urn:___param___#zone-area-value' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#zone-area-value</font></td></tr></table> >];
        node9 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>zone</B></td></tr><tr><td href='urn:___param___#zone' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#zone</font></td></tr></table> >];
        node10 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>HVAC_Zone</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#HVAC_Zone' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#HVAC_Zone</font></td></tr></table> >];
        node11 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>command</B></td></tr><tr><td href='urn:___param___#command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#command</font></td></tr></table> >];
        node12 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>FT2</B></td></tr><tr><td href='http://qudt.org/vocab/unit#FT2' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>http://qudt.org/vocab/unit#FT2</font></td></tr></table> >];
        node13 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Occupancy_Sensor</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Occupancy_Sensor' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Occupancy_Sensor</font></td></tr></table> >];
        node14 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Thermostat_Equipment</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Thermostat_Equipment' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Thermostat_Equipment</font></td></tr></table> >];
        node15 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Mode_Status</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Mode_Status' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Mode_Status</font></td></tr></table> >];
        node16 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Mode_Command</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Mode_Command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Mode_Command</font></td></tr></table> >];
        }
        
