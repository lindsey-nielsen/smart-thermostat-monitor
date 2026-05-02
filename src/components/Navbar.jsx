import { Link, useLocation } from "react-router-dom";

/**
 * Navbar component for the runtime monitor application.
 *
 * Provides navigation between different simulation views
 * (correct behavior and buggy scenarios). Highlights the
 * currently active route using the URL path.
 */

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <h2 className="navbar-logo">Smart Thermostat</h2>

        <div className="navbar-links">
          <Link to="/" className={location.pathname === "/" ? "active" : ""}>
            Correct
          </Link>

          <Link
            to="/buggy-temp"
            className={location.pathname === "/buggy-temp" ? "active" : ""}
          >
            Buggy Temp
          </Link>

          <Link
            to="/buggy-mode"
            className={location.pathname === "/buggy-mode" ? "active" : ""}
          >
            Buggy Mode
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
