import './App.css'
import {RouterProvider, createBrowserRouter, NavLink} from 'react-router-dom'
import Home from "./Home/Home.jsx";
import useFetch from "./Hooks/useFetch.jsx";
import {useDispatch, useSelector} from "react-redux";
import {useEffect} from "react";
import CategoriesSlice from "./ReduxSlices/CategoriesSlice.jsx";
import Tracks from "./Tracks/Tracks.jsx";

const mainRouter = createBrowserRouter([
    {
        path: '/',
        children: [
            {'path': '/',
                element: <Home />
            },
            {
                path: '/tracks',
                element: <Tracks />,
            }
        ]
    }
])

function App() {
    const dispatch = useDispatch()

    function setFetchedData(data) {
        dispatch(CategoriesSlice.actions.setCategories(data.categories))
    }

    useEffect(() => {
        useFetch("http://localhost:8000/api/home?format=json", setFetchedData)
    }, []);

    return (
      <RouterProvider router={mainRouter}>
      </RouterProvider>
    )
}

export default App

