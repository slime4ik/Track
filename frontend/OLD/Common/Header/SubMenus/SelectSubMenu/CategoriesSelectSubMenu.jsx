import "./CategoriesSelectSubMenu.css"
import {useEffect, useState} from "react";
import {NavLink, useSearchParams} from "react-router-dom";
import {motion} from "framer-motion";
import getAlreadySelectedCategories from "../../../utils/getAlreadySelectedCategories.js";
import {createCategoriesSearchParams} from "../../../utils/createCategoriesSearchParams.js";
import selectedCategoriesSlice from "../../../../../src/ReduxSlices/SelectedCategoriesSlice.jsx";
import {useDispatch} from "react-redux";

function moveSelectedToLocalStorage(selected) {
    localStorage.setItem("selected", JSON.stringify(selected))
}

export default function CategoriesSelectSubMenu({options = []}) {
    const alreadySelectedFromStorage = getAlreadySelectedCategories()
    const [urlParams, setUrlParams] = useSearchParams()

    // TODO: REFACTOR THIS ...
    const alreadySelected = alreadySelectedFromStorage ?? []

    const [selected, setSelected] = useState(alreadySelected);

    const dispatch = useDispatch()

    useEffect(() => {
        setUrlParams({category: selected})
    }, [selected]);

    moveSelectedToLocalStorage(selected);
    dispatch(selectedCategoriesSlice.actions.setSelectedCategories(selected));

    function handleSelect(e) {
        setSelected(previousSelected => [...previousSelected, e.target.dataset.key])
    }

    function handleUnselect(e) {
        setSelected(previousSelected => previousSelected.filter(option => option !== e.target.dataset.key))
    }

    function selectAll() {
        setSelected(previousSelected => [...previousSelected, ...options]
            .filter((option, index, array) => array.indexOf(option) === index)
        )
    }

    function unselectAll() {
        setSelected([])
    }

    // TODO: Refactor this ...
    const optionsToShow = options.filter(option => !selected.includes(option))
    return (
        <motion.div className="select_sub_menu">
            <motion.div className="select_sub_menu_selected">
                <motion.div className="select_sub_menu_selected_items">
                    {selected.map(option => <motion.button layout layoutId={option} className="select_sub_menu_selected_item" key={option} data-key={option} onClick={handleUnselect}>{option}</motion.button>)}
                </motion.div>
                <NavLink to={"/tracks" + createCategoriesSearchParams(alreadySelected)} className="select_sub_menu_selected_search_button">Search</NavLink>
            </motion.div>
            <motion.div className="select_sub_menu_options_container">
                <motion.div>
                    {optionsToShow.map(option => <motion.button layout layoutId={option} className="select_sub_menu_options_item" key={option} data-key={option} onClick={handleSelect}>{option}</motion.button>)}
                </motion.div>
                <motion.div className="select_sub_menu_options_buttons">
                    <motion.button onClick={selectAll}>Select All</motion.button>
                    <motion.button onClick={unselectAll}>Unselect All</motion.button>
                </motion.div>
            </motion.div>
        </motion.div>
    )
}