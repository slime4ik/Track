import "./SelectSubMenu.css"
import {useState} from "react";
import {NavLink} from "react-router-dom";
import {motion} from "framer-motion";

const CATEGORIES_URL = "http://localhost:8000/api/tracks/"
const MotionNavLink = motion(NavLink);

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
        <motion.div className="select_sub_menu">
            <motion.div className="select_sub_menu_selected">
                <motion.div className="select_sub_menu_selected_items">
                    {selected.map(option => <motion.button layout layoutId={option} className="select_sub_menu_selected_item" key={option} data-key={option} onClick={handleUnselect}>{option}</motion.button>)}
                </motion.div>
                <NavLink to={searchLink} className="select_sub_menu_selected_search_button">Search</NavLink>
            </motion.div>
            <motion.div className="select_sub_menu_options_container">
                <motion.div>
                    {optionsToShow.map(option => <button layout layoutId={option} className="select_sub_menu_options_item" key={option} data-key={option} onClick={handleSelect}>{option}</button>)}
                </motion.div>
                <motion.div className="select_sub_menu_options_buttons">
                    <motion.button onClick={selectAll}>Select All</motion.button>
                    <motion.button onClick={unselectAll}>Unselect All</motion.button>
                </motion.div>
            </motion.div>
        </motion.div>
    )
}