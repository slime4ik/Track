import HeaderItem from "./HeaderItem";
import HeaderSubMenuItem from "./SubMenus/HeaderSubMenu/HeaderSubMenuItem.jsx";
import HeaderSubMenuContent from "./SubMenus/HeaderSubMenu/HeaderSubMenuContent.jsx";
import HeaderSubMenuButton from "./SubMenus/HeaderSubMenu/HeaderSubMenuButton.jsx";
import "./Header.css"

export default function Header({children = null, ...props}) {
    return (
        <header {...props}>
            {children}
        </header>
    )
}

Header.Item = HeaderItem
Header.SubMenuContent = HeaderSubMenuContent
Header.SubMenuButton = HeaderSubMenuButton
Header.SubMenuItem = HeaderSubMenuItem