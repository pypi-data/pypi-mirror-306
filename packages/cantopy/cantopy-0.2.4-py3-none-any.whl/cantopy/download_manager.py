from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from cantopy.xenocanto_components import QueryResult, Recording
from os.path import exists, join
import pandas as pd
import requests
import os
import numpy as np


class DownloadManager:
    """A helper class for locally downloading retrieved information from the XenoCanto API.

    Attributes
    ----------
    data_base_path
        The base data folder where we want our download manager to store the downloaded files.
        This can also be a folder that was already used by a previous run of this download
        manager, since it will skip duplicate downloads.
    max_workers
        The maximum number of workers to use for downloading the recordings.
    """

    def __init__(self, data_base_path: str, max_workers: int = 1):
        """Initialize a DownloadManager instance

        Parameters
        ----------
        data_base_path
            The base data folder where we want our download manager to store the downloaded files.
            This can also be a folder that was already used by a previous run of this download
            manager, since it will skip duplicate downloads.
        max_workers : optional
            The maximum number of workers to use for downloading the recordings, by default 1
        """
        self.data_base_path = data_base_path
        self.max_workers = max_workers

    def download_all_recordings_in_queryresult(self, query_result: QueryResult):
        """Download all the recordings contained in the provided QueryResult.

        This function downloads all recordings contained in a QueryResult. Additionally,
        the function also generates and updates a per-species metadata CSV file
        containing additional recording information for each downloaded recording of
        that species like recording_length, date, ... (See the
        :func:`Recording.to_dataframe_row <cantopy.xenocanto_components.Recording.to_dataframe_row>`
        method for the attributes that get logged in this metadata file).

        Note that this function also checks for duplicate recordings that have already
        been downloaded and skips them.

        Parameters
        ----------
        query_result
            The QueryResult instance containing the recordings we want to download.
        """

        # Get all the recordings from the query result
        recordings = query_result.get_all_recordings()

        # First detect the recordings that are already downloaded
        detected_already_downloaded_recordings = (
            self._detect_already_downloaded_recordings(recordings)
        )

        # Download the not-already-downloaded recordings
        not_already_downloaded_recordings = list(
            filter(
                lambda x: detected_already_downloaded_recordings[str(x.recording_id)]
                == "new",
                recordings,
            )
        )
        download_pass_or_fail = self._download_all_recordings(
            not_already_downloaded_recordings,
        )

        # Generate the metadata dataframe for the downloaded recordings
        downloaded_recordings_metadata = self._generate_downloaded_recordings_metadata(
            not_already_downloaded_recordings,
            download_pass_or_fail,
        )

        # Udate the metadata file of each one of the downloaded animals
        self._update_animal_recordings_metadata_files(downloaded_recordings_metadata)

    def _download_all_recordings(self, recordings: list[Recording]) -> dict[str, str]:
        """Download all recordings in the provided recordings list.

        Parameters
        ----------
        recordings
            The list of recordings we want to download.

        Returns
        -------
        dict[str, str]
            A dictionary containing the download status of each recording ("pass" or "fail").
        """
        download_pass_or_fail: dict[str, str] = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:  # type: ignore
            futures = [
                executor.submit(self._download_single_recording, recording)
                for recording in recordings
            ]
            results: str = [future.result() for future in as_completed(futures)]  # type: ignore

        for recording, result in zip(recordings, results):
            download_pass_or_fail[str(recording.recording_id)] = result

        return download_pass_or_fail

    def _download_single_recording(self, recording: Recording) -> str:
        """Download a single recording.

        Parameters
        ----------
        recording
            The recording we want to download.

        Returns
        -------
        str
            The download status of the recording ("pass" or "fail").
        """
        # Generate the path where the recording should be located
        recording_path = join(
            self.data_base_path,
            self._generate_animal_folder_name(recording.english_name),
            f"{recording.recording_id}.mp3",
        )

        # Create the base animal folder if it does not exist yet
        try:
            os.mkdir(
                join(
                    self.data_base_path,
                    self._generate_animal_folder_name(recording.english_name),
                )
            )
        except Exception:
            pass

        # Download the recording
        try:
            response = requests.get(recording.audio_file_url)

            if response.status_code != 200:
                return "fail"

            open(recording_path, "wb").write(response.content)

            return "pass"
        except Exception:
            return "fail"

    def _update_animal_recordings_metadata_files(
        self, downloaded_recordings_metadata: pd.DataFrame
    ):
        """Update the metadata files of the animals whose recordings were downloaded.

        Parameters
        ----------
        downloaded_recordings_metadata
            The metadata dataframe for the downloaded recordings.
        """

        # Get the list of animals
        animals = (
            list(downloaded_recordings_metadata["english_name"].unique())  # type: ignore
            if len(downloaded_recordings_metadata) > 0
            else []
        )

        # For each animal, update its metadata file
        for animal in animals:
            # Get the animal folder name
            animal_folder_name = self._generate_animal_folder_name(animal)

            # Get the animal metadata file path
            animal_metadata_file_path = join(
                self.data_base_path,
                animal_folder_name,
                f"{animal_folder_name}_recording_metadata.csv",
            )

            # Get the animal metadata file
            animal_metadata = pd.read_csv(animal_metadata_file_path, dtype="object")  # type: ignore

            # Append the new metadata to the animal metadata file
            animal_metadata = pd.concat(  # type: ignore
                [
                    animal_metadata,
                    downloaded_recordings_metadata[
                        downloaded_recordings_metadata["english_name"] == animal
                    ],  # type: ignore
                ],
                ignore_index=True,
            )

            # Temporarily set the recording_id column to be of type int64 for sorting
            animal_metadata["recording_id"] = animal_metadata["recording_id"].astype(
                np.int64
            )

            # Sort the animal metadata file by recording id
            animal_metadata = animal_metadata.sort_values(by=["recording_id"])  # type: ignore

            # Reset the recording_id column to be of type object
            animal_metadata["recording_id"] = animal_metadata["recording_id"].astype(
                "object"
            )

            # Update the animal metadata file
            animal_metadata.to_csv(animal_metadata_file_path, index=False)

    def _detect_already_downloaded_recordings(
        self, recordings: list[Recording]
    ) -> dict[str, str]:
        """Detect the recordings that are already downloaded in the data folder.

        Parameters
        ----------
        recordings
            The list of recordings we want to check for already downloaded recordings.

        Returns
        -------
        dict[str, str]
            A dictionary containing the input recording ids as keys and their downloaded status as values
            ("already_downloaded" or "new").
        """
        detected_already_downloaded_recordings: dict[str, str] = {}

        for recording in recordings:
            species_folder_name = self._generate_animal_folder_name(
                recording.english_name
            )
            # Generate the path where the recording should be located
            recording_path = join(
                self.data_base_path,
                species_folder_name,
                f"{recording.recording_id}.mp3",
            )

            if exists(recording_path):
                detected_already_downloaded_recordings[str(recording.recording_id)] = (
                    "already_downloaded"
                )
            else:
                detected_already_downloaded_recordings[str(recording.recording_id)] = (
                    "new"
                )

        return detected_already_downloaded_recordings

    def _generate_downloaded_recordings_metadata(
        self, recordings: list[Recording], download_pass_or_fail: dict[str, str]
    ) -> pd.DataFrame:
        """Generate the metadata dataframe for the downloaded recordings.

        Parameters
        ----------
        recordings
            The list of recordings we want to generate the metadata dataframe for.
        download_pass_or_fail
            A dictionary containing the downloaded status of each recording ("pass" or "fail").

        Returns
        -------
        pd.DataFrame
            The metadata dataframe for the downloaded recordings.
        """

        downloaded_recording_metadata = pd.DataFrame({})

        for recording in recordings:
            # Only generate recording information for downloaded recordings
            if download_pass_or_fail[str(recording.recording_id)] == "pass":
                downloaded_recording_metadata = pd.concat([downloaded_recording_metadata, recording.to_dataframe_row()])  # type: ignore

        return downloaded_recording_metadata

    def _generate_animal_folder_name(self, animal_english_name: str) -> str:
        """Generate the download folder name for the animal recordings based on their english name.

        Parameters
        ----------
        animal_english_name
            The english name of the animal.

        Returns
        -------
        str
            The generated download folder name for the animal recordings.
        """
        # To lowercase
        animal_folder_name = animal_english_name.lower()

        # Remove spaces
        animal_folder_name = animal_folder_name.replace(" ", "_")

        # Remove special characters
        animal_folder_name = animal_folder_name.replace("-", "_")

        return animal_folder_name
