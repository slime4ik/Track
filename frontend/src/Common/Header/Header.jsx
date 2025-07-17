import HeaderItem from "./HeaderItem";
import HeaderSubMenuItem from "./SubMenus/HeaderSubMenu/HeaderSubMenuItem.jsx";
import HeaderSubMenuContent from "./SubMenus/HeaderSubMenu/HeaderSubMenuContent.jsx";
import HeaderSubMenuButton from "./SubMenus/HeaderSubMenu/HeaderSubMenuButton.jsx";
import {motion} from "framer-motion";
import "./Header.css"

export default function Header({children = null, ...props}) {
    return (
        <motion.header {...props}>
            {children}
        </motion.header>
    )
}

Header.Item = HeaderItem
Header.SubMenuContent = HeaderSubMenuContent
Header.SubMenuButton = HeaderSubMenuButton
Header.SubMenuItem = HeaderSubMenuItem