from typing import Optional, List

try:
    from reflex.base import pydantic
except ImportError:
    import pydantic


class VerifyClientRequest(pydantic.BaseModel):
    token: str


class CreateEmailAddressRequest(pydantic.BaseModel):
    user_id: str
    email_address: str
    verified: Optional[bool] = None
    primary: Optional[bool] = None


class UpdateEmailAddressRequest(pydantic.BaseModel):
    verified: Optional[bool] = None
    primary: Optional[bool] = None


class CreatePhoneNumberRequest(pydantic.BaseModel):
    user_id: str
    phone_number: str
    verified: Optional[bool] = None
    primary: Optional[bool] = None
    reserved_for_second_factor: Optional[bool] = None


class UpdatePhoneNumberRequest(pydantic.BaseModel):
    verified: Optional[bool] = None
    primary: Optional[bool] = None
    reserved_for_second_factor: Optional[bool] = None


class CreateUserRequest(pydantic.BaseModel):
    external_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[List[str]] = None
    phone_number: Optional[List[str]] = None
    web3_wallet: Optional[List[str]] = None
    username: Optional[str] = None
    password: Optional[str] = None
    password_digest: Optional[str] = None
    password_hasher: Optional[str] = None
    skip_password_checks: Optional[bool] = None
    skip_password_requirement: Optional[bool] = None
    totp_secret: Optional[str] = None
    backup_codes: Optional[List[str]] = None
    public_metadata: Optional[dict] = None
    private_metadata: Optional[dict] = None
    unsafe_metadata: Optional[dict] = None
    created_at: Optional[str] = None


class UpdateUserRequest(pydantic.BaseModel):
    external_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    primary_email_address_id: Optional[str] = None
    notify_primary_email_address_changed: Optional[bool] = None
    primary_phone_number_id: Optional[str] = None
    primary_web3_wallet_id: Optional[str] = None
    username: Optional[str] = None
    profile_image_id: Optional[str] = None
    password: Optional[str] = None
    password_digest: Optional[str] = None
    password_hasher: Optional[str] = None


class UpsertTemplateRequest(pydantic.BaseModel):
    name: str
    subject: Optional[str] = None
    markup: Optional[str] = None
    body: str
    delivered_by_clerk: Optional[bool] = None
    from_email_name: Optional[str] = None
    reply_to_email_name: Optional[str] = None


class PreviewTemplateRequest(pydantic.BaseModel):
    subject: Optional[str] = None
    body: str
    from_email_name: Optional[str] = None
    reply_to_email_name: Optional[str] = None


class ToggleTemplateDeliveryRequest(pydantic.BaseModel):
    delivered_by_clerk: Optional[bool] = None


class VerifySessionRequest(pydantic.BaseModel):
    token: str


class CreateSessionTokenFromTemplateRequest(pydantic.BaseModel):
    pass


class GetPublicInterstitialParams(pydantic.BaseModel):
    frontendApi: Optional[str] = None
    publishable_key: Optional[str] = None


class GetClientListParams(pydantic.BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None


class GetSessionListParams(pydantic.BaseModel):
    client_id: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None


class GetUserListParams(pydantic.BaseModel):
    email_address: Optional[List[str]] = None
    phone_number: Optional[List[str]] = None
    external_id: Optional[List[str]] = None
    username: Optional[List[str]] = None
    web3_wallet: Optional[List[str]] = None
    user_id: Optional[List[str]] = None
    organization_id: Optional[List[str]] = None
    query: Optional[str] = None
    last_active_at_since: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[str] = None


class GetUsersCountParams(pydantic.BaseModel):
    email_address: Optional[List[str]] = None
    phone_number: Optional[List[str]] = None
    external_id: Optional[List[str]] = None
    username: Optional[List[str]] = None
    web3_wallet: Optional[List[str]] = None
    user_id: Optional[List[str]] = None
    query: Optional[str] = None
