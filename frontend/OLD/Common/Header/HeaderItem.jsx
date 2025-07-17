import "./HeaderItem.css"
import {motion} from "framer-motion";

export default function HeaderItem({ children, ...props }) {
    return (
        <motion.div className="header_item" {...props}>
            {children}
        </motion.div>
    )
}