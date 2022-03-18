from gcode_machine import GcodeMachine

# initial conditions
initial_machine_position = impos = (0,0,0)
initial_coordinate_system = ics = "G54"
coordinate_system_offsets = cs_offsets = {"G54":(0,0,0)}


def zcorr(pos):
    print(pos)
    return 10.0


# make a new machine
gcm = GcodeMachine(impos, ics, cs_offsets)
gcm.z_corection_callback = zcorr
input = ["G0 Z-10", "G1 X10 Y10"]
output = []

for line in input:
    gcm.set_line(line)       # feed the line into the machine
    gcm.strip()              # clean up whitespace
    gcm.tidy()               # filter commands by a whitelist
    gcm.find_vars()          # parse variable usages
    gcm.substitute_vars()    # substitute variables
    gcm.parse_state()        # parse positions etc. and update the machine state
    gcm.override_feed()      # substitute F values
    gcm.transform_comments() # transform parentheses to semicolon comments
    print(gcm.line)  # read the processed line back from the machine
    print(gcm.z_corrected_line())
    gcm.done()               # update the machine position