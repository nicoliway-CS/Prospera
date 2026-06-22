"""Configuration & credentials.

Single place that reads secrets from the local ``.env`` file, so the rest of the
code never touches the environment directly.
"""

# TODO (week 2): load and expose
#   BASE_URL      -> PROSPERA_BASE_URL
#   API_TOKEN     -> PROSPERA_API_TOKEN   (personal user token, sk-...)
#   AGENT_TOKEN   -> PROSPERA_AGENT_TOKEN (agent token, ak-...)
# and a require_api_token() helper that errors clearly when it's missing.
