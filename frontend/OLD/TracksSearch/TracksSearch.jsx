import MainHeader from "../Common/Header/MainHeader.jsx";
import HamsterSpinner from "../Common/HamsterLoading/HamsterSpinner.jsx";
import {useEffect, useState} from "react";
import useFetch from "../Common/Hooks/useFetch.jsx";
import {useSearchParams} from "react-router-dom";
import {useSelector} from "react-redux";

const CATEGORIES_URL = "http://localhost:8000/api/tracks/"

export default function TracksSearch() {
    const [isFetched, setIsFetched] = useState(false);
    const [searchParams, setSearchParams] = useSearchParams()

    const selectedCategoriesFromStore = useSelector(state => state.selectedCategories)
    const alreadySelectedFromParams = searchParams.getAll("category")

    const alreadySelected = selectedCategoriesFromStore.length > 0 ? selectedCategoriesFromStore : alreadySelectedFromParams

    function fetchSelectedCategories() {
        const searchLink = `${CATEGORIES_URL}?category=${alreadySelected.join("&category=")}`
        useFetch(searchLink, setIsFetched)
    }

    useEffect(() => {
        fetchSelectedCategories()
    }, [alreadySelected])

    return (
        <>
            <MainHeader />
            {!isFetched && <HamsterSpinner />}
            {isFetched && JSON.stringify(isFetched, null, 2)}
        </>
    )
}
