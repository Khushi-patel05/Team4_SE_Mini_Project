
"""
collision: figures out whether a falling object has reached the basket.
"""


def is_caught(basket_rect, obj):
    """Return True when the object overlaps the basket horizontally and vertically."""
    horizontally_overlapping = (
        obj.x + obj.radius >= basket_rect.left
        and obj.x - obj.radius <= basket_rect.right
    )

    vertically_reached = (
        obj.y + obj.radius >= basket_rect.top
        and obj.y - obj.radius <= basket_rect.bottom
    )

    return horizontally_overlapping and vertically_reached
