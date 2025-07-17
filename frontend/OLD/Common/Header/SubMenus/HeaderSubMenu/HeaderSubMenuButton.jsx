import {motion} from "framer-motion";

export default function HeaderSubMenuButton({children, ...props}) {
    return (
        <motion.button {...props}>{children}</motion.button>
    )
}