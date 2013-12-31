# contentmodels

A library defining an API for working with [USGIN Content Models](http://schemas.usgin.org/models) in Python.

## Usage

Start by importing the module

```python
import usginmodels
```

This exposes four important functions:

### usginmodels.refresh

Checks http://schemas.usgin.org/contentmodels.json for the most up-to-date description of available content models

Example Usage:

```python
usginmodels.refresh()
```

### usginmodels.get_models

Returns a list of [ContentModel](#contentmodels) objects that represent the models available from USGIN. See below
for a description of the capabilities of [ContentModel](#contentmodels) objects.

Example Usage:

```python
models = usginmodels.get_models
```

### usginmodels.get_uris(uri)

Pass in a URI as a string and a model URI and a version URI are returned. If a version URI can't be determined an empty string will be returned.

Example Usage:

```python
model_uri, version_uri = usginmodels.get_uris("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault")
model_uri, version_uri = usginmodels.get_uris("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/1.2")
```

### usginmodels.get_model(uri)

Pass in a URI as a string and a model object will be returned. If the URI is invalid, an InvalidUri exception will be thrown.

```python
model = usginmodels.get_model("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/1.1")
model = usginmodels.get_model("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault")
```

### usginmodels.get_version(uri)

Pass in a URI as a string and a version object will be returned. If the version is not specified in the URI the latest version will be returned. If the URI is invalid, an InvalidUri exception will be thrown.

```python
version = usginmodels.get_version("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/1.1")
version = usginmodels.get_version("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault")
```

### usginmodels.get_layer(uri, layer_name = "")

Pass in a URI as a string and optionally, a layer name, and a layer object will be returned. If the version is not specified in the URI the latest version will be used. If the layer is not specified and a multilayer model is being requested, an exception will be thrown.

```python
layer = usginmodels.get_layer("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault/1.1")
layer = usginmodels.get_layer("http://schemas.usgin.org/uri-gin/ngds/dataschema/activefault")
layer = usginmodels.get_layer("http://schemas.usgin.org/uri-gin/ngds/dataschema/rockchemistry/0.4", 'USeries')
layer = usginmodels.get_layer("http://schemas.usgin.org/uri-gin/ngds/dataschema/rockchemistry", 'USeries')
```

### usginmodels.validate_file(csv_file, uri, layer_name = "")

Pass in a URI as a string, and a **file-like object** that represents a CSV file. The layer name is optional but will give an error if the model is multilayered. Returned is a boolean specifying if the data is valid or not, a list of error message and a list of lists with the data corrected to conform to NGDS parameters. If there are error messages but valid is True, the file is only valid if the data in dataCorrected is used.

Example Usage:

```python
import csv

my_csv = open("AZRockChemistryUSeries.csv", "r")
csv_text = csv.DictReader(my_csv)

valid, errors, dataCorrected = usginmodels.validate_file(
    csv_text,
    "http://schemas.usgin.org/uri-gin/ngds/dataschema/rockchemistry",
    "USeries"
)

if valid and len(errors) == 0:
    print "Hurrah the document is valid!"
elif valid and len(errors) != 0:
    print "The document is valid if the changes below are acceptable."
    print errors
else:
    print "Not Valid! Error messages:"
    print errors
```