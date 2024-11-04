import logging
import pandas as pd
import requests
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import NamedTuple
from werkzeug.datastructures import FileStorage

from .forms.reference import ReferenceForm
from .definitions.processed_fields import BaseProcessedField
from .google_api import API_SETTINGS
from .pre_processing import AlignmentResult, grayscale_image, align_images
from .processing import process_fields


logger = logging.getLogger(__name__)

RegionResults = dict[str, list[BaseProcessedField]]


class JobState(Enum):
    CREATED = auto()
    FILES_SUBMITTED = auto()
    PRE_PROCESSED = auto()

    # Terminal states
    COMPLETED = auto()
    ERROR = auto()


class StateChange(NamedTuple):
    state: JobState
    timestamp: datetime


@dataclass
class HtmlJobInfo:
    name: str
    uuid: str
    last_state: JobState
    last_timestamp: datetime


class Job:
    def __init__(
            self,
            parent_directory: Path,
            job_id: uuid.UUID,
            reference_form: ReferenceForm,
            job_name: str,
    ) -> None:
        self.job_name: str = job_name
        self.job_id: uuid.UUID = job_id
        self.states: list[StateChange] = [StateChange(JobState.CREATED, datetime.now())]
        self.exception: Exception | None = None

        self.reference_form: ReferenceForm = reference_form
        self.submitted_images: dict[int, Path] = {}
        self.alignment_results: dict[int, AlignmentResult] = {}
        self.processed_results: dict[int, RegionResults] = defaultdict(lambda: defaultdict(list))

        # Create a working directory for ourselves
        self.working_dir: Path = parent_directory / str(job_id)
        logger.info(f'Job working directory: {self.working_dir}')
        try:
            self.working_dir.mkdir()
        except Exception as e:
            self._record_exception(e)

    def get_processed_results_count(self) -> int:
        return len(self.processed_results)

    def get_processed_results(self) -> dict[int, RegionResults]:
        return self.processed_results

    def _change_state(self, state: JobState, force: bool = False) -> None:
        if not self.pending_work() and not force:
            logger.warning('Attempting to change state when we are in a terminal state.')
            return

        self.states.append(StateChange(state, datetime.now()))

    def _record_exception(self, exception: Exception) -> None:
        logger.exception('Encountered exception')
        self.exception = exception
        self._change_state(JobState.ERROR)

    def get_current_state(self) -> StateChange:
        return self.states[-1]

    def get_state_changes(self) -> list[StateChange]:
        return self.states

    def to_html_info(self) -> HtmlJobInfo:
        current_state = self.get_current_state()

        return HtmlJobInfo(
            name=self.job_name,
            uuid=str(self.job_id),
            last_state=current_state.state,
            last_timestamp=current_state.timestamp,
        )

    def pending_work(self) -> bool:
        return self.get_current_state().state not in [JobState.ERROR, JobState.COMPLETED]

    def succeeded(self) -> bool:
        return self.get_current_state().state is JobState.COMPLETED

    def progress_to_terminal_state(self, states: list[StateChange]) -> None:
        states.append(self.states[-1])

        while self.pending_work():
            self.progress_processing()
            states.append(self.states[-1])

    def progress_processing(self) -> None:
        if not self.pending_work():
            return

        current_state = self.get_current_state().state
        match current_state:
            case JobState.FILES_SUBMITTED:
                self._pre_process()
            case JobState.PRE_PROCESSED:
                self._process()
            case _:
                logger.warning(f'Unknown state: {current_state}')

    def regress_processing(self) -> None:
        current_state = self.get_current_state().state
        match current_state:
            case JobState.ERROR | JobState.FILES_SUBMITTED | JobState.CREATED:
                return
            case JobState.COMPLETED:
                self.processed_results.clear()
                self._change_state(JobState.PRE_PROCESSED, force=True)
            case JobState.PRE_PROCESSED:
                self.alignment_results.clear()
                self._change_state(JobState.FILES_SUBMITTED, force=True)
            case _:
                logger.warning(f'Unknown state: {current_state}')

    def save_files(self, files: list[FileStorage]) -> None:
        idx = 0
        for file in files:
            # Handle empty FileStorage objects
            if not file.filename:
                logger.warning('Received file without name')
                continue

            # Create the directory for this file
            file_dir_path = self.working_dir / str(idx)
            try:
                file_dir_path.mkdir()
            except Exception as e:
                self._record_exception(e)
                continue

            # Save the original file
            # TODO: This should be called something like "original.[EXTENSION]"
            #  (We need a mapping of the original to the new name if we do this. Metadata file? DB row?)
            file_path = file_dir_path / f'original_{file.filename}'
            logger.info(f'Saving: {file.filename} ({file_path})')

            try:
                file.save(file_path)
                self.submitted_images[idx] = file_path
            except Exception as e:
                self._record_exception(e)
            finally:
                idx += 1

        self._change_state(JobState.FILES_SUBMITTED)

    def update_fields(self, image_id: int, web_form_dict: dict[str, str | list[str]]) -> None:
        web_form_keys = list(web_form_dict.keys())

        for page_region, region_fields in self.processed_results[image_id].items():
            logger.info(f'Updating region: {page_region}')
            for field in region_fields:
                logger.info(f'Updating field: {field.name}')

                # Collect all keys that start with our prefix
                matched_keys = [key for key in web_form_keys if key.startswith(field.form_name())]
                matched_dict = {
                    key: web_form_dict[key] if len(web_form_dict.getlist(key)) == 1 else web_form_dict.getlist(key)
                    for key in matched_keys
                }

                if matched_keys:
                    logger.info(f'Matched keys: {matched_dict}')
                    field.handle_form_update(matched_dict)
                else:
                    field.handle_no_form_update()

                field.validate()

    def export_results(self) -> pd.DataFrame:
        fields_dict = defaultdict(list)
        for image_id, image_results in self.processed_results.items():
            logger.info(f'Exporting results for image: {image_id}')

            for page_region, region_results in image_results.items():
                logger.info(f'Exporting results for region: {page_region}')

                for result in region_results:
                    for column_name, column_value in result.export().items():
                        fields_dict[column_name].append(column_value)

        return pd.DataFrame(fields_dict)

    def _pre_process(self) -> None:
        for image_id, original_path in self.submitted_images.items():
            logger.info(f'Pre-processing {image_id}: {original_path}')

            try:
                # Convert the original image to grayscale
                gray_path = grayscale_image(original_path)
                logger.info(f'Converted image to grayscale: {gray_path}')

                # Align this image to the reference
                alignment_result = align_images(gray_path, self.reference_form)

                self.alignment_results[image_id] = alignment_result
                logger.info(f'Matched features image: {alignment_result.matched_features_image_path}')
                logger.info(f'Overlaid image: {alignment_result.overlaid_image_path}')
                logger.info(f'Aligned image: {alignment_result.aligned_image_path}')
            except Exception as e:
                self._record_exception(e)
                break

        self._change_state(JobState.PRE_PROCESSED)

    def _process(self) -> None:
        # Establish a session to persist an HTTP connection for back-to-back requests
        session = requests.Session()
        session.headers.update(
            {
                'Authorization': f'Bearer {API_SETTINGS.access_token}',
                'x-goog-user-project': API_SETTINGS.project_id,
            }
        )

        for image_index, result in self.alignment_results.items():
            logger.info(f'Processing: {result.aligned_image_path}')

            previous_region_fields = None
            for page_region, region_fields in self.reference_form.regions.items():
                # Create a directory to store the snipped roi pictures for this region
                working_dir = result.aligned_image_path.parent / page_region
                working_dir.mkdir()
                logger.info(f'Processing "{page_region}": {working_dir}')

                try:
                    results = process_fields(
                        session=session,
                        working_dir=working_dir,
                        aligned_image_path=result.aligned_image_path,
                        image_index=image_index,
                        page_region=page_region,
                        region_fields=region_fields,
                        prev_region_fields=previous_region_fields,
                    )

                    previous_region_fields = results
                    self.processed_results[image_index][page_region].extend(results)
                except Exception as e:
                    self._record_exception(e)
                    break

        self._change_state(JobState.COMPLETED)
