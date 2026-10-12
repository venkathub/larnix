"""Larnix M03-L01: implement and test a five-document similarity comparison.

Run: python3 exercise.py
Complete the TODOs, then compare your results with hand calculations and NumPy.
No model, credentials, or external dataset is needed.
"""
import math

QUERY = [1.0, 0.0]
DOCUMENTS = {
    "A": [1.0, 0.0], "B": [2.0, 2.0], "C": [-1.0, 0.0],
    "D": [0.0, 1.0], "E": [0.0, 0.0],
}


def validate_pair(a, b):
    if not a or len(a) != len(b):
        raise ValueError("Vectors must be nonempty and have equal dimensions")
    if not all(math.isfinite(x) for x in [*a, *b]):
        raise ValueError("Coordinates must be finite")


def dot(a, b):
    validate_pair(a, b)
    # TODO: multiply corresponding coordinates, then add.
    raise NotImplementedError("Implement dot product")


def cosine(a, b):
    validate_pair(a, b)
    # TODO: return None if either vector has zero length; otherwise normalize
    # both vectors and compute their dot product. Do not replace None with 0.
    raise NotImplementedError("Implement cosine similarity")


def main():
    print("Expected dot scores: A=1, B=2, C=-1, D=0, E=0")
    print("Expected cosine: A=1, B=1/sqrt(2), C=-1, D=0, E=None")
    for name, vector in DOCUMENTS.items():
        print(name, "dot:", dot(QUERY, vector), "cosine:", cosine(QUERY, vector))
    # TODO: rank the valid scores, explicitly preserve ties, and list exclusions.
    # TODO: verify positive-scaling invariance of cosine and the dot/unit-vector identity.
    # TODO: add tests for zero query, dimension mismatch and non-finite inputs.
    # TODO: compare your functions with a numerical library such as NumPy.


if __name__ == "__main__":
    main()
