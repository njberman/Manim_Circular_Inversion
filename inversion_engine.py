from manim import *
from numpy import *


def invert(
    object: tuple | list | np.ndarray | Dot | Line | Circle,
    circle: Circle = Circle(1),
    seg=False,
    color=YELLOW,
):
    def calculate_intersection_point_line_line(p1, p2, q1, q2):
        # Convert the points to numpy arrays for easier calculations
        p1, p2, q1, q2 = np.array(p1), np.array(p2), np.array(q1), np.array(q2)

        # Calculate the direction vectors of the lines
        v1 = p2 - p1
        v2 = q2 - q1

        # Set up the system of linear equations and solve for the parameters t and s
        A = np.vstack((v1, -v2)).T
        b = q1 - p1
        t, s = np.linalg.lstsq(A, b, rcond=None)[0]

        # Calculate the intersection point
        intersection_point = p1 + t * v1

        return intersection_point

    def calculate_intersection_point_line_circle(
        line_start, line_end, circle_center, circle_radius
    ):
        # Convert the points to numpy arrays for easier calculations
        line_start, line_end, circle_center = (
            np.array(line_start),
            np.array(line_end),
            np.array(circle_center),
        )

        # Calculate the direction vector of the line
        line_vector = line_end - line_start

        # Calculate the coefficients of the quadratic equation
        a = np.dot(line_vector, line_vector)
        b = 2 * np.dot(line_vector, line_start - circle_center)
        c = (
            np.dot(line_start - circle_center, line_start - circle_center)
            - circle_radius**2
        )

        # Solve the quadratic equation to find the parameter values
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            # No real solutions, i.e., no intersection points
            return []
        else:
            t1 = (-b + np.sqrt(discriminant)) / (2 * a)
            t2 = (-b - np.sqrt(discriminant)) / (2 * a)

            # Calculate the intersection points
            intersection_point1 = line_start + t1 * line_vector
            intersection_point2 = line_start + t2 * line_vector

            return [intersection_point1, intersection_point2]

    O = circle.get_center()
    O_x, O_y, _ = O
    if type(object) is tuple or isinstance(object, np.ndarray):
        x, y, _ = object
        a = x - O_x
        b = y - O_y
        r = circle.radius
        l = a**2 + b**2
        x_p = (a * r**2 / l) + O_x
        y_p = (b * r**2 / l) + O_y
        return np.array([x_p, y_p, 0.0])

    if type(object) is Dot:
        x, y, _ = object.get_center()
        c_p = invert(object.get_center(), circle)
        return Dot(c_p, color=color)

    if type(object) is Line:
        p1, p2 = object.get_anchors()

        p1_x, p1_y, _ = p1
        p2_x, p2_y, _ = p2

        verti = p2_x - p1_x == 0
        if (verti and p1_x == O_x) or round(
            ((p2_y - p1_y) / (p2_x - p1_x)) * (O_x - p1_x) + p1_y, 9
        ) == round(O_y, 9):
            return Line(p1, p2, color=color)

        line_vector = np.array(p1) - np.array(p2)
        perpendicular_vector = np.array([-line_vector[1], line_vector[0], 0])

        start2 = O
        end2 = O + perpendicular_vector

        Q = np.array(calculate_intersection_point_line_line(p1, p2, start2, end2))
        Q_p = invert(Q, circle)
        Q_p_x, Q_p_y, _ = Q_p

        C_x = (O_x + Q_p_x) / 2
        C_y = (O_y + Q_p_y) / 2
        r = sqrt((C_x - O_x) ** 2 + (C_y - O_y) ** 2)

        if not seg:
            new_circle = Circle(r, color=color)
            new_circle.move_to([C_x, C_y, 0])
            return new_circle

        p1_p = invert(p1, circle)
        p2_p = invert(p2, circle)
        new_circle = ArcBetweenPoints(
            p2_p, p1_p, radius=r, arc_center=[C_x, C_y, 0], color=color
        )
        return new_circle

    if type(object) is Circle:
        C = object.get_center()
        C_x, C_y, _ = C
        if round((O_x - C_x) ** 2 + (O_y - C_y) ** 2, 9) == round(
            object.radius**2, 9
        ):
            Q = np.array([2 * C_x - O_x, 2 * C_y - O_y, 0])
            Q_p = invert(Q, circle)
            Q_x, Q_y, _ = Q_p

            if Q_y == 0:
                return Line(
                    np.array((Q_x, 40, 0)) + O,
                    np.array((Q_x, -40, 0)) + O,
                    color=color,
                )

            m_OQ_p = Q_y / Q_x
            m_perp = -1 / m_OQ_p
            eq_perp = lambda x: m_perp * (x - Q_x) + Q_y
            return Line((-40, eq_perp(-40), 0), (40, eq_perp(40), 0), color=color)

        eq = lambda x: ((O_y - C_y) / (O_x - C_x)) * (x - C_x) + C_y
        Q, P = calculate_intersection_point_line_circle(
            O,
            np.array([50, eq(50), 0]),
            C,
            object.radius,
        )

        Q_p = invert(Q, circle)
        P_p = invert(P, circle)

        Q_P_x, Q_P_y, _ = Q_p
        P_P_x, P_P_y, _ = P_p

        pos = np.array(((Q_P_x + P_P_x) / 2, (Q_P_y + P_P_y) / 2, 0))
        C = Circle(sqrt((P_P_x - Q_P_x) ** 2 + (P_P_y - Q_P_y) ** 2) / 2, color=color)
        C.move_to(pos)
        return C
