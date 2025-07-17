import {useEffect} from "react";
import {useInView} from "react-intersection-observer";
import "./TrackList.css"

export default function TrackList({tracks, scrolledToLastItemCallback = () => {}}) {
    const [lastTrackItemRef, isInView, entry] = useInView({
        rootMargin: "10%",
        triggerOnce: false
    })

    useEffect(() => {
        if (isInView && entry.isIntersecting) {
            scrolledToLastItemCallback()
        }
    }, [isInView, entry])

    return (
        <div id="track_list">
            {tracks.results?.map((category, index, array) => (
                <div
                    ref={index === array.length - 1 ? lastTrackItemRef : undefined}
                    key={category.id}
                    className="track_list_item"
                >
                    <h3>{category.subject}</h3>
                    <p>{category.description}</p>
                    <p>{category.creator}</p>
                    <p>{category.created_at}</p>
                </div>
            ))}
        </div>
    )
}