# PlanetPlot3D
Given a date, will generate a stylized 3-dimensional representation of the solar system at that date, including the Sun, all 8 planets, and Pluto.

![White orbits on black background](samples/samples.svg)

- Requires: matplotlib

## Files and usage:

<ul>
  <li><strong>get_orbit.py:</strong>
  <ul>
    <li>Produces csv file including orbital radii, latitudinal and longitudinal angles for specified bodies using NASA JPL Horizons ephemerides data.</li>
    <li>All planetary data is included in /csvs folder, however this script can be used to get data for any other body tracked by NASA, including dwarf planets, asteroids, comets, etc.</li>
  </ul></li>
  <li><strong>planetplot3d.py</strong>
    <ul>
      <li>Produces a 3D representation of the solar system, with the outer planets' radii reduced for aesthetic effect.</li>
      <li>4 color palettes. Colors may be altered.</li>
      <li>Amount of shown orbital path can be altered.</li>
    </ul>
  </li>
</ul>