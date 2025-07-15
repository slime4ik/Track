import "./CategoriesMenu.css";
import Header from "../Header.jsx";
import { useEffect, useState } from "react";
import useFetch from "../../Hooks/useFetch.jsx";
import SelectSubMenu from "../SubMenus/SelectSubMenu/SelectSubMenu.jsx";
import { AnimatePresence, motion } from "framer-motion";

const SubMenuContent = motion(Header.SubMenuContent);

export default function CategoriesMenu() {
  const [isOpened, setIsOpened] = useState(false);
  const [fetchState, setFetchState] = useState(null);

  useEffect(() => {
    useFetch("http://127.0.0.1:8000/api/home?format=json", setFetchState);
  }, []);

  return (
    <Header.SubMenuItem>
      <Header.SubMenuButton
        className="main_header_sub_button"
        onClick={() => setIsOpened(o => !o)}
      >
        Cats
      </Header.SubMenuButton>

      <AnimatePresence>
        {isOpened && fetchState && (
          <SubMenuContent
            key="categories-submenu"
            initial={{ opacity: 0, y: -20, x: "-50%", }}
            animate={{ opacity: 1, y: 0, x: "-50%", transition: { duration: 0.3 } }}
            exit={{ opacity: 0, y: [-10, -30, -70, -130, -200, -300, -500], transition: { duration: 0.5 } }}
            className="main_header_sub_content"
          >
            <SelectSubMenu
              options={fetchState.categories.map(cat => cat.name)}
            />
          </SubMenuContent>
        )}
      </AnimatePresence>
    </Header.SubMenuItem>
  );
}
