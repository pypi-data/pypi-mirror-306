from super_scad.boolean.Union import Union
from super_scad.d2.Circle import Circle
from super_scad.d2.Rectangle import Rectangle
from super_scad.scad import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate2D import Translate2Dnish


class FinishedRegularPolygonFinishLollipop(FinishedRegularPolygonFinish):
    """
    A finish for a regular polygon node (a.k.a. corner) with a lollipop-shaped cutout.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, diameter: float, stem_length: float, stem_width: float):
        """
        Object constructor.

        :param diameter: The diameter of the lollipop.
        :param stem_length: The length of the stem of the lollipop.
        :param stem_width: The width of the stem of the lollipop.
        """
        self.__diameter: float = diameter
        """
        The radius of a node of a regular polygon.
        """

        self.stem_width = stem_width
        """
        The length of the stem of the lollipop. 
        """

        self.stem_length = stem_length
        """
        The length of the stem of the lollipop. 
        """

    # ------------------------------------------------------------------------------------------------------------------
    def finishing(self, context: Context, polygon: RegularPolygon) -> ScadWidget:
        """
        Returns a SuperSCAD object that will be subtracted from a node (a.k.a. corner) of a regular polygon. It is
        assumed that the node is located at the origin and is aligned along the y-axis.
        """
        return Union(children=[Translate2D(x=-0.5 * self.stem_width,
                                           y=-self.stem_length - 0.5 * self.__diameter,
                                           child=Rectangle(width=self.stem_width,
                                                           depth=self.stem_length + 0.5 * self.__diameter +
                                                                 context.eps)),
                               Translate2D(y=-self.stem_length - 0.5 * self.__diameter,
                                           child=Circle(diameter=self.__diameter, fn4n=True))])

# ----------------------------------------------------------------------------------------------------------------------
