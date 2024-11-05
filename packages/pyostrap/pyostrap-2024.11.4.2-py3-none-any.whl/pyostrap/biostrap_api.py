from datetime import date, datetime
import logging
from typing import List

from pyostrap.models import (
    Biometrics,
    CalorieDetailsGranular,
    DeviceInfo,
    JobStatus,
    LockStatus,
    Pagination,
    Scores,
    User,
    Users,
)
from pyostrap.rest_adapter import RestAdapter
from pyostrap.util import get_rfc3339_str


class BiostrapApi:
    def __init__(
        self,
        api_key: str,
        hostname: str = "api-beta.biostrap.com",
        ver: str = "v1",
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        self._rest_adapter = RestAdapter(api_key, hostname, ver, ssl_verify, logger)

    # Biometrics
    def get_user_biometrics(
        self, last_timestamp: datetime, limit: int, user_id: str
    ) -> Biometrics:
        if limit < 1 or limit > 50:
            raise ValueError("Limit must be between 1 and 50, inclusive")

        ep_params = {
            "last-timestamp": get_rfc3339_str(last_timestamp),
            "limit": limit,
            "user_id": user_id,
        }
        result = self._rest_adapter.get(endpoint="biometrics", ep_params=ep_params)
        if not result.data:
            return None
        return Biometrics(**result.data)

    # Calories
    def get_calorie_details_granular(
        self,
        user_id: str,
        date: date,
        granularity: str,
        user_timezone_offset_in_mins: int = 0,
    ) -> CalorieDetailsGranular:
        ep_params = {
            "user_id": user_id,
            "user_timezone_offset_in_mins": user_timezone_offset_in_mins,
            "date": date.strftime("%Y-%m-%d"),
            "granularity": granularity,
        }
        result = self._rest_adapter.get(endpoint="calorie/details", ep_params=ep_params)
        return CalorieDetailsGranular(**result.data)

    # Device Information
    def get_device_info(self, user_id: str) -> List[DeviceInfo]:
        ep_params = {"user_id": user_id}
        result = self._rest_adapter.get(endpoint="device-info", ep_params=ep_params)
        return [DeviceInfo(**device) for device in result.data["devices"]]

    # Organizations
    def download_raw_data(
        self,
        target_email: str,
        start_time: datetime,
        end_time: datetime,
        user_ids: List[str],
        data_to_download: List[str],
        output_file_formats: List[str],
        anonymize_ids: bool = False,
    ) -> str:
        json_body = {
            "target_email": target_email,
            "start_time": get_rfc3339_str(start_time),
            "end_time": get_rfc3339_str(end_time),
            "user_ids": user_ids,
            "data_to_download": data_to_download,
            "output_file_formats": output_file_formats,
            "anonymize_ids": anonymize_ids,
        }
        result = self._rest_adapter.post(
            endpoint="organizations/data-download/raw/send-request", data=json_body
        )
        return result.data["job_id"]

    def get_job_status(self, job_id: str) -> JobStatus:
        ep_params = {"job_id": job_id}
        result = self._rest_adapter.get(
            endpoint="organizations/job-status", ep_params=ep_params
        )
        return JobStatus(**result.data["data"])

    def lock_or_unlock_device_to_user(
        self,
        user_id: str,
        device_type: str,
        device_mac_address_or_id_encoded: str,
        operation: str,
    ):
        json_body = {
            "user_id": user_id,
            "device_type": device_type,
            "device_mac_address_or_id_encoded": device_mac_address_or_id_encoded,
            "operation": operation,
        }

        result = self._rest_adapter.post(
            endpoint="organizations/user-device-lock", data=json_body
        )
        return LockStatus(**result.data)

    def get_users(self, page: int, items_per_page: int) -> Users:
        ep_params = {"page": page, "items_per_page": items_per_page}
        result = self._rest_adapter.get(
            endpoint="organizations/users", ep_params=ep_params
        )
        pagination = Pagination(**result.data["pagination"])
        user_list = [User(**raw_user) for raw_user in result.data["users"]]
        return Users(user_list, pagination.page < pagination.available_pages)

    # Scores
    def get_user_scores(self, day: date, user_id: str) -> Scores:
        ep_params = {"date": day.isoformat(), "user_id": user_id}
        result = self._rest_adapter.get(endpoint="scores", ep_params=ep_params)
        if not result.data:
            return None
        return Scores(**result.data)

    # Users
    def get_user(self, user_id: str) -> User:
        ep_params = {"user_id": user_id}
        result = self._rest_adapter.get(endpoint="user", ep_params=ep_params)
        return User(**result.data["data"])
