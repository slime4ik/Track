import "./CategoriesMenu.css"
import Header from "../Header.jsx";
import {createContext, useEffect, useState} from "react";
import useFetch from "../../Hooks/useFetch.jsx";
import SelectSubMenu from "../SubMenus/SelectSubMenu/SelectSubMenu.jsx";

export default function CategoriesMenu() {
    const [isOpened, setIsOpened] = useState(false);

    function handleOpen() {
        setIsOpened(previousIsOpened => {
            return !previousIsOpened;
        });
    }

    const [fetchState, setFetchState] = useState(null);
    useEffect(() => useFetch("http://127.0.0.1:8000/api/home?format=json", setFetchState), [])

    return (
        <Header.SubMenuItem>
            <Header.SubMenuButton className="main_header_sub_button" onClick={handleOpen}>Cats</Header.SubMenuButton>
            <Header.SubMenuContent id="main_header_categories_content" className={"main_header_sub_content " + (isOpened && fetchState ? "opened" : "")}>
                <SelectSubMenu options={fetchState ? fetchState.categories?.map(category => category.name) : []}>
                </SelectSubMenu>
            </Header.SubMenuContent>
        </Header.SubMenuItem>
    )
}