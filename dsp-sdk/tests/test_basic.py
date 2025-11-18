from dsp_sdk import Source, Connection, Dataset, Field, validate_source


def test_minimal_manifest_validates():
    source = Source(
        source_id="test_source",
        connection=Connection(type="custom"),
        datasets=[
            Dataset(
                dataset_id="example_dataset",
                kind="custom",
                fields=[Field(name="field1", type="string")],
            )
        ],
    )

    validate_source(source)
