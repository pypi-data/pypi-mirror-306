import numpy as np

from dataclasses import dataclass, field


@dataclass
class Cell:
    # Input parameters
    Label: int = 0
    X: int = 0
    Y: int = 0
    Area: float = 0.0
    Peri: float = 0.0
    Feret: float = 0.0
    MinFeret: float = 0.0
    EllipMaj: float = 0.0
    Width: float = 0.0
    Height: float = 0.0
    Solidity: float = 0.0
    Neighbors: int = 0

    # Output parameters
    AoP: float = np.nan
    FeretAR: float = np.nan
    Compactness: float = np.nan
    Extent: float = np.nan
    A_hull: float = np.nan
    P_hull: float = np.nan
    PoN: float = np.nan
    Poly_SR: float = np.nan
    Poly_AR: float = np.nan
    Poly_Ave: float = np.nan
    Hex_SR: float = np.nan
    Hex_AR: float = np.nan
    Hex_Ave: float = np.nan

    def get_output(self) -> None:
        def safe_divide(a, b):
            return a / b if b != 0 else float('nan')

        # Basic shape descriptors
        self.AoP = safe_divide(self.Area, self.Peri)
        self.FeretAR = safe_divide(self.Feret, self.MinFeret)
        self.Compactness = safe_divide(
            np.sqrt((4.0 / np.pi) * self.Area), self.EllipMaj)
        self.Extent = safe_divide(self.Area, (self.Width * self.Height))
        self.A_hull = safe_divide(self.Area, self.Solidity)
        self.P_hull = 6.0 * \
            np.sqrt(safe_divide(self.A_hull, (1.5 * np.sqrt(3.0))))

        if self.Neighbors > 0:
            self.PoN = safe_divide(self.Peri, self.Neighbors)

        if self.Neighbors < 3:
            # Cannot compute polygonality metrics with fewer than 3 neighbors
            return

        # Polygonality metrics based on the number of sides (neighbors)
        n = self.Neighbors
        tan_pi_n = np.tan(np.pi / n)
        denom_poly = np.sqrt((4.0 * self.Area) / (n * (1.0 / tan_pi_n)))

        term_poly_sr = safe_divide(self.PoN, denom_poly)
        self.Poly_SR = 1.0 - np.sqrt((1.0 - term_poly_sr) ** 2)

        denom_poly_ar = 0.25 * n * self.PoN ** 2 * (1.0 / tan_pi_n)
        term_poly_ar = safe_divide(self.Area, denom_poly_ar)
        self.Poly_AR = 1.0 - np.sqrt((1.0 - term_poly_ar) ** 2)

        self.Poly_Ave = 10.0 * (self.Poly_SR + self.Poly_AR) / 2.0

        # Hexagonality metrics based on a convex regular hexagon
        # Calculating apothems and sides
        sqrt3 = np.sqrt(3.0)
        apoth1 = (sqrt3 * self.Peri) / 12.0
        apoth2 = (sqrt3 * self.Feret) / 4.0
        apoth3 = self.MinFeret / 2.0
        side1 = self.Peri / 6.0
        side2 = self.Feret / 2.0
        side3 = self.MinFeret / sqrt3
        side4 = self.P_hull / 6.0

        # Unique area calculations
        Area_uniq = [
            0.5 * (3.0 * sqrt3) * side1 ** 2,
            0.5 * (3.0 * sqrt3) * side2 ** 2,
            0.5 * (3.0 * sqrt3) * side3 ** 2,
            3.0 * side1 * apoth2,
            3.0 * side1 * apoth3,
            3.0 * side2 * apoth3,
            3.0 * side4 * apoth1,
            3.0 * side4 * apoth2,
            3.0 * side4 * apoth3,
            self.A_hull,
            self.Area
        ]

        # Calculate area ratios
        Area_ratio = 0.0
        jv = 0
        for ib in range(len(Area_uniq)):
            for ic in range(ib + 1, len(Area_uniq)):
                term = safe_divide(Area_uniq[ib], Area_uniq[ic])
                Area_ratio += 1.0 - np.sqrt((1.0 - term) ** 2)
                jv += 1
        self.Hex_AR = safe_divide(Area_ratio, jv)

        # Additional apothems for perimeter calculations
        apoth4 = (sqrt3 * self.P_hull) / 12.0
        apoth5 = np.sqrt((4.0 * self.A_hull) / (4.5 * sqrt3))

        # Unique perimeter calculations
        Perim_uniq = [
            np.sqrt((24.0 * self.Area) / sqrt3),
            np.sqrt((24.0 * self.A_hull) / sqrt3),
            self.Peri,
            self.P_hull,
            3.0 * self.Feret,
            6.0 * self.MinFeret / sqrt3,
            safe_divide(2.0 * self.Area, apoth1),
            safe_divide(2.0 * self.Area, apoth2),
            safe_divide(2.0 * self.Area, apoth3),
            safe_divide(2.0 * self.Area, apoth4),
            safe_divide(2.0 * self.Area, apoth5),
            safe_divide(2.0 * self.A_hull, apoth1),
            safe_divide(2.0 * self.A_hull, apoth2),
            safe_divide(2.0 * self.A_hull, apoth3)
        ]

        # Calculate perimeter ratios
        Perim_ratio = 0.0
        jv = 0
        for ib in range(len(Perim_uniq)):
            for ic in range(ib + 1, len(Perim_uniq)):
                term = safe_divide(Perim_uniq[ib], Perim_uniq[ic])
                Perim_ratio += 1.0 - np.sqrt((1.0 - term) ** 2)
                jv += 1
        self.Hex_SR = safe_divide(Perim_ratio, jv)

        # Average hexagonality measure
        self.Hex_Ave = 10.0 * (self.Hex_AR + self.Hex_SR) / 2.0
