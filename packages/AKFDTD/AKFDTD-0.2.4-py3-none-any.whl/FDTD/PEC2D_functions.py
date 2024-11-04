# no PEC
def free_PEC_func(hx, hy, x0, y0):
    return lambda x, y: x != x


# set single rectangular slit
def slit_func(hx, hy, x0, y0):
    return lambda x, y: (x0 - hx / 2 < x) & (x < x0 + hx / 2) & ((y0 - hy / 2 > y) | (y > y0 + hy / 2))
