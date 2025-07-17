import {useEffect, useState} from "react";
import "./Categories.css"
import {useSelector} from "react-redux";
import {NavLink, useLocation, useSearchParams} from "react-router-dom";

export default function Categories() {
    const [isCategoriesOpen, setIsCategoriesOpen] = useState(false)

    const [searchParams, setSearchParams] = useSearchParams()

    const categories = useSelector(state => state.categories)
        .map(category => category.name)
    const selectedCategoriesFromSearchParams = searchParams.getAll("category")
    const [selectedCategories, setSelectedCategories] = useState(selectedCategoriesFromSearchParams)

    const options = categories.filter(category => !selectedCategories.includes(category))

    useEffect(() => {
        setSearchParams({...searchParams, category: selectedCategories})
    }, [searchParams, selectedCategories]);

    function toggleCategories() {
        setIsCategoriesOpen(previousState => !previousState)
    }

    function selectCategory(e) {
        setSelectedCategories(previousState => {
            return [...previousState, e.target.textContent]
        })
    }

    function deselectCategory(e) {
        setSelectedCategories(previousState => {
            return previousState.filter(category => category !== e.target.textContent)
        })
    }

    function selectAllCategories() {
        setSelectedCategories(previousState => {
            return [...previousState, ...options]
        })
    }

    function deselectAllCategories() {
        setSelectedCategories([])
    }

    const location = useLocation()

    return <div id="categories_submenu">
        <button id="categories_button" onClick={toggleCategories}>Cats</button>
        <div id="categories_content" style={{display: isCategoriesOpen ? "flex" : "none"}}>
            <div id="categories_selected">
                <div id="categories_selected_list">
                    {selectedCategories.map(category => <button onClick={deselectCategory} key={category} className="main_header_categories_selected_category">{category}</button>)}
                </div>
                <div id="categories_selected_buttons">
                    {!location.pathname.startsWith("/tracks") && <NavLink to={"/tracks?" + searchParams.toString()} id="categories_search_button" className="categories_selected_button">Search</NavLink>}
                </div>
            </div>
            <div id="categories_options">
                <div id="categories_options_list">
                    {options.map(category => <button key={category} className="main_header_categories_category" onClick={selectCategory}>{category}</button>)}
                </div>
                <div id="categories_options_buttons">
                    <button onClick={selectAllCategories} className="categories_selected_button" id="categories_select_all_button">Select All</button>
                    <button onClick={deselectAllCategories} className="categories_selected_button" id="categories_deselect_all_button">Deselect All</button>
                </div>
            </div>
        </div>
    </div>
}