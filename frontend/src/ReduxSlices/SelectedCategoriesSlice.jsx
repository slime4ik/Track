import { createSlice } from '@reduxjs/toolkit'

const selectedCategoriesSlice = createSlice({
    name: 'selectedCategories',
    initialState: [],
    reducers: {
        setSelectedCategories: (state, action) => action.payload
    }
})

export default selectedCategoriesSlice