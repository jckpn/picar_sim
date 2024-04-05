def scale_coords(coords, scale=4):
    if isinstance(coords, tuple):
        return tuple(scale_coords(c) for c in coords)
    elif isinstance(coords, list):
        return [scale_coords(c) for c in coords]
    else:
        return coords * scale
