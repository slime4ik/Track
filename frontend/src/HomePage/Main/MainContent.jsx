import {useEffect, useState} from "react";
import HamsterSpinner from "./HamsterSpinner.jsx";
import "./HamsterSpinner.css"
import useFetch from "../../Common/Hooks/useFetch.jsx";

export default function MainContent() {
    const [fetchedData, setFetchedData] = useState(null);

    useEffect(() => useFetch("http://127.0.0.1:8000/api/home?format=json", setFetchedData), [])

    return (
        <>
            {!fetchedData && <HamsterSpinner />}
            {fetchedData && JSON.stringify(fetchedData, null, 2)}
        </>
    )
}