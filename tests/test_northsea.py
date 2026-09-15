from feln import FELN
from layers_json.layers import Layers

from feln_rag.eval import NORTHSEA
from feln_rag.index import load_examples
from feln_rag.rag import system_prompt_okf


def test_bundled_northsea_is_self_contained():
    examples = load_examples(NORTHSEA / "FELN.json")
    layers = Layers.load(str(NORTHSEA / "Layers.json"))
    names = {layer.name for layer in layers}
    assert len(examples) == 1000
    assert len(names) == 5
    assert all(not layer.uri for layer in layers)
    for example in examples:
        assert set(FELN.model_validate(example["meta"]).layers) <= names
    assert "Wells" in system_prompt_okf(NORTHSEA / "okf")
