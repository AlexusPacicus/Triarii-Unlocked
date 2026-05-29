// api/scrape.js (Node.js Serverless Runtime - Dataset API Real Compliance)

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', ['POST']);
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const { targetUrl } = req.body || {};
    if (!targetUrl) {
        return res.status(400).json({ error: 'Missing required targetUrl parameter inside request body' });
    }

    const apiToken = process.env.BRIGHT_DATA_API_TOKEN;
    const datasetId = process.env.BRIGHT_DATA_DATASET_ID;

    if (!apiToken || !datasetId) {
        return res.status(500).json({
            error: 'Internal Server Configuration Error: Authoritative environment variables missing.'
        });
    }

    try {
        const endpointUrl = `https://api.brightdata.com/datasets/v3/scrape?dataset_id=${datasetId}&notify=false&include_errors=true`;
        const datasetPayload = { input: [{ url: targetUrl }] };

        console.log(`[PROXY OUTBOUND] Forwarding transaction request to Bright Data Cloud Dataset API...`);

        const response = await fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datasetPayload)
        });

        const responseData = await response.json().catch(() => ({}));

        if (!response.ok) {
            console.error(`[PROXY GATEWAY REJECTION] Upstream cluster rejected package with status: ${response.status}`);
            return res.status(response.status).json({
                error: 'Bright Data Dataset API transaction rejected',
                status: response.status,
                details: responseData
            });
        }

        // CONTRATO SINCRONIZADO: Devolvemos collection_id en snake_case de forma legítima
        return res.status(200).json({
            collection_id: responseData.snapshot_id || responseData.snapshotId || "dataset_success_trigger",
            raw: responseData
        });

    } catch (error) {
        console.error(`[PROXY CRITICAL FAILURE] Execution exception intercepted: ${error.message}`);
        return res.status(500).json({ error: 'Internal gateway communication failure.' });
    }
};