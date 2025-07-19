import {configureStore} from "@reduxjs/toolkit";
import CategoriesSlice from "./ReduxSlices/CategoriesSlice.jsx"
import selectedCategoriesSlice from "./ReduxSlices/SelectedCategoriesSlice.jsx";

const store = configureStore(
    {
        reducer: {
            categories: CategoriesSlice.reducer,
            selectedCategories: selectedCategoriesSlice.reducer
        }
    }
)

export default store