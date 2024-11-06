from super_scad.scad.ScadWidget import ScadWidget
from super_scad.type import Vector2
from super_scad_smooth_profile.SmoothProfile import SmoothProfile
from super_scad_smooth_profile.SmoothProfileFactory import SmoothProfileFactory

from super_scad_smooth_profiles.Chamfer import Chamfer


class ChamferFactory(SmoothProfileFactory):
    """
    A factory that produces chamfer smoothing profiles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 length: float | None = None,
                 height: float | None = None):
        """
        Object constructor.

        :param length: The length of the chamfer.
        :param height: The height of the chamfer.
        """
        self._length: float = length
        """
        The length of the chamfer.
        """

        self._height: float = height
        """
        The height of the chamfer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def create_smooth_profile(self,
                              *,
                              inner_angle: float,
                              normal_angle: float,
                              position: Vector2,
                              child: ScadWidget) -> SmoothProfile:
        """
        Returns a smoothing profile widget creating a chamfer.

        :param inner_angle: Inner angle between the vertices.
        :param normal_angle: The normal angle of the vertices, i.e., the angle of the vector that lies exactly between
                             the two vertices and with origin at the node.
        :param position: The position of the node.
        :param child: The child object on which the smoothing must be applied.
        """
        return Chamfer(length=self._length,
                       height=self._height,
                       inner_angle=inner_angle,
                       normal_angle=normal_angle,
                       position=position,
                       child=child)

    # ------------------------------------------------------------------------------------------------------------------
