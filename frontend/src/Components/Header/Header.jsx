import {NavLink} from "react-router-dom";
import "./Header.css"
import Categories from "./Categories/Categories.jsx";

export function Header() {
    return (
        <nav id="main_header">
            <div className="main_header_item">
                <NavLink to="/">Дом</NavLink>
            </div>
            <div className="main_header_item">
                <Categories />
            </div>
            <div className="main_header_item">
                <NavLink to="/registration">Регистрация</NavLink>
            </div>
        </nav>
    )
}