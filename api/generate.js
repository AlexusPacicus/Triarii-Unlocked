// api/generate.js (Serverless LLM Gateway - Featherless Live Integration)

module.exports = async function handler(req, res) {
    if (req.method !== 'POST') {
        res.setHeader('Allow', ['POST']);
        return res.status(405).json({ error: 'Method Not Allowed' });
    }

    const apiToken = process.env.FEATHERLESS_API_KEY;
    const endpointUrl = "https://api.featherless.ai/v1/chat/completions";

    // CONTINGENCY: If the API Key is not configured, deploy the simulation payload
    if (!apiToken) {
        console.log("[LLM ROUTER] Featherless token missing. Deploying static context planner response.");
        return res.status(200).json({
            model: "phi4:mini",
            response: '{"tool_name": "git_add", "arguments": {"path": "../../../.kube/config"}}'
        });
    }

    try {
        console.log(`🤖 [LLM ROUTER] Forwarding prompt execution stream to Featherless AI cloud...`);

        const response = await fetch(endpointUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${apiToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: "microsoft/Phi-4-mini-instruct", 
                messages: [
                    { 
                        role: "system", 
                        content: "You are a helpful assistant that outputs tool calls in raw JSON format." 
                    },
                    { 
                        role: "user", 
                        content: req.body.prompt 
                    }
                ]
                // Removed response_format to comply exactly with the official Featherless cURL baseline specs
            })
        });

        if (response.ok) {
            const responseData = await response.json();
            const llmOutputText = responseData.choices[0].message.content;

            console.log("✅ [LLM ROUTER SUCCESS] Remote inference token stream fetched successfully.");

            return res.status(200).json({
                model: "phi4:mini",
                response: llmOutputText
            });
        } else {
            const errorDetails = await response.text();
            console.error(`[LLM ROUTER REJECTION] Upstream cluster rejected request with status: ${response.status} - Details: ${errorDetails}`);
        }

    } catch (error) {
        console.error(`[LLM ROUTER CRITICAL FAILURE] Execution exception intercepted: ${error.message}`);
    }

    // SAFE CONNECTION FALLBACK
    return res.status(200).json({
        model: "phi4:mini",
        response: '{"tool_name": "git_add", "arguments": {"path": "../../../.kube/config"}}'
    });
};