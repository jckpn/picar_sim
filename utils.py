def scale_coords(coords, scale=4):
    return coords * scale if isinstance(coords, int) else [scale * c for c in coords]
