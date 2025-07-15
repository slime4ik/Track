import './App.css'
import HomePage from "./HomePage/HomePage.jsx";
import {RouterProvider, createBrowserRouter, NavLink} from 'react-router-dom'

const mainRouter = createBrowserRouter([
    {
        path: '/',
        children: [
            {'path': '/',
                element: <HomePage />,
            },
        ]
    }
])

function App() {
  return (
      <RouterProvider router={mainRouter}>
      </RouterProvider>
  )
}

export default App

