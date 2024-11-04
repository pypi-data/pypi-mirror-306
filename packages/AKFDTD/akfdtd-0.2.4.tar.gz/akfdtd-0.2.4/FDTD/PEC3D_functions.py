import math


# no PEC
def free_PEC_func(hx, hy, hz, x0, y0, z0):
    return lambda x, y, z: x != x


# set single rectangular slit
def rect_slit_func(hx, hy, hz, x0, y0, z0):
    return lambda x, y, z: (x0 - hx / 2 < x) & (x < x0 + hx / 2) & \
                           ((y0 - hy / 2 > y) | (y > y0 + hy / 2) | (z0 - hz / 2 > z) | (z > z0 + hz / 2))


# set single hexagonal slit
def hex_slit_func(hx, hy, hz, x0, y0, z0):
    d = hy
    return lambda x, y, z: (x0 - hx / 2 < x) & (x < x0 + hx / 2) & \
                           ((abs(y - y0) > d / 2) | (abs(z - z0) > (d - abs(y - y0)) / math.sqrt(3)))


# set single circular slit
def circ_slit_func(hx, hy, hz, x0, y0, z0):
    d = hy
    return lambda x, y, z: (x0 - hx / 2 < x) & (x < x0 + hx / 2) & \
                           ((y - y0)**2 + (z - z0)**2 > d**2 / 4)


# set single rectangular obstacle
def rect_obstacle_func(hx, hy, hz, x0, y0, z0):
    return lambda x, y, z: (x0 - hx / 2 < x) & (x < x0 + hx / 2) & \
                           ((y0 - hy / 2 < y) & (y < y0 + hy / 2) & (z0 - hz / 2 < z) & (z < z0 + hz / 2))


# set single hexagonal obstacle
def hex_obstacle_func(hx, hy, hz, x0, y0, z0):
    d = hy
    return lambda x, y, z: (x0 - hx / 2 < x) & (x < x0 + hx / 2) & \
                           ((abs(y - y0) < d / 2) & (abs(z - z0) < (d - abs(y - y0)) / math.sqrt(3)))


# set single circular slit
def circ_obstacle_func(hx, hy, hz, x0, y0, z0):
    d = hy
    return lambda x, y, z: (x0 - hx / 2 < x) & (x < x0 + hx / 2) & \
                           ((y - y0)**2 + (z - z0)**2 < d**2 / 4)
