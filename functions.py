import pygame


def get_center_coords(env):
    return env.width // 2, env.height // 2


def scale_coords(*coords, scale=4):
    scaled = [coord * scale for coord in coords]
    scaled = tuple(scaled)  # cvt to tuple for pygame
    return scaled


def rotate(surface, angle, pivot, offset):  # https://stackoverflow.com/a/49413006
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

def check_collisions(picar, obstacles):
    for obstacle in obstacles:
        if picar.rect.colliderect(obstacle.rect):
            return True
    return False