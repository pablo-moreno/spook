from unittest import TestCase
from spook.transformers import Transformer


def parse_vat_id(vat_id):
    return f"{vat_id[:8]}-{vat_id[-1]}"


class CustomTransformer(Transformer):
    mappings = {"NAME": "name", "FIRST_NAME": "first_name", "VAT_ID": "vat_id"}
    value_mappings_functions = {
        "VAT_ID": parse_vat_id,
    }


class TestTransformers(TestCase):
    def test_transformer_dict(self):
        data = {
            "NAME": "John",
            "FIRST_NAME": "Doe",
            "VAT_ID": "11111111H",
            "NOT_EXISTING": "value",
        }
        transformer = CustomTransformer(initial_data=data)
        result = transformer.transform()
        assert result["name"] == data["NAME"]
        assert result["first_name"] == data["FIRST_NAME"]
        assert result["vat_id"] == parse_vat_id(data["VAT_ID"]) == "11111111-H"
        assert result.get("NOT_EXISTING") is None

    def test_transformer_list(self):
        data = [{"NAME": "John", "FIRST_NAME": "Doe", "VAT_ID": "11111111H"}]
        transformer = CustomTransformer(initial_data=data)
        result = transformer.transform()
        assert result[0]["name"] == data[0]["NAME"]
        assert result[0]["first_name"] == data[0]["FIRST_NAME"]
        assert result[0]["vat_id"] == parse_vat_id(data[0]["VAT_ID"]) == "11111111-H"
