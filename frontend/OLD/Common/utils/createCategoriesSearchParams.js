export function createCategoriesSearchParams(categories) {
    return "?category=" + categories.join("&category=")
}