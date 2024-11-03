import oci
from oci.generative_ai_inference import GenerativeAiInferenceClient, models
from oci import generative_ai
from typing import Literal, List, Dict
from contextlib import suppress

llama_3170_germany = {
    "model_id": "ocid1.generativeaimodel.oc1.eu-frankfurt-1.amaaaaaask7dceyatobkuq6yg3lqeqhawaj3i7pckwaoeyf2liwnzvgtp6ba",
    "region": "eu-frankfurt-1",
}


def get_free_trial_remaining():
    try:
        config = oci.config.from_file()

        # Create base client directly for identity service
        signer = oci.Signer(
            tenancy=config["tenancy"],
            user=config["user"],
            fingerprint=config["fingerprint"],
            private_key_file_location=config.get("key_file"),
            private_key_content=config.get("key_content"),
        )
        base_client = oci.base_client.BaseClient(
            service="identity",
            config=config,
            signer=signer,  # Will use default signer from config
            service_endpoint="https://identity.ap-mumbai-1.oci.oraclecloud.com",
            base_path="/20190111",
            type_mapping={},
        )

        # Prepare request parameters
        tenancy_id = config['tenancy']
        subscription_id = "32530219"

        query_params = {"compartmentId": tenancy_id, "subscriptionId": subscription_id, "isCommitInfoRequired": "true"}

        # Make the API call using base_client
        response = base_client.call_api(resource_path="/subscriptions", method="GET", query_params=query_params, header_params={}, response_type="object")
        used = float(response.data[0]['subscribedServices'][1]['usedAmount'])
        available = float(response.data[0]['subscribedServices'][1]['availableAmount'])
        return {'used': used, "available": available} if response else None

    except Exception as e:
        print(f"Error getting usage limits: {str(e)}")
        return None


def list_models(compartment_id):
    config = oci.config.from_file()
    # possible regions
    regions = ["sa-saopaulo-1", "eu-frankfurt-1", "uk-london-1", "us-chicago-1"]

    generative_ai_client = generative_ai.GenerativeAiClient(config, service_endpoint="https://generativeai.eu-frankfurt-1.oci.oraclecloud.com")

    list_models_response = generative_ai_client.list_models(compartment_id=compartment_id, capability=["CHAT"], display_name="meta.llama-3.1-70b-instruct")

    return list_models_response.data


def simple_msgs(msgs: List[Dict[str, str]]):
    """
    input:
        [{"system": "expert programmer"}, {"user": "how to print in python"}]
    output:
        [{"role": "SYSTEM", "content": [{"type": "TEXT", "text": "expert programmer"}]},...etc]
    """

    return [{"role": r.upper(), "content": [{"type": "TEXT", "text": c}]} for m in msgs for r, c in m.items()]


def chat(
    messages=[],
    model_id: str | None = None,
    region: Literal['us-chicago-1', 'eu-frankfurt-1'] | str = "eu-frankfurt-1",
):
    # Configuration
    endpoint = f"https://inference.generativeai.{region}.oci.oraclecloud.com"
    model_id = llama_3170_germany.get('model_id')

    if model_id is None:
        raise ValueError("model_id is required")
    if region not in model_id:
        raise ValueError("model_id must be in the same region as the endpoint, possible misconfiguration by user")

    # Create client
    config = oci.config.from_file()
    # print(config)
    compartment_id = config['tenancy']
    client = GenerativeAiInferenceClient(config=config, service_endpoint=endpoint, retry_strategy=oci.retry.NoneRetryStrategy(), timeout=(10, 240))

    # prepare shitty oracle to universal standard

    with suppress(Exception):
        messages = simple_msgs(messages)

    # Create chat request
    chat_request = models.ChatDetails(
        serving_mode=models.OnDemandServingMode(model_id=model_id),
        compartment_id=compartment_id,
        chat_request=models.GenericChatRequest(
            api_format=models.BaseChatRequest.API_FORMAT_GENERIC,
            messages=messages,
            max_tokens=4000,
            temperature=0.1,
            # frequency_penalty=0,
            # presence_penalty=0,
            # top_p=0.75,
            # top_k=-1,
        ),
    )

    # Get chat response
    chat_response: str = (c := client.chat(chat_request)).data.chat_response.choices[0].message.content[0].text

    return chat_response


if __name__ == "__main__":

    # Get trial balance
    trial_balance = get_free_trial_remaining()
    if trial_balance:
        print(f"Danger Balance Zone: {trial_balance}")

    # Usage example:
    response = chat([{"user": "biggest known planet in universe, and details"}], **llama_3170_germany)
    print((response))

# list
# response = list_models("ocid1.tenancy.oc1..aaaaaaaacibzcstouxwteyvshebzb2zyw5atfqbaunyqikc46vjccogpjaha")
# print(response)
