import os
import time
import math
import numpy as np
import sys

theta_spacing = 0.07
phi_spacing   = 0.02

R1 = 1.0
R2 = 2.0
K2 = 5.0

screen_width  = 50
screen_height = 50

K1 = (screen_width*K2*3)/(8*(R1+R2))


def render_frame(A, B):

    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    output = np.full((screen_width, screen_height), fill_value=' ')
    zbuffer = np.zeros((screen_width,screen_height), dtype='float')

    theta = 0.0
    pi = math.pi

    while theta < 2*pi:
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        phi = 0.0
        while phi < 2*pi:

            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            circlex = R2 + R1*costheta
            circley = R1*sintheta

            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = K2 + cosA*circlex*sinphi + circley*sinA
            ooz = z**-1

            xp = int(screen_width/2 + K1*ooz*x);
            yp = int(screen_height/2 - K1*ooz*y);

            L =  cosphi*costheta*sinB - cosA*costheta*sinphi - \
                sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi)
            
            if L > 0:
                if ooz > zbuffer[xp,yp]:
                    zbuffer[xp,yp] = ooz
                    luminance_index = int(L*8)
                    output[xp, yp] = ".,-~:;=!*#$@"[luminance_index]
            
            phi += phi_spacing

        theta += theta_spacing

    return output

def rotate():
    
    rot = np.arange(0.1, 20.1, 0.1)

    for i in rot:
        frame = render_frame(i, 0.5)

        for row in frame:
            row = ''.join(row)
            sys.stdout.write(row + '\n')
        sys.stdout.flush()
        #time.sleep(0.05)
        #os.system("clear")
rotate()
