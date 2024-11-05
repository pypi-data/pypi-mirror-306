from super_scad.d2.private.PrivateSquare import PrivateSquare
from super_scad.scad.ArgumentAdmission import ArgumentAdmission
from super_scad.scad.Context import Context
from super_scad.scad.ScadWidget import ScadWidget
from super_scad.transformation.Translate2D import Translate2D
from super_scad.type.Vector2 import Vector2


class Square(ScadWidget):
    """
    Widget for creating squares.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: float,
                 center: bool = False,
                 position: Vector2 = None):
        """
        Object constructor.

        :param size: The size of the square.
        :param center: Whether the square is centered at its position.
        :param position: The position of the square. The default value is the origin.
        """
        ScadWidget.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        """
        Validates the arguments supplied to the constructor of this SuperSCAD widget.
        """
        admission = ArgumentAdmission(self._args)
        admission.validate_required({'size'}, {'center'})

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> float:
        """
        Returns the size of this square.
        """
        return self.uc(self._args['size'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether this square is centered at its position.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def position(self) -> Vector2:
        """
        Returns position of this square.
        """
        return self.uc(self._args.get('position', Vector2.origin))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadWidget:
        """
        Builds a SuperSCAD widget.

        :param context: The build context.
        """
        square = PrivateSquare(size=self.size, center=self.center)

        position = self.position
        if position.is_not_origin:
            square = Translate2D(vector=position, child=square)

        return square

# ----------------------------------------------------------------------------------------------------------------------
