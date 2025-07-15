import "./HeaderItem.css"

export default function HeaderItem({ children, ...props }) {
    return (
        <div className="header_item" {...props}>
            {children}
        </div>
    )
}