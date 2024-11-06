import math

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Union import Union
from super_scad.d2.Polygon import Polygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad.type.Angle import Angle
from super_scad_smooth_profile.SmoothProfile import SmoothProfile


class Chamfer(SmoothProfile):
    """
    Applies a chamfer to vertices at a node.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 length: float | None = None,
                 height: float | None = None,
                 inner_angle: float,
                 normal_angle: float,
                 position: Vector2,
                 child: ScadWidget):
        """
        Object constructor.

        :param length: The length of the chamfer.
        :param height: The height of the chamfer.
        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param child: The child object on which the fillet is applied.
        """
        SmoothProfile.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        The height of the chamfer.
        """
        if 'height' in self._args:
            return self.uc(self._args['height'])

        inner_angle = self.inner_angle
        if inner_angle > 180:
            inner_angle = Angle.normalize(360.0 - inner_angle)

        angle = Angle.normalize(inner_angle / 2.0, 180.0)

        return 0.5 * self.length / math.tan(math.radians(angle))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> float:
        """
        The height of the chamfer.
        """
        if 'length' in self._args:
            return self.uc(self._args['length'])

        angle = Angle.normalize(self.inner_angle, 180.0)

        return 2.0 * self.height * math.tan(math.radians(0.5 * angle))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        inner_angle = self.inner_angle

        if inner_angle < 180.0:
            # The corner is convex.
            polygon = self._build_polygon(context,
                                          self.normal_angle,
                                          Angle.normalize(self.inner_angle / 2.0, 180.0))

            return Difference(children=[self.child, polygon])

        if inner_angle > 180.0:
            # The corner is concave.
            polygon = self._build_polygon(context,
                                          Angle.normalize(self.normal_angle - 180.0),
                                          Angle.normalize((360.0 - self.inner_angle) / 2.0, 90.0))

            return Union(children=[self.child, polygon])

        return self.child

    # ------------------------------------------------------------------------------------------------------------------
    def _build_polygon(self, context: Context, normal_angle: float, alpha: float) -> ScadWidget:
        """
        Returns a masking polygon.

        :param context: The build context.
        """
        p1 = self.position
        p2 = self.position + \
             Vector2.from_polar_coordinates(self.height, normal_angle) + \
             Vector2.from_polar_coordinates(0.5 * self.length, normal_angle + 90.0)
        p3 = p2 + Vector2.from_polar_coordinates(self.length, normal_angle - 90.0)

        eps0 = Vector2.from_polar_coordinates(context.eps, normal_angle + 180.0)
        eps1 = Vector2.from_polar_coordinates(context.eps, normal_angle + alpha + 90.0)
        eps2 = Vector2.from_polar_coordinates(context.eps, normal_angle - alpha - 90.0)

        return Polygon(points=[p1 + eps0,
                               p1 + eps1,
                               p2 + eps1,
                               p2,
                               p3,
                               p3 + eps2,
                               p1 + eps2])

# ----------------------------------------------------------------------------------------------------------------------
