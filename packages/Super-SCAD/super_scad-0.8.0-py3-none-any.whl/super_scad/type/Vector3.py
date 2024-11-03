import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector3:
    """
    A point in 3D space.
    """
    x: float
    """
    The x-coordinate of this point.
    """

    y: float
    """
    The y-coordinate of this point.
    """

    z: float
    """
    The z-coordinate of this point.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{self.x}, {self.y}, {self.z}]"

    # ------------------------------------------------------------------------------------------------------------------
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    # ------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    # ------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, other: float):
        return Vector3(self.x / other, self.y / other, self.z / other)

    # ------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other: float):
        return Vector3(self.x * other, self.y * other, self.z * other)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def from_polar_coordinates(length: float, phi: float, theta: float):
        """
        Creates a 3-dimensional vector from polar coordinates.

        @param length: The length of the vector.
        @param phi: The azimuth, i.e., the angle of the vector in the xy-plane.
        @param theta: The inclination, i.e., the angle of the vector in the z-axis.
        """
        phi_radians = math.radians(phi)
        theta_radians = math.radians(theta)

        return Vector3(length * math.sin(theta_radians) * math.cos(phi_radians),
                       length * math.sin(theta_radians) * math.sin(phi_radians),
                       length * math.cos(theta_radians))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> float:
        """
        Returns the length of this vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def normal(self):
        """
        Returns the unit vector of this vector.

        :rtype: super_scad.type.Vector3.Vector3
        """
        length = self.length

        return Vector3(self.x / length, self.y / length, self.z / length)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def phi(self) -> float:
        """
        Returns the azimuth, i.e., the angle of the vector in the xy-plane.
        """
        return math.atan2(self.y, self.x)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def theta(self) -> float:
        """
        Returns the inclination, i.e., the angle of the vector in the z-axis.
        """
        return math.acos(self.z / self.length)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def cross_product(v1, v2):
        """
        Returns cross product of two vectors.

        :rtype: super_scad.type.Vector3.Vector3
        """
        return Vector3(v1.y * v2.z - v1.z * v2.y,
                       v1.z * v2.x - v1.x * v2.z,
                       v1.x * v2.y - v1.y * v2.x)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def dot_product(v1, v2) -> float:
        """
        Returns the dot product of two vectors.
        """
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    # ------------------------------------------------------------------------------------------------------------------
    def rotate_x(self, angle: float):
        """
        Returns a copy of this vector rotated around the x-axis using the right-hand rule.

        :param angle: The angle of rotation.
        :rtype: super_scad.type.Vector3.Vector3
        """
        radians = math.radians(angle)

        return Vector3(self.x,
                       self.y * math.cos(radians) - self.z * math.sin(radians),
                       self.y * math.sin(radians) + self.z * math.cos(radians))

    # ------------------------------------------------------------------------------------------------------------------
    def rotate_y(self, angle: float):
        """
        Returns a copy of this vector rotated around the y-axis using the right-hand rule.

        :param angle: The angle of rotation.
        :rtype: super_scad.type.Vector3.Vector3
        """
        radians = math.radians(angle)

        return Vector3(self.x * math.cos(radians) + self.z * math.sin(radians),
                       self.y,
                       -self.x * math.sin(radians) + self.z * math.cos(radians))

    # ------------------------------------------------------------------------------------------------------------------
    def rotate_z(self, angle: float):
        """
        Returns a copy of this vector rotated around the z-axis using the right-hand rule.

        :param angle: The angle of rotation.
        :rtype: super_scad.type.Vector3.Vector3
        """
        radians = math.radians(angle)

        return Vector3(self.x * math.cos(radians) - self.y * math.sin(radians),
                       self.x * math.sin(radians) + self.y * math.cos(radians),
                       self.z)

# ----------------------------------------------------------------------------------------------------------------------
