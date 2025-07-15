import HeaderItem from "./HeaderItem";
import "./Header.css"

export default function Header({children = null, ...props}) {
    return (
        <header {...props}>
            {children}
        </header>
    )
}

Header.Item = HeaderItem