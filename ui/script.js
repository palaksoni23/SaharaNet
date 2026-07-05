async function sendReport() {

    const data = {
        location: document.getElementById("location").value,
        people_count: parseInt(document.getElementById("people").value),
        situation_types: [document.getElementById("situation").value],
        urgency: document.getElementById("urgency").value,
        language: document.getElementById("language").value
    };

    try {
        const res = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        document.getElementById("output").innerText =
            JSON.stringify(result, null, 2);

    } catch (err) {
        document.getElementById("output").innerText =
            "Error: Backend not responding ❌";
    }
}