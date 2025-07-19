export default function useFetch(url, successfulCallback, errorCallback, requestExtraParameters = {}) {
    async function fetchUrl() {
        const response = await fetch(url, {...requestExtraParameters});

        const json = await response.json()
        if (!json) {
            errorCallback({message: "Не удалось получить JSON"});
        }

        if (!response.ok) {
            errorCallback(json);
        }

        successfulCallback(json)
    }

    fetchUrl()
}