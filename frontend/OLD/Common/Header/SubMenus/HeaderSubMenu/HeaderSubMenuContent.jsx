import {motion} from "framer-motion";

export default function HeaderSubMenuContent({children, ...props}) {
    return (
        <motion.div {...props}>
            {children}
        </motion.div>
    )
}