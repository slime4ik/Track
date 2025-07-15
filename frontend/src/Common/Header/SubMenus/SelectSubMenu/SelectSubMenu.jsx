import "./SelectSubMenu.css"
import {useState} from "react";
import {NavLink} from "react-router-dom";

const CATEGORIES_URL = "http://localhost:8000/api/tracks/"

export default function SelectSubMenu({options = []}) {
    const [selected, setSelected] = useState([]);

    function handleSelect(e) {
        setSelected(previousSelected => {
            return [...previousSelected, e.target.dataset.key]
        })
    }

    function handleUnselect(e) {
        setSelected(previousSelected => {
            return previousSelected.filter(option => option !== e.target.dataset.key)
        })
    }

    function selectAll() {
        setSelected(previousSelected => {
            return [...previousSelected, ...options]
        })
    }

    function unselectAll() {
        setSelected([])
    }

    const searchLink = `${CATEGORIES_URL}?category=${selected.join("&category=")}`

    // TODO: Refactor this ...
    const optionsToShow = options.filter(option => !selected.includes(option))
    return (
        <div className="select_sub_menu">
            <div className="select_sub_menu_selected">
                <div className="select_sub_menu_selected_items">
                    {selected.map(option => <button className="select_sub_menu_selected_item" key={option} data-key={option} onClick={handleUnselect}>{option}</button>)}
                </div>
                <NavLink to={searchLink} className="select_sub_menu_selected_search_button">Search</NavLink>
            </div>
            <div className="select_sub_menu_options_container">
                <div className="select_sub_menu_options">
                    {optionsToShow.map(option => <button className="select_sub_menu_options_item" key={option} data-key={option} onClick={handleSelect}>{option}</button>)}
                </div>
                <div className="select_sub_menu_options_buttons">
                    <button onClick={selectAll}>Select All</button>
                    <button onClick={unselectAll}>Unselect All</button>
                </div>
            </div>
        </div>
    )
}