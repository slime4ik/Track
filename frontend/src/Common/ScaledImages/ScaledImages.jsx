import "./ScaledImages.css"
import {useState} from "react";

export default function ScaledImages({images, onClose}) {
    const [selectedImage, setSelectedImage] = useState(images[0])

    return (<div id="scaled_images_container" onClick={(e) => {
        if (e.target.id === "scaled_images_container") {
            onClose()
        }
    }}>
        <div id="scaled_images_block">
            <div id="scaled_images_list">
                {images.map(image => <img key={image} onClick={() => setSelectedImage(image)} className="scaled_image" src={image} alt=""/>)}
            </div>
            <div id="selected_scaled_image">
                <img src={selectedImage} alt=""/>
            </div>
        </div>
    </div>)
}