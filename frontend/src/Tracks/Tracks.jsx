import { useCallback, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { Header } from "../Header/Header.jsx";
import TrackList from "./Main/TrackList.jsx";
import useFetch from "../Hooks/useFetch.jsx";


export default function Tracks() {
    const [searchParams] = useSearchParams();
    const [fetchedTracks, setFetchedTracks] = useState({ results: [] });
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        setIsLoading(true);

        try {
            useFetch(`http://127.0.0.1:8000/api/tracks?${searchParams.toString()}`, (data) => {
                setFetchedTracks(data)
                setIsLoading(false);
            });
        } finally {
            setIsLoading(false);
        }

    }, [searchParams]);

    const fetchMore = useCallback(async () => {
        if (!fetchedTracks.next || isLoading) return;

        setIsLoading(true);
        try {
           useFetch(fetchedTracks.next, (data) => {
                setFetchedTracks(prev => ({
                    ...data,
                    results: [...prev.results, ...data.results]
                }));
           })
        } finally {
            setIsLoading(false);
        }
    }, [fetchedTracks.next, isLoading]);

    return (
        <>
            <Header />
            <TrackList
                tracks={fetchedTracks}
                scrolledToLastItemCallback={fetchMore}
            />
            {isLoading && <div>Loading more tracks...</div>}
        </>
    );
}