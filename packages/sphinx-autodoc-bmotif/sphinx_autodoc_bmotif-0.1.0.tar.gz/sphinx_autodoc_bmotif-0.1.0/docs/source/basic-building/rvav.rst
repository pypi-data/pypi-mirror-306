
rvav
####

.. code-block:: turtle

    @prefix brick: <https://brickschema.org/schema/Brick#> .
    @prefix ns1: <urn:___param___#> .
    
    ns1:name a brick:Variable_Air_Volume_Box_With_Reheat ;
        brick:hasPart ns1:heating_coil .
    
    

Parameters
----------

- name
- heating_coil

Dependencies
------------

- :doc:`vav`
- :doc:`heating-coil`


Backlinks
---------

No templates depend on this template.

Graphviz
--------

.. graphviz::

        digraph G {
    node [fontname="DejaVu Sans"];
    node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
    node0 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPart</font> >];
    node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
    node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Variable_Air_Volume_Box_With_Reheat</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Variable_Air_Volume_Box_With_Reheat' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Variable_Air_Volume_Box_With_Reheat</font></td></tr></table> >];
    node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>heating_coil</B></td></tr><tr><td href='urn:___param___#heating_coil' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#heating_coil</font></td></tr></table> >];
    }
    

.. collapse:: Template With Inline Dependencies

    .. graphviz::

                digraph G {
        node [fontname="DejaVu Sans"];
        node0 -> node1 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node2 -> node3 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node4 -> node5 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node6 -> node2 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:feeds</font> >];
        node6 -> node7 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPart</font> >];
        node7 -> node8 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node9 -> node10 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node11 -> node12 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasUnit</font> >];
        node6 -> node13 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node6 -> node0 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPart</font> >];
        node0 -> node4 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPart</font> >];
        node6 -> node14 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node6 -> node15 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node11 -> node16 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasValue</font> >];
        node6 -> node9 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node7 -> node17 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node17 -> node18 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node2 -> node11 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:area</font> >];
        node19 -> node20 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node15 -> node21 [color=BLACK, label=< <font point-size='10' color='#336633'>rdf:type</font> >];
        node6 -> node19 [color=BLACK, label=< <font point-size='10' color='#336633'>brick:hasPoint</font> >];
        node0 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>heating_coil</B></td></tr><tr><td href='urn:___param___#heating_coil' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#heating_coil</font></td></tr></table> >];
        node1 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Heating_Coil</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Heating_Coil' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Heating_Coil</font></td></tr></table> >];
        node2 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-zone</B></td></tr><tr><td href='urn:___param___#name-zone' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-zone</font></td></tr></table> >];
        node3 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>HVAC_Zone</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#HVAC_Zone' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#HVAC_Zone</font></td></tr></table> >];
        node4 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>heating_coil-valve_command</B></td></tr><tr><td href='urn:___param___#heating_coil-valve_command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#heating_coil-valve_command</font></td></tr></table> >];
        node5 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Valve_Command</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Valve_Command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Valve_Command</font></td></tr></table> >];
        node6 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name</B></td></tr><tr><td href='urn:___param___#name' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name</font></td></tr></table> >];
        node7 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-damper</B></td></tr><tr><td href='urn:___param___#name-damper' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-damper</font></td></tr></table> >];
        node8 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Supply_Damper</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Supply_Damper' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Supply_Damper</font></td></tr></table> >];
        node9 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-supply_air_temp</B></td></tr><tr><td href='urn:___param___#name-supply_air_temp' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-supply_air_temp</font></td></tr></table> >];
        node10 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Supply_Air_Temperature_Sensor</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Supply_Air_Temperature_Sensor' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Supply_Air_Temperature_Sensor</font></td></tr></table> >];
        node11 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-zone-area</B></td></tr><tr><td href='urn:___param___#name-zone-area' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-zone-area</font></td></tr></table> >];
        node12 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>FT2</B></td></tr><tr><td href='http://qudt.org/vocab/unit#FT2' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>http://qudt.org/vocab/unit#FT2</font></td></tr></table> >];
        node13 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Variable_Air_Volume_Box_With_Reheat</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Variable_Air_Volume_Box_With_Reheat' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Variable_Air_Volume_Box_With_Reheat</font></td></tr></table> >];
        node14 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Variable_Air_Volume_Box</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Variable_Air_Volume_Box' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Variable_Air_Volume_Box</font></td></tr></table> >];
        node15 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-supply_air_flow</B></td></tr><tr><td href='urn:___param___#name-supply_air_flow' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-supply_air_flow</font></td></tr></table> >];
        node16 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-zone-area-value</B></td></tr><tr><td href='urn:___param___#name-zone-area-value' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-zone-area-value</font></td></tr></table> >];
        node17 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-damper-position</B></td></tr><tr><td href='urn:___param___#name-damper-position' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-damper-position</font></td></tr></table> >];
        node18 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Damper_Position_Command</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Damper_Position_Command' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Damper_Position_Command</font></td></tr></table> >];
        node19 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>name-supply_air_temp_sp</B></td></tr><tr><td href='urn:___param___#name-supply_air_temp_sp' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>urn:___param___#name-supply_air_temp_sp</font></td></tr></table> >];
        node20 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Supply_Air_Temperature_Setpoint</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Supply_Air_Temperature_Setpoint' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Supply_Air_Temperature_Setpoint</font></td></tr></table> >];
        node21 [shape=none, color=black, label=< <table color='#666666' cellborder='0' cellspacing='0' border='1'><tr><td colspan='2' bgcolor='grey'><B>Supply_Air_Flow_Sensor</B></td></tr><tr><td href='https://brickschema.org/schema/Brick#Supply_Air_Flow_Sensor' bgcolor='#eeeeee' colspan='2'><font point-size='10' color='#6666ff'>https://brickschema.org/schema/Brick#Supply_Air_Flow_Sensor</font></td></tr></table> >];
        }
        
