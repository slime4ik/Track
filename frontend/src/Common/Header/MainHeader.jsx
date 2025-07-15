import Header from "./Header.jsx";
import {NavLink} from "react-router-dom";
import useFetch from "../Hooks/useFetch.jsx";
import {useEffect, useState} from "react";
import CategoriesMenu from "./CategoriesMenu/CategoriesMenu.jsx";

const CATEGORIES_URL = "http://localhost:8000/api/tracks/?category="

export default function MainHeader() {
    const [fetchState, setFetchState] = useState(null);

    useEffect(() => useFetch("http://127.0.0.1:8000/api/home?format=json", setFetchState), [])

    return (
        <Header id="main_header">
              <Header.Item id="main_header_categories">
                  <NavLink to="/">Home</NavLink>
              </Header.Item>
            {fetchState && fetchState.categories?.map(category => (
                <Header.Item key={fetchState.categories.name}>
                    <NavLink to={CATEGORIES_URL + category.name}>{category.name}</NavLink>
                </Header.Item>
            ))}
              <Header.Item id="main_header_categories">
                    <CategoriesMenu />
              </Header.Item>
        </Header>
    )
}