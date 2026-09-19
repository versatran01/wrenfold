# https://arxiv.org/pdf/1107.1119
import wrenfold as wf
from wrenfold import sym


class UnitN:

  def __init__(self, n: int = 2):
    pass


def compute_Rx(x: wf.Vector3):
    """
    Given `x` as a unit-vector, compute basis matrix Rx that maps from tangent-space
    at `x` to ambient space.

    Equation (106)
    """
    v = x - sym.vector(1, 0, 0)
    v_norm_squared = v.squared_norm()

    vvT = v * v.T
    H_reflect = sym.eye(3) - 2 * vvT / v_norm_squared

    # Mirror H_reflect about the y-axis to convert it from a reflection to a rotation.
    Rx = H_reflect * sym.matrix([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

    # Small angle case converts to identity.
    return sym.where(v_norm_squared < 1.0e-16, sym.eye(3), Rx)


def unit3_retract(x: wf.Vector3, dx: wf.Vector3):
    """
    Given `x` as a unit-vector and `v` as a tangent vector at `x`, compute the retraction
    of `v` at `x` back to the unit-sphere.

    Equation (107) and (109)
    """
    dx_norm = dx.norm()

    exp_dx = sym.vector(
        sym.cos(dx_norm),
        sym.sin(dx_norm) * dx[0, 0] / dx_norm,
        sym.sin(dx_norm) * dx[1, 0] / dx_norm,
    )
    exp_dx_small_angle = sym.vector(1, dx[0, 0], dx[1, 0])
    exp_dx_small_angle = exp_dx_small_angle / exp_dx_small_angle.norm()
    return compute_Rx(x) * sym.where(dx_norm < 1.0e-16, exp_dx_small_angle, exp_dx)


def unit3_local_coord(y: wf.Vector3, x: wf.Vector3):
    """
    Given `x` as a unit-vector and `y` as a unit-vector, compute the local coordinates
    of `y` in the tangent space at `x`.

    local_coords = y [-] x

    Equation (108) and (109)
    """
    Rx = compute_Rx(x)
    y_local = Rx.T * y

    w = y_local[0, 0]
    v = y_local[1:3, 0]
    v_norm = v.norm()

    dx = (v / v_norm) * sym.atan2(v_norm, w)
    dx_small_angle = sym.atan2(0, w) * sym.vector(1, 0)

    return sym.where(v_norm < 1.0e-16, dx_small_angle, dx)
