import {useEffect, useState} from "react";
import {useInView} from "react-intersection-observer";
import "./TrackList.css"
import ScaledImages from "../../../Common/ScaledImages/ScaledImages.jsx";

const MAX_DESCRIPTION_LENGTH_CLOSED = 250

export default function TrackList({tracks, scrolledToLastItemCallback}) {
    const [lastTrackItemRef, isInView, entry] = useInView({
        rootMargin: "10%",
        triggerOnce: false
    })

    tracks.results.forEach(track => {
        if (track.images.length <= 0)
            track.images = [{image:  "https://media.discordapp.net/attachments/768729724796534824/1395269376743182388/41e15eff07e0ddce.png?ex=6879d55e&is=687883de&hm=46b15a9fb235e81eb2d392cc14ba704e0a7585c4cc38307cc226bdebd0e1cce0&=&format=webp&quality=lossless"}]
    })

    useEffect(() => {
        if (isInView && entry.isIntersecting) {
            scrolledToLastItemCallback()
        }
    }, [isInView, entry])

    const [showFullDescriptionTrackIds, setShowFullDescriptionTrackIds] = useState([])

    const [selectedImageTrackId, setSelectedImageTrackId] = useState(null)

    return (
        <>
            {selectedImageTrackId && <ScaledImages images={tracks.results.find(track => track.id === selectedImageTrackId).images.map(image => image.image)} onClose={() => setSelectedImageTrackId(null)}/>}
            {!selectedImageTrackId && <div id="track_list">
                {tracks.results.map((track, index, array) =>
                    <div className="track_list_item_container" key={track.id} ref={index === array.length - 1 ? lastTrackItemRef : undefined}>
                        <div className="track_list_item_top_container">
                            <div className="track_list_item_top_left_container">
                                <div className="track_list_item_top_left_image_container">
                                    <img onClick={() => setSelectedImageTrackId(track.id)} src={track.images[0]?.image} alt={track.subject} />
                                </div>
                                <h2>{track.creator}</h2>
                            </div>
                            <div className="track_list_item_top_right_container">
                                <h2 className="track_list_item_subject">{track.subject}</h2>
                                <p className="track_list_item_description" onClick={() => setShowFullDescriptionTrackIds(
                                    previousShown => {
                                        if (previousShown.includes(track.id)) {
                                            return previousShown.filter(id => id !== track.id)
                                        } else {
                                            return [...previousShown, track.id]
                                        }
                                    }
                                )}>{showFullDescriptionTrackIds.includes(track.id) ? track.description : track.description.slice(0, MAX_DESCRIPTION_LENGTH_CLOSED)}</p>
                            </div>
                        </div>
                        <div className="track_list_item_bottom_container">
                            <div className="track_list_item_bottom_categories">
                                {track.category.join(", ")}
                            </div>
                            <div className="track_list_item_bottom_date">
                                {track.created_at !== track.edited_at ? `(Изм.) ${track.edited_at}` : track.created_at}
                            </div>
                        </div>
                    </div>
                )}
            </div>}
        </>
    )
}