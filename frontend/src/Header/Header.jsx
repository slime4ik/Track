import {NavLink} from "react-router-dom";
import "./Header.css"
import Categories from "./Categories/Categories.jsx";

export function Header() {
    return (
        <nav id="main_header">
            <div className="main_header_item">
                <NavLink to="/">Home</NavLink>
            </div>
            <div className="main_header_item">
                <Categories />
            </div>
        </nav>
    )
}