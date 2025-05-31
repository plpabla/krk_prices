import { NavLink } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  return (
    <nav>
      <ul>
        <li>
          <NavLink to="/">Wycena</NavLink>
        </li>
        {/* <li>
          <NavLink to="/photo">Analiza zdjęć</NavLink>
        </li> */}
        <li>
          <NavLink to="/contact">Kontakt</NavLink>
        </li>
      </ul>
    </nav>
  );
}
