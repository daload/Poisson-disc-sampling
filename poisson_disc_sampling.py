import numpy as np
import matplotlib.pyplot as plt


def pds(width, height, k, r):
    """ NTS """
    # Cell side length
    a = r / np.sqrt(2)

    # Number of cells in the x and y directions of the grid
    columns, rows = int(width / a) + 1, int(height / a) + 1

    # List of coordinates in the grid of cells
    coords_list = [(ix, iy) for ix in range(columns) for iy in range(rows)]

    # Initialize the dictionary of cells: each key is a cell's coordinates, the corresponding value is the index of
    # that cell's point's coordinates in the samples list (or None if the cell is empty).
    cells = {coords: None for coords in coords_list}

    """ AUXILIAR METHODS """

    def get_cell_coords(point):
        """Get the coordinates of the cell that pt(x,y) falls in."""
        return int(point[0] // a), int(point[1] // a)

    def get_neighbours(coords):
        """Return the indexes of points in cells neighboring cell at coords."""
        neighboring_cells = [(-1, -2), (0, -2), (1, -2), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1),
                             (-2, 0), (-1, 0), (1, 0), (2, 0), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1),
                             (-1, 2), (0, 2), (1, 2), (0, 0)]

        neighbours = []
        for x, y in neighboring_cells:
            neighbour_coords = coords[0] + x, coords[1] + y
            # Check if we're out of the grid
            if not (0 <= neighbour_coords[0] < columns and
                    0 <= neighbour_coords[1] < rows):
                continue
            neighbour_cell = cells[neighbour_coords]
            # Check if cell is occupied -> save index on neighbours if it is.
            if neighbour_cell is not None:
                neighbours.append(neighbour_cell)
        return neighbours

    def point_valid(point, samples):
        """Check if a point is a valid sample."""
        cell_coords = get_cell_coords(point)
        for index in get_neighbours(cell_coords):
            nearby_pt = samples[index]
            # Squared distance between or candidate point, point, and this nearby_pt.
            distance2 = (nearby_pt[0] - point[0]) ** 2 + (nearby_pt[1] - point[1]) ** 2
            # Check if the points are too close
            if distance2 < r ** 2:
                return False
        return True

    def get_point(ref_point, samples):
        """Try to find a candidate point relative to ref_point to emit in the sample.
        We draw up to k points from the annulus of inner radius r, outer radius 2r
        around the reference point, ref_point."""
        i = 0
        while i < k:
            i += 1
            rho = np.sqrt(np.random.uniform(r ** 2, 4 * r ** 2))
            theta = np.random.uniform(0, 2 * np.pi)
            point = ref_point[0] + rho * np.cos(theta), ref_point[1] + rho * np.sin(theta)
            if not (0 <= point[0] < width and 0 <= point[1] < height):
                # This point falls outside the domain, try again.
                continue
            if point_valid(point, samples):
                return point
        # We failed to find a suitable point in the vicinity of ref_pointt.
        return False

    # Pick a random point to start with.
    point = (np.random.uniform(0, width), np.random.uniform(0, height))
    samples = [point]

    # Our first sample is indexed at 0 in the samples list and it is active,
    # in the sense that we're going to look for more points in its neighborhood.
    cells[get_cell_coords(point)] = 0
    active = [0]
    nsamples = 1

    # As long as there are points in the active list, keep trying to find samples.
    while active:
        # choose a random "reference" point from the active list.
        idx = np.random.choice(active)
        refpt = samples[idx]
        # Try to pick a new point relative to the reference point.
        pt = get_point(refpt, samples)
        # Check if pt is valid and if it is add it to the sample list and mark it as active.
        # If there are no valid points we remove the current point (at index idx) from the active list
        if pt:
            # Point pt is valid: add it to the samples list and mark it as active
            samples.append(pt)
            nsamples += 1
            active.append(len(samples) - 1)
            cells[get_cell_coords(pt)] = len(samples) - 1
        else:
            active.remove(idx)

    plt.scatter(*zip(*samples), color='r', alpha=0.6, lw=0)
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.axis('off')
    plt.show()
