# ./swan/common/constant.py

ORCHESTRATOR_API_TESTNET = "https://swanhub-cali.swanchain.io"
ORCHESTRATOR_API_MAINNET = "https://orchestrator-mainnet-api.swanchain.io"

# Swan API
SWAN_APIKEY_LOGIN = "/login_by_api_key"
DEPLOY_TASK = "/v2/task_deployment"
DEPLOYMENT_INFO = "/v2/task_deployment/"
TASK_LIST = "/v2/task_list"
GET_CP_CONFIG = "/cp/machines"
GET_CP_CONFIG_DP = "/cp/machines-dp-ssh-ready"    # the one of dynamic pricing
GET_GPU_SELECTION_LIST = "/gpu-selection-list"
CUSTOM_INSTANCE = "/custom_instance"
PROVIDER_PAYMENTS = "/provider/payments"
CREATE_TASK = "/v2/task_deployment-dp"
TERMINATE_TASK = "/terminate_task"
CLAIM_REVIEW = "/claim_review"
RENEW_TASK = "/v2/extend_task"
PREMADE_IMAGE = "/util/example_code_mapping"
CONFIG_ORDER_STATUS = "/v2/config_order_status"
TASK_PAYMENT_VALIDATE = '/v2/task_payment_validate'
GET_CONTRACT_INFO = "/contract_info"
GET_ABI_VERSION = "/abi_version"
GET_SOURCE_URI = "/v2/get_source_uri"

# API Syntax
GET = "GET"
PUT = "PUT"
POST = "POST"
DELETE = "DELETE"

# Contract
PAYMENT_CONTRACT_ABI = "PaymentContract.json"
SWAN_TOKEN_ABI = "SwanToken.json"
CLIENT_CONTRACT_ABI = "ClientPayment.json"

# Other
CONTRACT_TIMEOUT = 300
MAX_DURATION = 1209600

# bucket API stuff

MCS_POLYGON_MAIN_API = "https://api.multichain.storage"
MCS_POLYGON_MUMBAI_API = "https://calibration-mcs-api.filswan.com"
MCS_BSC_API = 'https://calibration-mcs-bsc.filswan.com'

FIL_PRICE_API = "https://api.filswan.com/stats/storage"
# swan_mcs api
MCS_PARAMS = "/api/v1/common/system/params"
PRICE_RATE = "/api/v1/billing/price/filecoin"
PAYMENT_INFO = "/api/v1/billing/deal/lockpayment/info"
TASKS_DEALS = "/api/v1/storage/tasks/deals"
MINT_INFO = "/api/v1/storage/mint/info"
UPLOAD_FILE = "/api/v1/storage/ipfs/upload"
DEAL_DETAIL = "/api/v1/storage/deal/detail/"
USER_REGISTER = "/api/v1/user/register"
USER_LOGIN = "/api/v1/user/login_by_metamask_signature"
GENERATE_APIKEY = "/api/v1/user/generate_api_key"
APIKEY_LOGIN = "/api/v2/user/login_by_api_key"
COLLECTIONS = "/api/v1/storage/mint/nft_collections"
COLLECTION = "/api/v1/storage/mint/nft_collection"
# bucket api
CREATE_BUCKET = "/api/v2/bucket/create"
BUCKET_LIST = "/api/v2/bucket/get_bucket_list"
DELETE_BUCKET = "/api/v2/bucket/delete"
FILE_INFO = "/api/v2/oss_file/get_file_info"
DELETE_FILE = "/api/v2/oss_file/delete"
CREATE_FOLDER = "/api/v2/oss_file/create_folder"
CHECK_UPLOAD = "/api/v2/oss_file/check"
UPLOAD_CHUNK = "/api/v2/oss_file/upload"
MERGE_FILE = "/api/v2/oss_file/merge"
FILE_LIST = "/api/v2/oss_file/get_file_list"
GET_FILE = "/api/v2/oss_file/get_file_by_object_name"
GET_GATEWAY = "/api/v2/gateway/get_gateway"
PIN_IPFS = "/api/v2/oss_file/pin_files_to_ipfs"
# contract
USDC_ABI = "ERC20.json"
SWAN_PAYMENT_ABI = "SwanPayment.json"
MINT_ABI = "CollectionFactory.json"

CONTRACT_TIME_OUT = 300

