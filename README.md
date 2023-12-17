# Inversion engine

## Installation

- Firstly, ensure that you have manimce installed. You can follow the instructions to install here: [Installation - Manim Community](https://docs.manim.community/en/stable/installation.html)
- Then, clone this repository: `https://github.com/njberman/Manim_Circular_Inversion.git`, and run `manim -pqh examples.py ExampleInversions`, or just play the `TestInversions.mp4` file, to see how the inversions work, and enjoy!

## Docs

- Usage:
```python
invert(object_to_invert, circle_of_inversion)

# object_to_invert can be of the following types:
[[tuple, list, np.ndarray], [Dot], [Line], [Circle]]

# circle_of_inversion must be of the type Circle

# Depending on the object to be inverted, the invert function can return any of the above types
```