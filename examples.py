from inversion_engine import invert as i
from manim import *
from numpy import *


class ExampleInversions(Scene):
    def construct(self):
        O = np.array([0, 0, 0])
        r = 2
        omega = Circle(r, color=RED)
        omega.move_to(O)
        omega_label = Tex("\[\\Omega\]", color=RED, font_size=32)
        a = radians(145)
        omega_label.move_to(np.array([(r + 0.5) * cos(a), (r + 0.5) * sin(a), 0]) + O)
        omega_radius = DashedLine(
            O,
            np.array([r * cos(a + radians(15)), r * sin(a + radians(15)), 0]) + O,
            color=RED,
        )
        omega_radius_label = Tex("r", color=RED, font_size=24)
        omega_radius_label.move_to(
            np.array(
                [
                    r / 2 * cos(a + radians(15)) + 0.125,
                    r / 2 * sin(a + radians(15)) + 0.125,
                    0,
                ]
            )
            + O
        )
        O_dot = Dot(O, color=RED, radius=0.05)
        O_dot.set_z_index(1)
        self.play(
            Create(omega),
            Create(omega_label),
            Create(omega_radius),
            Create(omega_radius_label),
            Create(O_dot),
        )

        example_dot = Dot([1.2, 1.3, 0], color=TEAL)
        self.play(Create(example_dot))

        example_dot_p = i(example_dot, omega)
        self.play(TransformFromCopy(example_dot, example_dot_p))

        self.wait(1)

        example_line = Line([1.75, -50, 0], [1.75, 50, 0], color=TEAL)
        self.play(FadeIn(example_line))

        example_line_p = i(example_line, omega)
        self.play(TransformFromCopy(example_line, example_line_p))

        self.wait(1)

        example_circle = Circle(0.8, color=TEAL)
        example_circle.move_to([-1.2, 0.9, 0])
        self.play(Create(example_circle))

        example_circle_p = i(example_circle, omega)
        self.play(TransformFromCopy(example_circle, example_circle_p))

        self.wait(3)
