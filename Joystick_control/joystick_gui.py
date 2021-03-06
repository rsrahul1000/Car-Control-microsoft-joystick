import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import subprocess
import time 

#styling for matplotlib
style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

display_window = []
def animate(i):
    global display_window
    print("function recived data :", display_window)
    ax1.clear()
    ax1.plot(display_window)
    plt.show()

#Creation of subprocess to read data from joystick
process = subprocess.Popen(['jstest', '--normal', '/dev/input/js0'], 
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

def check(data):
    if len(data) >= 1:
        if len(data)==2 and data[1]==":":
            return False
        elif len(data) >=2 and data[1] == ":":
            return (True,1)
        return True
    return False

count = 0
while True:
    try:
        output = process.stdout.readline()
        #h = output.strip().split()
        h = output.strip().split(' ')
        g = []
        for i in h:
            response = check(i)
            if type(response) is bool:
                if response == True:
                    g.append(i)
            else:
                    g.append(i[2:])
        print("outside function ", g)
        ##################### g is the main variable
        if count != 20:
            count += 1
        elif len(g) > 10:
            data = int(g[1])
            if len(display_window) == 10:
                display_window.append(data)
                del display_window[0]
            else:
                display_window.append(data)
            print("inside function ",display_window)
            ani = animation.FuncAnimation(fig, animate, interval=0.1)
            plt.show(block = False)
            g = []
        ##################### coading aread above
        return_code = process.poll()
        if return_code is not None:
            print('RETURN CODE', return_code)
            # Process has finished, read rest of the output 
            for output in process.stdout.readlines():
                print(output.strip())
            break
        print()
    except KeyboardInterrupt:
        print(" User Instrupt Generated ")
        

