import './App.css'
import {RouterProvider, createBrowserRouter, NavLink} from 'react-router-dom'
import Home from "./Components/Home/Home.jsx";
import useFetch from "./Hooks/useFetch.jsx";
import {useDispatch} from "react-redux";
import {useEffect} from "react";
import CategoriesSlice from "./ReduxSlices/CategoriesSlice.jsx";
import Tracks from "./Components/Tracks/Tracks.jsx";
import RegistrationPage from "./Components/Registration/RegistrationPage.jsx";

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
            },
            {
                path: "/registration",
                element: <RegistrationPage />
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

