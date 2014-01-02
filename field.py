import datetime
import dateutil.parser as parser

class Field():

    field_name = ""
    field_type = ""
    field_description = ""
    field_optional = bool()

    def __init__(self, field):
        self.field_name = field.get("name", "")
        self.field_type = field.get("type", "")
        self.field_description = field.get("description", "")
        self.field_optional = field.get("optional", "")

    def validate_field(self, data):
        """Check that the data matches the required type: string, double or dateTime"""
        msg = None

        # String type
        if self.field_type == "string":
            try:
                data = str(data)
            except:
                if self.field_optional == False:
                    msg = "Error! Type should be string. Changing " + data + " to Missing"
                else:
                    msg = "Warning! " + self.field_name + " not recognized as a string. Deleting " + data
                    data = ""
            if data == "" and self.field_optional == False:
                data = "Missing"
                msg = "Warning! " + self.field_name + " can't be blank. Changing to Missing"

        # Double type
        elif self.field_type == "double":
            if data != "":
                try:
                    data = float(data)
                except:
                    if self.field_optional == False:
                        msg = "Warning! Type should be double. Changing " + str(data) + " to -9999"
                        data = -9999
                    else:
                        msg = "Warning! " + self.field_name + " not recognized as a double. Deleting " + str(data)
                        data = ""
            else:
                if self.field_optional == False:
                    data = -9999
                    msg = "Warning! " + self.field_name + " can't be blank. Changing to -9999"

        # DateTime type
        elif self.field_type == "dateTime":
            if data != "":
                try:
                    data = (parser.parse(data, default=datetime.datetime(1901, 01, 01, 00, 00, 00))).isoformat()
                except:
                    if self.field_optional == False:
                        msg = "Warning! Type should be dateTime. Changing " + str(data) + " to 1901-01-01T00:00:00"
                        data = datetime.datetime(1901, 01, 01, 00, 00, 00).isoformat()
                    else:
                        msg = "Warning! " + self.field_name + " not recognized as a date. Deleting " + str(data)
                        data = ""
            else:
                if self.field_optional == False:
                    data = datetime.datetime(1901, 01, 01, 00, 00, 00).isoformat()
                    msg = "Warning! " + self.field_name + " can't be blank. Changing to " + data

        # Improper schema or new type
        else:
            msg = "Error! " + self.field_name + ": schema does not indicate string, double or dateTime for this field"

        return msg, data

    def check_uri(self, data, primaryURIField, used_uris):
        """Check that the URI is formatted correctly and, if it is the primary URI, that it is not repeated"""
        msg = None

        if "URI" in self.field_name:
            # If the value is not blank or the word Missing and the field name is not MetadataURI or SourceURI or SourceCitationURI
            if data != "" and data !="Missing" and self.field_name != "MetadataURI" and self.field_name != "SourceURI" and self.field_name != "SourceCitationURI":
                data = data.replace("\n","")
                # Remove any whitespace in the URI, unless there is a pipe character indicating multiple URIs
                if not "|" in data:
                    data = data.replace(" ", "")
                # If the value does not start with "http://resources.usgin.org/uri-gin/"
                if data.find("http://resources.usgin.org/uri-gin/") != 0:
                    msg = "Error! " + self.field_name + ": URI needs to start with http://resources.usgin.org/uri-gin/ (Currently " + data + ".)"
                # If the last character is not a backslash add one
                if data[len(data)-1] != "/":
                    data = data + "/"
                # If the URI has less than 7 backslashes it does not have enough parts
                if data.count("/") < 7:
                    msg = "Error! " + self.field_name + ": URI field does not have enough components."
                # If the current field is the primary URI field there can be no duplicates
                if self.field_name == primaryURIField.field_name:
                    # If the current URI is already in the list of URIs there is an error
                    if data in used_uris:
                        msg = "Error! " + self.field_name + ": URI has already been used. (" + data + ")"
                    # If the current URI is not in the list of URIs add it
                    else:
                        used_uris.append(data)

        return msg, data, used_uris