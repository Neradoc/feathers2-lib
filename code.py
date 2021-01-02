import time, gc, os
from feathers2 import fs2

# Make sure the 2nd LDO is turned on
fs2.enable_LDO2(True)

# use the DotStar instance
fs2.dot[0] = (0,100,100)

# Say hello
print("\nHello from FeatherS2!")
print("---------------------\n")

# Turn on the internal blue LED
fs2.blue_led = True

# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print("{} Bytes\n".format(gc.mem_free()))

flash = os.statvfs('/')
flash_size = flash[0] * flash[2]
flash_free = flash[0] * flash[3]
# Show flash size
print("Flash - os.statvfs('/')")
print("---------------------------")
print("Size: {} Bytes\nFree: {} Bytes\n".format(flash_size, flash_free))

print("Dotstar Time!\n")

# Create a colour wheel index int
color_index = 0
# Detect clicking boot
boot_down = False

# Rainbow colours on the Dotstar
while True:
    # Get the R,G,B values of the next colour
    r,g,b = fs2.wheel( color_index )
    # Set the colour on the dotstar
    fs2.dot[0] = ( r, g, b, 0.5)
    # Increase the wheel index
    color_index += 1
    
    # If the index == 255, loop it
    if color_index == 255:
        color_index = 0
    if color_index % 128 == 0:
        # Invert the internal LED state every half colour cycle
        fs2.blue_led = not fs2.blue_led
        # Read the ambient light sensor
        print("Ambient light: %.0f%%" % ( (fs2.light-516) / 526.86 ))
    
    if fs2.boot:
    	boot_down = True
    elif boot_down:
    	boot_down = False
    	print("You pressed the boot button")
    
    # Sleep for 15ms so the colour cycle isn't too fast
    time.sleep(0.015)
    
