import {useEffect, useState} from "react";
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

    const [showFullDescriptionTrackIds, setShowFullDescriptionTrackIds] = useState([])
    function toggleFullDescription(trackId) {
        setShowFullDescriptionTrackIds(prevState => {
            if (prevState.includes(trackId)) {
                return prevState.filter(id => id !== trackId)
            } else {
                return [...prevState, trackId]
            }
        })
    }

    return (
        <div id="track_list">
            {tracks.results?.map((track, index, array) => (
                <div
                    ref={index === array.length - 1 ? lastTrackItemRef : undefined}
                    key={track.id}
                    className="track_list_item_container"
                >
                    <div className="track_list_item_main_container">
                        <div className="track_list_item">
                            <div className="track_list_item_top">
                                <div className="track_list_left_container">
                                    <div className="track_list_image_container">
                                        <img className="track_list_item_image" src={track.images[0]?.image || "https://media.discordapp.net/attachments/768729724796534824/1395269376743182388/41e15eff07e0ddce.png?ex=6879d55e&is=687883de&hm=46b15a9fb235e81eb2d392cc14ba704e0a7585c4cc38307cc226bdebd0e1cce0&=&format=webp&quality=lossless"} alt=""/>
                                    </div>
                                    <p className="track_list_left_creator">{track.creator}</p>
                                </div>
                                <div className="track_list_item_data">
                                    <h3 className="track_list_item_subject"><p className={track.completed ? "track_completed" : null}>{track.completed ? "V" : null}</p><p>{track.subject}</p></h3>
                                    <p onClick={() => toggleFullDescription(track.id)} className={`track_list_item_description ${showFullDescriptionTrackIds.includes(track.id) ? "full_description" : ""}`}>{track.description}</p>
                                </div>
                            </div>
                            <div className="track_list_item_bottom">
                                <p className="track_list_item_date">{track.created_at != track.edited_at ? `(edit) ${track.edited_at}` : track.created_at}</p>
                                <p className="track_list_item_categories">{track.category.join(", ")}</p>
                            </div>
                        </div>
                    </div>
                    <div className="tack_list_item_likes">
                        <p>123</p>
                        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/240px-Heart_coraz%C3%B3n.svg.png" alt="Likes"/>
                    </div>
                </div>
            ))}
        </div>
    )
}