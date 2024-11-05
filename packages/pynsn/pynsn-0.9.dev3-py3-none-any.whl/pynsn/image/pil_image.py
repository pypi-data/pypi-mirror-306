"""
"""
__author__ = "Oliver Lindemann <lindemann@cognitive-psychology.eu>"

from copy import deepcopy
import typing as _tp

import numpy as _np
from PIL import Image as _Image
from PIL import ImageDraw as _ImageDraw

from . import _base
from .. import _shapes
from .. import _stimulus
# TODO pillow supports no alpha/opacity

RESAMPLING = _Image.Resampling.LANCZOS


def create(
    nsn_stimulus: _stimulus.NSNStimulus,
    antialiasing: _tp.Union[bool, int] = True,
) -> _Image.Image:
    # ImageParameter
    """use PIL colours (see PIL.ImageColor.colormap)

    returns pil image

    antialiasing: True or integer

    default_dot_colour: if colour is undefined in _lib
    """

    return _PILDraw().create_image(
        nsn_stimulus=nsn_stimulus, antialiasing=antialiasing
    )


class _PILDraw(_base.AbstractArrayDraw):
    @staticmethod
    def get_image(image_size, background_colour: str, **kwargs) -> _Image.Image:
        # filename not used for pil images
        return _Image.new("RGBA", image_size, color=background_colour)

    @staticmethod
    def scale_image(image, scaling_factor):
        im_size = (
            int(image.size[0] / scaling_factor),
            int(image.size[1] / scaling_factor),
        )
        return image.resize(im_size, resample=RESAMPLING)

    @staticmethod
    def draw_shape(
        image, shape: _shapes.AbstractShape, opacity: float, scaling_factor: float
    ):
        # FIXME opacity is ignored (not yet supported)
        # draw object
        shape = deepcopy(shape)
        shape.xy = _base.cartesian2image_coordinates(
            _np.asarray(shape.xy) * scaling_factor, image.size)
        shape.scale(scaling_factor)

        if isinstance(shape, (_shapes.Ellipse, _shapes.Dot)):
            rx, ry = shape.size / 2
            x, y = shape.xy
            _ImageDraw.Draw(image).ellipse(
                (x - rx, y - ry, x + rx, y + ry), fill=shape.colour.value
            )

        elif isinstance(shape, _shapes.Picture):
            upper_left = _np.flip(shape.left_top).tolist()
            pict = _Image.open(shape.path, "r")
            if pict.size[0] != shape.size[0] or pict.size[1] != shape.size[1]:
                pict = pict.resize((int(shape.size[0]), int(shape.size[1])),
                                   resample=RESAMPLING)

            tr_layer = _Image.new("RGBA", image.size, (0, 0, 0, 0))
            tr_layer.paste(pict, upper_left)
            res = _Image.alpha_composite(image, tr_layer)
            image.paste(res)

        elif isinstance(shape, _shapes.Rectangle):
            # rectangle shape TODO decentral _shapes seems to be bit larger than with pyplot
            _ImageDraw.Draw(image).rectangle(tuple(shape.box),  # type: ignore
                                             fill=shape.colour.value)
        else:
            raise NotImplementedError(
                f"Shape {type(shape)} NOT YET IMPLEMENTED")

    @staticmethod
    def draw_convex_hull(image, points, convex_hull_colour, opacity, scaling_factor):
        # FIXME opacity is ignored (not yet supported)
        points = _base.cartesian2image_coordinates(
            points * scaling_factor, image.size)
        last = None
        draw = _ImageDraw.Draw(image)
        for p in _np.append(points, [points[0]], axis=0):
            if last is not None:
                draw.line(_np.append(last, p).tolist(),
                          width=2, fill=convex_hull_colour.value)
            last = p
