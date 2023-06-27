FILAMENT_NAME = "pla"
BUILD_PLATE_TEMPERATURE = 50
HOTEND_TEMPERATURE = 200

Z_HOP_HEIGHT = 0.75
LAYER_HEIGHT = 0.26
RETRACTION_DISTANCE = 1
FILAMENT_DIAMETER = 1.75
NOZZLE_DIAMETER = .6
LINE_WIDTH = 0.8 # May need adjustment. 

number_off_test = 20
test_increment = .05
PA_START_VALUE = 0.03
PA_STOP_VALUE = (number_off_test * test_increment)+PA_START_VALUE
start_x = 50
start_y = 50
line_length = 30
spacing = 3




bounding_box_height = (number_off_test+1) * spacing
EXTRUSION_DISTANCE_PER_MM = ((1*LAYER_HEIGHT*LINE_WIDTH)/((3.1416*(FILAMENT_DIAMETER**2))/4))
FINISHED_X = 0
FINISHED_Y = bounding_box_height + start_y
print(';EXTRUSION DISTANCE '+ str(EXTRUSION_DISTANCE_PER_MM))
print(';bounding box height '+ str(bounding_box_height))

f = open("PA_CALIBRATION_"+ FILAMENT_NAME + ".gcode" , "w")

f.write(
        "\n"
        "G21 ; Millimeter units""\n"
        "G90 ; Absolute XYZ""\n"
        "M83 ; Relative E""\n"
        "M104 S" + str(HOTEND_TEMPERATURE) +  "; set extruder temp""\n"
        "M140 S" + str(BUILD_PLATE_TEMPERATURE) + " ; set bed temp""\n"
        "M109 S" + str(HOTEND_TEMPERATURE) + " ; wait for extruder temp""\n"
        "M190 S" + str(BUILD_PLATE_TEMPERATURE) + " ; wait for bed temp""\n"
        "G28  ; home all ""\n"
        "SET_VELOCITY_LIMIT ACCEL=3000 ACCEL_TO_DECEL=1500""\n"
        "\n"

        "G90""\n"
        "G92 E0""\n"
        "G1 Z0.2 F720""\n"
        "G1 Y5 F1000 ; go outside print area""\n"
        "G92 E0""\n"
        "G1 X60 E9 F1000 ; intro line""\n"
        "G1 X100 E12.5 F1000 ; intro line""\n"
        "G92 E0""\n"
        "\n"

        "G92 E0 ;""\n"
        "M106 S0 ; set fan speed to 0""\n"

        "G1 X" + str(start_x + line_length + LINE_WIDTH*2) + " Y" + str(start_y - spacing - LINE_WIDTH*2) + " F30000 ; move to start position""\n"
        "G1 Z" + str(LAYER_HEIGHT) + " F300 ; move to layer height""\n"
        "G91 ; switch to relative movements""\n"
    
        "; Print a bounding box to aid with removal and prime the extruder.""\n"
        "G1 E" + str(RETRACTION_DISTANCE) + "\n"
        "G1 Y" + str(bounding_box_height + LINE_WIDTH*2) + ' E' + str((bounding_box_height) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 ' "\n"
        "G1 X-" + str(line_length + LINE_WIDTH*2) + ' E' + str((line_length) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 '"\n"
        "G1 Y-" + str(bounding_box_height + LINE_WIDTH*2) + ' E' + str((bounding_box_height) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 '"\n"
        "G1 X" + str(line_length + LINE_WIDTH*2) + ' E' + str((line_length) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 '"\n"
        "G1 X" + str(-LINE_WIDTH) + " Y" + str(LINE_WIDTH) + "\n"
        "; second bounding box loop""\n"
        "G1 Y" + str(bounding_box_height) + ' E' + str((bounding_box_height) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 '"\n"
        "G1 X" + str(-line_length) + ' E' + str((line_length) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 '"\n"
        "G1 Y" + str(-bounding_box_height) + ' E' + str((bounding_box_height) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 '"\n"
        "G1 X" + str(line_length) + ' E' + str((line_length) * EXTRUSION_DISTANCE_PER_MM) + ' F3000 '"\n"

        "G1 Z" + str(Z_HOP_HEIGHT) + " E" + str(-RETRACTION_DISTANCE) + " F300; retract and prepare to hop to first line location."
        "\n"  
)

    
while PA_START_VALUE < PA_STOP_VALUE :   
        f.write(        
        
                "\n"
                "SET_PRESSURE_ADVANCE = " + str(PA_START_VALUE) + " ; set Pressure Advance""\n"
                
                'M117 Testing Pressure Advance at: ' + str(PA_START_VALUE) + "\n"
                'G1 X-' + str(line_length) + ' Y' + str(spacing) + ' F30000        ; move to start position'"\n"
                'G1 Z' + str(-Z_HOP_HEIGHT) + ' F300           ; move to layer height'"\n"
                'G1 E' + str(RETRACTION_DISTANCE) + ' F1800           ; un-retract'"\n"
                'G1 X' + str(line_length / 4) + ' E' + str((line_length / 4) * EXTRUSION_DISTANCE_PER_MM) + ' F300     ; print line part one'"\n"
                'G1 X' + str( line_length / 2) + ' E' + str((line_length / 2) * EXTRUSION_DISTANCE_PER_MM) + ' F4000    ; print line part two'"\n"
                'G1 X' + str(line_length / 4) + ' E' + str((line_length / 4) * EXTRUSION_DISTANCE_PER_MM) + ' F300     ; print line part three'"\n"
                'G1 E' + str(-RETRACTION_DISTANCE) + ' F1800          ; retract'"\n"
                'G1 Z' + str(Z_HOP_HEIGHT) + ' F300            ; Move above layer height' "\n"
        )
        PA_START_VALUE = PA_START_VALUE + test_increment

f.write('''
G4 ; wait
M104 S0 ; turn off temperature
M140 S0 ; turn off heatbed
M107 ; turn off fan
'''
"G1 Z" + str(Z_HOP_HEIGHT*2) + " E" + str(-RETRACTION_DISTANCE*1.5) + " F300; retract and get over the line.""\n"
"G90 ; Absolute XYZ""\n"
'G1 X5 Y' + str(FINISHED_Y) + ' F30000        ; move to end position'
'''
M84 ; disable motors
'''
)



f.close()
