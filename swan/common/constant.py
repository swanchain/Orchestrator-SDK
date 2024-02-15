# ./swan/common/constant.py

# Swan API
API_TOKEN = "/api_token"
DELETE_API_TOKEN = "/api_token/delete"
VALIDATE_API_TOKEN = "/api_token/validate"
ADDRESS_FROM_TOKEN = "/address_from_token"
LOGIN = "/login"
LOGIN_WITH_API_KEY = "/login_by_api_key"
PUBLIC_ADDRESS = "/public_address"
COMPUTE_PROVIDER = "/cp"
AUTHENTICATE_PROVIDER = "/cp/<string:apikey>"
CONNECT_CP = "/cp/connect"
UPDATE_CP = "/cp/update"
DELETE_CP = "/cp/delete"
PROVIDER_DASHBOARD = "/cp/dashboard"
UPDATE_CP_RESOURCES = "/cp/summary"
UPDATE_CP_STATUS = "/cp/heartbeat"
GET_CP_MACHINES = "/cp/machines"
CHECK_ACTIVE_CP = "/cp/active"
FILTER_CP_BY_NAME = "/cp/filter/<string:serach_string>"
GET_CP_DETAILS = "/cp/details/<string:node_id>"
UPDATE_JOB_STATUS = "/job/status"
SPACE_CP_DETAIL = "/cp/<string:node_id>/<string:task_uuid>"
COLLATERAL_BALANCE = "/cp/collateral/<string:cp_address>"
EXTEND_JOBS = "/cp/extend_task"
CHECK_FROZEN_COLLATERAL = "/check_holding_collateral/<string:wallet_address>"
CP_DISTRIBUTION = "/cp_distribution"
AVAILABLE_CPS = "cp_avilable"
CP_LIST = "/cp_list"
CP_DETAIL = "/cp_detail/<string:cp_id>"
DEPLOY_SPACE = "/v1/space_deployment"
DEPLOYMENT_INFO = "/v1/space_deployment/<string:task_uuid>"
CONFIG_ORDER = "/v1/active_order/<string:task_uuid"
HOST_INFO = "/host/info"
AUCTION_INFO = "/auction/info"
STATS = "/stats/general"
TASK_BIDDING = "/task/bidding"
TASKS = "/tasks"
JOB_UUID = "/tasks/job_uuid/<string:task_uuid>"
DEPLOY_STATUS = "/tasks/deploy_space/<string:task_uuid>"
REFUNDABLE_STATUS = "check_refundable/<string:task_uuid>"
USER_PROVIDER_PAYMENTS = "/user/provider/payments"
PROVIDER_PAYMENTS = "/provider/payments"
WALLET_ADDRESS = "/jwt_info"
VALIDATE_PAYMENT = "/payment_validate"
CLAIM_REVIEW = "/claim_review"
TERMINATE_TASK = "/terminate_task"
# API Syntax
REST_API_VERSION = "v1"
GET = "GET"
PUT = "PUT"
POST = "POST"
DELETE = "DELETE"

# Contract
