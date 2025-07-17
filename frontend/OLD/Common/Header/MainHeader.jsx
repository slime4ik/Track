import Header from "./Header.jsx";
import {NavLink} from "react-router-dom";
import CategoriesMenu from "./CategoriesMenu/CategoriesMenu.jsx";
import {AnimatePresence, motion} from "framer-motion";
import "./MainHeader.css"

export default function MainHeader() {
    return (
        <AnimatePresence>
            <Header key="main_header" id="main_header">
                  <Header.Item key="home" id="main_header_categories" className="main_header_item">
                      <NavLink to="/">Home</NavLink>
                  </Header.Item>
                  <Header.Item key="categories" id="main_header_categories" className="main_header_item">
                        <CategoriesMenu />
                  </Header.Item>
                  <Header.Item key="tracks" id="main_header_categories" className="main_header_item">
                        <NavLink to="/tracks">SEARCH</NavLink>
                  </Header.Item>
            </Header>
        </AnimatePresence>
    )
}