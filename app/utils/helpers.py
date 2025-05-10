def sanitize_for_llm(data: dict) -> dict:
    def serialize_value(value):
        if isinstance(value, dict):
            return "\n".join(f"{k}: {serialize_value(v)}" for k, v in value.items())
        elif isinstance(value, list):
            return ", ".join(serialize_value(v) for v in value)
        elif isinstance(value, (int, float, str, bool)) or value is None:
            return str(value)
        else:
            return str(value)  # Fallback for any custom objects

    return {k: serialize_value(v) for k, v in data.items()}