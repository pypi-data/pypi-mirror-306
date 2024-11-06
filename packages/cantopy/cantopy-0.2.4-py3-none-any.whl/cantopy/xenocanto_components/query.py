# Additional information on the Xeno Canto API can be found at:
# https://www.xeno-canto.org/explore/api


class Query:
    """Wrapper for a query passed to the Xeno Canto API.

    This is a simple wrapper that adheres to the query fields of the original XenoCanto
    API. Additional context about these fields can be found at: https://xeno-canto.org/help/search.

    Attributes
    ----------
    species_name : str
        The name of the species, can be either the English name, the scientific name, or the scientific name of the family.
    group : str
        The group of the recording. The `grp` field in the XenoCanto API.
    genus : str
        The genus name of the species. The `gen` field in the XenoCanto API.
    subspecies : str
        The subspecies. The `ssp` field in the XenoCanto API.
    recordist_id : str
        The id of the person who uploaded the recording.  The `rec` field in the XenoCanto API.
    country : str
        The country of the recording. The `cnt` field in the XenoCanto API.
    location : str
        The location of the recording. The `loc` field in the XenoCanto API.
    remarks : str
        Additional remarks for the recording. The `rmk` field in the XenoCanto API.
    animal_seen : str
        If the animal was seen. The `seen` field in the XenoCanto API.
    playback_used : str
        The playback used attribute to set. The `playback` field in the XenoCanto API.
    latitude : str
        The latitude of the recording. The `lat` field in the XenoCanto API.
    longitude : str
        The longitude of the recording. The `lon` field in the XenoCanto API.
    coordinate_box : str
        The coordinate box which should contain the recording location. The `box` field in the XenoCanto API.
    also_attribute : str
        The 'also' attribute is used to search for background species in a recording.  The `also` field in the XenoCanto API.
    song_type : str
        The type of song in the recording. The `type` field in the XenoCanto API.
    other_type : str
        The 'other type' attribute is used when the type field does not contain the desired sound type. The `othertype` field in the XenoCanto API.
    sex : str
        The sex of the species. The `sex` field in the XenoCanto API.
    life_stage : str
        The life stage attribute to set, valid values are: "adult", "juvenile", "nestling", "nymph", and "subadult". The `stage` field in the XenoCanto API.
    recording_method : str
        The recording method of the recording. The `method` field in the XenoCanto API.
    catalog_number : str
        The catalog number of recording to search for a specific recording.  The `nr` field in the XenoCanto API.
    recording_license : str
        The recording license. The `lic` field in the XenoCanto API.
    quality : str
        The quality of the recording. The `q` field in the XenoCanto API.
    recording_length : str
        The length of the recording. The `len` field in the XenoCanto API.
    world_area : str
        The general world area of the recording. The `area` field in the XenoCanto API.
    uploaded_since : str
        Search for recordings UPLOADED after a certain date. The `since` field in the XenoCanto API.
    recorded_year : str
        Search for recordings RECORDED in a certain year. The `year` field in the XenoCanto API.
    recorded_month : str
        Search for recordings RECORDED in a certain month. The `month` field in the XenoCanto API.
    sample_rate : str
        The sample rate of the recording. The `smp` field in the XenoCanto API.

    """

    def __init__(
        self,
        species_name: str,
        group: str = "None",
        genus: str = "None",
        subspecies: str = "None",
        recordist_id: str = "None",
        country: str = "None",
        location: str = "None",
        remarks: str = "None",
        animal_seen: str = "None",
        playback_used: str = "None",
        latitude: str = "None",
        longitude: str = "None",
        coordinate_box: str = "None",
        also_attribute: str = "None",
        song_type: str = "None",
        other_type: str = "None",
        sex: str = "None",
        life_stage: str = "None",
        recording_method: str = "None",
        catalog_number: str = "None",
        recording_license: str = "None",
        quality: str = "None",
        recording_length: str = "None",
        world_area: str = "None",
        uploaded_since: str = "None",
        recorded_year: str = "None",
        recorded_month: str = "None",
        sample_rate: str = "None",
    ):
        """Initialize the query object for passing to the Xeno Canto API.

        These query attributes follow the XenoCanto API search fields. Additional
        context about these fields can be found at: https://xeno-canto.org/help/search.

        Note: As stated in the XenoCanto advanced search documentation, some fiels
        require in certain scenarios the addition of double qoutes, for example,
        `cnt:"United States"`. This also needs to be accounted for when creating a Query,
        this can be done by enclosing the statements containing double qoutes in single
        quotes, e.g. `country = 'cnt:"United States"'`.

        Parameters
        ----------
        species_name
            The name of the species, can be either the English name, the scientific name, or the scientific name of the family.
        group
            The group of the recording. The `grp` field in the XenoCanto API.
        genus
            The genus name of the species. The `gen` field in the XenoCanto API.
        subspecies
            The subspecies. The `ssp` field in the XenoCanto API.
        recordist_id
            The id of the person who uploaded the recording.  The `rec` field in the XenoCanto API.
        country
            The country of the recording. The `cnt` field in the XenoCanto API.
        location
            The location of the recording. The `loc` field in the XenoCanto API.
        remarks
            Additional remarks for the recording. The `rmk` field in the XenoCanto API.
        animal_seen
            If the animal was seen. The `seen` field in the XenoCanto API.
        playback_used
            The playback used attribute to set. The `playback` field in the XenoCanto API.
        latitude
            The latitude of the recording. The `lat` field in the XenoCanto API.
        longitude
            The longitude of the recording. The `lon` field in the XenoCanto API.
        coordinate_box
            The coordinate box which should contain the recording location. The `box` field in the XenoCanto API.
        also_attribute
            The 'also' attribute is used to search for background species in a recording.  The `also` field in the XenoCanto API.
        song_type
            The type of song in the recording. The `type` field in the XenoCanto API.
        other_type
            The 'other type' attribute is used when the type field does not contain the desired sound type. The `othertype` field in the XenoCanto API.
        sex
            The sex of the species. The `sex` field in the XenoCanto API.
        life_stage
            The life stage attribute to set, valid values are: "adult", "juvenile", "nestling", "nymph", and "subadult". The `stage` field in the XenoCanto API.
        recording_method
            The recording method of the recording. The `method` field in the XenoCanto API.
        catalog_number
            The catalog number of recording to search for a specific recording.  The `nr` field in the XenoCanto API.
        recording_license
            The recording license. The `lic` field in the XenoCanto API.
        quality
            The quality of the recording. The `q` field in the XenoCanto API.
        recording_length
            The length of the recording. The `len` field in the XenoCanto API.
        world_area
            The general world area of the recording. The `area` field in the XenoCanto API.
        uploaded_since
            Search for recordings UPLOADED after a certain date. The `since` field in the XenoCanto API.
        recorded_year
            Search for recordings RECORDED in a certain year. The `year` field in the XenoCanto API.
        recorded_month
            Search for recordings RECORDED in a certain month. The `month` field in the XenoCanto API.
        sample_rate
            The sample rate of the recording. The `smp` field in the XenoCanto API.
        """

        self.species_name = species_name
        self.group = group
        self.genus = genus
        self.subspecies = subspecies
        self.recordist_id = recordist_id
        self.country = country
        self.location = location
        self.remarks = remarks
        self.animal_seen = animal_seen
        self.playback_used = playback_used
        self.latitude = latitude
        self.longitude = longitude
        self.coordinate_box = coordinate_box
        self.also_attribute = also_attribute
        self.song_type = song_type
        self.other_type = other_type
        self.sex = sex
        self.life_stage = life_stage
        self.recording_method = recording_method
        self.catalog_number = catalog_number
        self.recording_license = recording_license
        self.quality = quality
        self.recording_length = recording_length
        self.world_area = world_area
        self.uploaded_since = uploaded_since
        self.recorded_year = recorded_year
        self.recorded_month = recorded_month
        self.sample_rate = sample_rate

    def to_string(self) -> str:
        """Generate a string representation of the XenoCantoQuery object for passing to the Xeno Canto API.

        Returns
        -------
        str
            The string representation of the XenoCantoQuery object.
        """

        attributes = [
            f"{self.species_name}",
            f"group:{self.group}",
            f"gen:{self.genus}",
            f"ssp:{self.subspecies}",
            f"rec:{self.recordist_id}",
            f"cnt:{self.country}",
            f"loc:{self.location}",
            f"rmk:{self.remarks}",
            f"seen:{self.animal_seen}",
            f"playback:{self.playback_used}",
            f"lat:{self.latitude}",
            f"lon:{self.longitude}",
            f"box:{self.coordinate_box}",
            f"also:{self.also_attribute}",
            f"type:{self.song_type}",
            f"othertype:{self.other_type}",
            f"sex:{self.sex}",
            f"stage:{self.life_stage}",
            f"method:{self.recording_method}",
            f"nr:{self.catalog_number}",
            f"license:{self.recording_license}",
            f"q:{self.quality}",
            f"length:{self.recording_length}",
            f"area:{self.world_area}",
            f"since:{self.uploaded_since}",
            f"year:{self.recorded_year}",
            f"month:{self.recorded_month}",
            f"smp:{self.sample_rate}",
        ]

        # Remove the None values
        attributes = [attribute for attribute in attributes if "None" not in attribute]

        return " ".join(filter(None, attributes))
