scale = 4


def scale_coords(coords):
    if isinstance(coords, tuple):
        return tuple(scale_coords(c) for c in coords)
    elif isinstance(coords, list):
        return [scale_coords(c) for c in coords]
    else:
        return coords * scale

def unscale_coords(coords):
    if isinstance(coords, tuple):
        return tuple(unscale_coords(c) for c in coords)
    elif isinstance(coords, list):
        return [unscale_coords(c) for c in coords]
    else:
        return coords // scale