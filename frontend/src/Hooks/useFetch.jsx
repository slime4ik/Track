export default function useFetch(url, setFetchData, requestExtraParameters = {}) {
    async function fetchUrl() {
        const response = await fetch(url, {...requestExtraParameters});

        if (!response.ok) {
            throw new Response("Failed to fetch json", {
                status: response.status,
                statusText: response.statusText,
            })
        }

        const json = await response.json()

        if (!json) {
            throw new Response("Failed to load json", {
                status: response.status,
                statusText: response.statusText,
            })
        }

        setFetchData(json)
    }

    fetchUrl()
}