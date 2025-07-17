export default function getAlreadySelectedCategories(categories) {
    const alreadySelectedJson = localStorage.getItem("selected")
    return alreadySelectedJson ? JSON.parse(alreadySelectedJson) : []
}